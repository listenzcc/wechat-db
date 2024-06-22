"""
File: query.py
Author: Chuncheng Zhang
Date: 2024-06-22
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    SQL query code-book

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-06-22 ------------------------
# Requirements and constants


# %% ---- 2024-06-22 ------------------------
# Function and class
class Query(object):
    _select_all_tables_name = "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';"

    def select_from_table(self, table_name: str, cols: str = '*', where: str = ''):
        if where:
            return f"SELECT {cols} FROM {table_name} WHERE {where}"
        else:
            return f"SELECT {cols} FROM {table_name}"

    def get_cols_from_table(self, table_name: str):
        return f"PRAGMA table_info({table_name})"

    def select_all_tables_name(self):
        return self._select_all_tables_name


# %% ---- 2024-06-22 ------------------------
# Play ground


# %% ---- 2024-06-22 ------------------------
# Pending


# %% ---- 2024-06-22 ------------------------
# Pending
