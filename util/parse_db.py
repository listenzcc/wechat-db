"""
File: parse_db.py
Author: Chuncheng Zhang
Date: 2024-06-22
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Amazing things

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-06-22 ------------------------
# Requirements and constants
import os
import hmac
import shutil
import hashlib
from Cryptodome.Cipher import AES

SQLITE_FILE_HEADER = "SQLite format 3\x00"  # SQLite文件头

KEY_SIZE = 32
DEFAULT_PAGESIZE = 4096
DEFAULT_ITER = 64000

# %% ---- 2024-06-22 ------------------------
# Function and class


def decrypt(key: str, db_path, out_path):
    """
    通过密钥解密数据库
    :param key: 密钥 64位16进制字符串
    :param db_path:  待解密的数据库路径(必须是文件)
    :param out_path:  解密后的数据库输出路径(必须是文件)
    :return:
    """
    if not os.path.exists(db_path) or not os.path.isfile(db_path):
        return False, f"[-] db_path:'{db_path}' File not found!"
    if not os.path.exists(os.path.dirname(out_path)):
        return False, f"[-] out_path:'{out_path}' File not found!"

    if len(key) != 64:
        return False, f"[-] key:'{key}' Len Error!"

    password = bytes.fromhex(key.strip())
    with open(db_path, "rb") as file:
        blist = file.read()

    salt = blist[:16]
    byteKey = hashlib.pbkdf2_hmac(
        "sha1", password, salt, DEFAULT_ITER, KEY_SIZE)
    first = blist[16:DEFAULT_PAGESIZE]
    if len(salt) != 16:
        return False, f"[-] db_path:'{db_path}' File Error!"

    mac_salt = bytes([(salt[i] ^ 58) for i in range(16)])
    mac_key = hashlib.pbkdf2_hmac("sha1", byteKey, mac_salt, 2, KEY_SIZE)
    hash_mac = hmac.new(mac_key, first[:-32], hashlib.sha1)
    hash_mac.update(b'\x01\x00\x00\x00')

    if hash_mac.digest() != first[-32:-12]:
        return False, f"[-] Key Error! (key:'{key}'; db_path:'{db_path}'; out_path:'{out_path}' )"

    newblist = [blist[i:i + DEFAULT_PAGESIZE]
                for i in range(DEFAULT_PAGESIZE, len(blist), DEFAULT_PAGESIZE)]

    with open(out_path, "wb") as deFile:
        deFile.write(SQLITE_FILE_HEADER.encode())
        t = AES.new(byteKey, AES.MODE_CBC, first[-48:-32])
        decrypted = t.decrypt(first[:-48])
        deFile.write(decrypted)
        deFile.write(first[-48:])

        for i in newblist:
            t = AES.new(byteKey, AES.MODE_CBC, i[-48:-32])
            decrypted = t.decrypt(i[:-48])
            deFile.write(decrypted)
            deFile.write(i[-48:])
    return True, [db_path, out_path, key]


def parse_db(key, db_path, output_dir):
    # ? Doesn't know how
    # close_db()

    os.makedirs(output_dir, exist_ok=True)
    tasks = []
    for root, dirs, files in os.walk(db_path):
        for file in files:
            if '.db' == file[-3:]:
                if 'xInfo.db' == file:
                    continue
                inpath = os.path.join(root, file)
                output_path = os.path.join(output_dir, file)
                tasks.append([key, inpath, output_path])
            else:
                try:
                    name, suffix = file.split('.')
                    if suffix.startswith('db_SQLITE'):
                        inpath = os.path.join(root, file)
                        # print(inpath)
                        output_path = os.path.join(output_dir, name + '.db')
                        tasks.append([key, inpath, output_path])
                except:
                    continue
    for i, task in enumerate(tasks):
        flag, msg = decrypt(*task)
        print(f"[{i+1}/{len(tasks)}] {flag} {msg}")

    print('开始数据库合并...')
    # 目标数据库文件
    target_database = os.path.join(output_dir, 'MSG.db')
    # 源数据库文件列表
    source_databases = [os.path.join(
        output_dir, f"MSG{i}.db") for i in range(1, 50)]
    if os.path.exists(target_database):
        os.remove(target_database)
    shutil.copy2(
        os.path.join(output_dir, 'MSG0.db'), target_database)  # 使用一个数据库文件作为模板

    # ? Doesn't know how
    # merge_databases(source_databases, target_database)

# %% ---- 2024-06-22 ------------------------
# Play ground


# %% ---- 2024-06-22 ------------------------
# Pending


# %% ---- 2024-06-22 ------------------------
# Pending
# 通过密钥解密数据库
