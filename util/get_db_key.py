"""
File: get_db_key.py
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
import pymem
import ctypes
import hashlib

ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
void_p = ctypes.c_void_p

# %% ---- 2024-06-22 ------------------------
# Function and class


def get_key(db_path, addr_len):
    def read_key_bytes(h_process, address, address_len=8):
        array = ctypes.create_string_buffer(address_len)
        if ReadProcessMemory(h_process, void_p(address), array, address_len, 0) == 0:
            return "None"
        address = int.from_bytes(
            array, byteorder='little')  # 逆序转换为int地址（key地址）
        key = ctypes.create_string_buffer(32)
        if ReadProcessMemory(h_process, void_p(address), key, 32, 0) == 0:
            return "None"
        key_bytes = bytes(key)
        return key_bytes

    def verify_key(key, wx_db_path):
        if not wx_db_path or wx_db_path.lower() == "none":
            return True
        KEY_SIZE = 32
        DEFAULT_PAGESIZE = 4096
        DEFAULT_ITER = 64000
        with open(wx_db_path, "rb") as file:
            blist = file.read(5000)
        salt = blist[:16]
        byteKey = hashlib.pbkdf2_hmac(
            "sha1", key, salt, DEFAULT_ITER, KEY_SIZE)
        first = blist[16:DEFAULT_PAGESIZE]

        mac_salt = bytes([(salt[i] ^ 58) for i in range(16)])
        mac_key = hashlib.pbkdf2_hmac("sha1", byteKey, mac_salt, 2, KEY_SIZE)
        hash_mac = hmac.new(mac_key, first[:-32], hashlib.sha1)
        hash_mac.update(b'\x01\x00\x00\x00')

        if hash_mac.digest() != first[-32:-12]:
            return False
        return True

    phone_type1 = "iphone\x00"
    phone_type2 = "android\x00"
    phone_type3 = "ipad\x00"

    pm = pymem.Pymem("WeChat.exe")
    module_name = "WeChatWin.dll"

    MicroMsg_path = os.path.join(db_path, "MSG", "MicroMsg.db")

    type1_addrs = pm.pattern_scan_module(
        phone_type1.encode(), module_name, return_multiple=True)
    type2_addrs = pm.pattern_scan_module(
        phone_type2.encode(), module_name, return_multiple=True)
    type3_addrs = pm.pattern_scan_module(
        phone_type3.encode(), module_name, return_multiple=True)
    type_addrs = type1_addrs if len(type1_addrs) >= 2 else type2_addrs if len(type2_addrs) >= 2 else type3_addrs if len(
        type3_addrs) >= 2 else "None"
    # print(type_addrs)
    if type_addrs == "None":
        return "None"
    for i in type_addrs[::-1]:
        for j in range(i, i - 2000, -addr_len):
            key_bytes = read_key_bytes(pm.process_handle, j, addr_len)
            if key_bytes == "None":
                continue
            if db_path != "None" and verify_key(key_bytes, MicroMsg_path):
                return key_bytes.hex()
    return "None"

# %% ---- 2024-06-22 ------------------------
# Play ground


# %% ---- 2024-06-22 ------------------------
# Pending


# %% ---- 2024-06-22 ------------------------
# Pending
