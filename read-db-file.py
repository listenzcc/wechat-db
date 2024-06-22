"""
File: read-db-file.py
Author: Chuncheng Zhang
Date: 2024-06-22
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Read db file for example

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-06-22 ------------------------
# Requirements and constants
import time
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from rich import print
from pathlib import Path
from datetime import datetime
from sql_query.query import Query

from util.constant import MsgTypes, MsgTypesInv

#
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # Or any other Chinese characters

# %% ---- 2024-06-22 ------------------------
# Function and class


def report(*args):
    for i, arg in enumerate(args):
        if i == 0:
            print(f'---- {arg} ----')
        else:
            print(arg)
    print()


def get_basic(conn: sqlite3.Connection, target_table_name: str):
    cursor = conn.execute(query.select_all_tables_name())
    table_names = list(cursor)
    report('Found table_names:', table_names)

    cursor = conn.execute(query.get_cols_from_table(target_table_name))
    cols = list(cursor)
    report(f'Table {target_table_name} contains columns:', cols)

    return dict(
        table_names=table_names,
        target_table_name=target_table_name,
        cols=cols
    )


# %% ---- 2024-06-22 ------------------------
# Play ground
if __name__ == '__main__':
    query = Query()
    root_path = Path(__file__).parent

    # ----------------------------------------
    # ---- Example for MicroMsg.db ----
    db_path = root_path.joinpath('output/MicroMsg.db')
    target_table_name = 'Contact'

    with sqlite3.connect(db_path) as conn:
        basic = get_basic(conn, target_table_name)

        # Select all from the table 'Contact'
        cursor = conn.execute(query.select_from_table(target_table_name))
        contact_df = pd.DataFrame(
            cursor, columns=[e[1] for e in basic['cols']])
        report(f'Everything in table {target_table_name}')
        print(contact_df)

    # ----------------------------------------
    # ---- Example for MSG ----
    db_path = root_path.joinpath('output/MSG7.db')
    target_table_name = 'MSG'
    with sqlite3.connect(db_path) as conn:
        basic = get_basic(conn, target_table_name)

        # Find all the messages from 'mirror--%'
        where = "StrTalker LIKE 'mirror--%'"
        cursor = conn.execute(query.select_from_table(
            target_table_name, where=where))
        msg_df = pd.DataFrame(cursor, columns=[e[1] for e in basic['cols']])
        report(f'Everything in table {target_table_name}')
        print(msg_df)
        print(msg_df['StrContent'])

        # Convert columns
        msg_df['_time'] = msg_df['CreateTime'].map(
            lambda x: pd.to_datetime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x))))
        msg_df['_msg_type'] = msg_df['Type'].map(
            lambda i: MsgTypesInv.get(i, f'-{i}'))
        msg_df['_msg_length'] = msg_df['StrContent'].map(lambda x: len(x))

        # --------------------
        # Plot with sns.relplot as points
        plt.style.use("ggplot")
        grid = sns.relplot(
            msg_df, x='_time', y='_msg_type', col='IsSender', hue='_msg_type')
        grid.tick_params(axis='x', labelrotation=45)
        grid.tight_layout()

        # --------------------
        # Plot with sns.relplot as histplot
        grid = sns.FacetGrid(msg_df, col="IsSender")
        grid.map_dataframe(
            sns.histplot, x="_msg_type", hue="_msg_type")
        grid.tick_params(axis='x', labelrotation=45)
        grid.tight_layout()

        # --------------------
        t = MsgTypes['文本']
        df = msg_df.query(f'Type == {t}')
        fig, axs = plt.subplots(1, 2, figsize=(8, 4))

        ax = axs[1]
        sns.histplot(
            df, hue='IsSender', x='_msg_length',
            legend=True,
            ax=ax)
        ax.set_xlim([0, 100])
        ax.legend(loc='best')

        ax = axs[0]
        sns.violinplot(
            df, x='IsSender', hue='IsSender', y='_msg_length',
            legend='full',
            ax=ax)
        ax.set_ylim([0, 100])
        ax.legend(loc='center', bbox_to_anchor=(0.5, 0.5))

        fig.tight_layout()

        # Show
        plt.show()


# %% ---- 2024-06-22 ------------------------
# Pending


# %% ---- 2024-06-22 ------------------------
# Pending
