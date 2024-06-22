"""
File: read-wechat-data.py
Author: Chuncheng Zhang
Date: 2024-06-22
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Read WeChatFolder .db files and save them into ./output folder

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-06-22 ------------------------
# Requirements and constants
from pathlib import Path
from tqdm.auto import tqdm

from util.get_db_key import get_key
from util.parse_db import parse_db

root = Path(__file__).parent
output_dir = root.joinpath('output')
output_dir.mkdir(exist_ok=True)

WeChatFolder = Path(open(root.joinpath('private/wechat-folder')).read())


# %% ---- 2024-06-22 ------------------------
# Function and class


# %% ---- 2024-06-22 ------------------------
# Play ground
if __name__ == '__main__':
    # gets the key of the WeChat db
    # The 8 is prior parameter without a reason
    key = get_key(WeChatFolder, 8)
    print(key)

    # reads the db and put them into output_dir after decryption
    parse_db(key, WeChatFolder, output_dir)


# %% ---- 2024-06-22 ------------------------
# Pending


# %% ---- 2024-06-22 ------------------------
# Pending
