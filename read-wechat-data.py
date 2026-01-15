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
from datetime import datetime

from util.get_db_key import get_key
from util.parse_db import parse_db

output_dir = Path(f'output/{datetime.now().isoformat()}'.replace(':', ''))
output_dir.mkdir(exist_ok=True, parents=True)

WeChatFolder = Path(open('private/wechat-folder').read())


# %% ---- 2024-06-22 ------------------------
# Function and class


# %% ---- 2024-06-22 ------------------------
# Play ground
if __name__ == '__main__':
    # gets the key of the WeChat db
    # The 8 is prior parameter without a reason
    key = get_key(WeChatFolder, 8)
    print(f'Got {key=}')

    # reads the db and put them into output_dir after decryption
    parse_db(key, WeChatFolder, output_dir)


# %% ---- 2024-06-22 ------------------------
# Pending


# %% ---- 2024-06-22 ------------------------
# Pending
