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
            return None
        address = int.from_bytes(
            array, byteorder='little')  # 逆序转换为int地址（key地址）
        k = 32
        key = ctypes.create_string_buffer(k)
        if ReadProcessMemory(h_process, void_p(address), key, k, 0) == 0:
            return None
        key_bytes = bytes(key)
        return key_bytes

    def verify_key(key, wx_db_path):
        from pathlib import Path
        # if not wx_db_path or wx_db_path.lower() == "none":
        #     return True
        assert Path(wx_db_path).is_file(), f'File not exists {wx_db_path=}'
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

    # pm = pymem.Pymem("WeChatAppEx.exe")
    pm = pymem.Pymem("Weixin.exe")
    # module_name = "WeChatWin.dll"
    my_module_name = "Weixin.dll"  # 最可能包含核心逻辑的模块
    MicroMsg_path = os.path.join(db_path, "MSG", "MicroMsg.db")

    # 列出所有加载的模块
    print("=== 微信加载的所有模块 ===")
    modules = [(m.name, m.filename)
               for m in pm.list_modules()]
    modules.sort(key=lambda e: e[1])
    for m in modules:
        print(m)

    # for module in pm.list_modules():
    #     print(
    #         f"模块名: {module.name} | {module.filename}, 基址: {hex(module.lpBaseOfDll)}")
    # modules_info = []
    # for module in pm.list_modules():
    #     if 'AppData' not in module.filename:
    #         continue
    #     info = {
    #         'name': module.name,
    #         'filename': module.filename,
    #         'base': module.lpBaseOfDll,
    #         # 'size': module.size,
    #         # 'size_mb': module.size / 1024 / 1024
    #     }
    #     modules_info.append(info)
    # print(modules_info)
    # for module_info in modules_info:  # 只搜索前3个最大的模块
    #     module_name = module_info['name']
    #     module_filename = module_info['filename']
    #     print(f"\n搜索模块: {module_name} ({module_filename})")

    #     # 读取模块的前1MB内容（如果模块很大）
    #     read_size = 1024*5  # min(module_info['size'], 1024 * 1024)  # 最多1MB
    #     module_data = pm.read_bytes(module_info['base'], read_size)
    #     # print(module_data)
    #     for e in [phone_type1, phone_type2, phone_type3]:
    #         print(e.encode() in module_data)

    for module_name, module_filename in modules:
        if not module_name == my_module_name:
            continue
        print(f'Searching in {module_name=}')
        type1_addrs = pm.pattern_scan_module(
            phone_type1.encode(), module_name, return_multiple=True)
        type2_addrs = pm.pattern_scan_module(
            phone_type2.encode(), module_name, return_multiple=True)
        type3_addrs = pm.pattern_scan_module(
            phone_type3.encode(), module_name, return_multiple=True)
        type_addrs = type1_addrs if len(type1_addrs) >= 2 else type2_addrs if len(type2_addrs) >= 2 else type3_addrs if len(
            type3_addrs) >= 2 else None
        print(type_addrs)
        if type_addrs is not None:
            print(module_name, module_filename)
            break

    # print(type_addrs)
    if type_addrs is None:
        raise ValueError(f'Incorrect {type_addrs=}')

    from tqdm.auto import tqdm
    for j in tqdm(range(1024*1024*1024)):
        key_bytes = read_key_bytes(pm.process_handle, j, addr_len)
        if key_bytes == None:
            continue
        if verify_key(key_bytes, MicroMsg_path):
            return key_bytes.hex()

    # for i in tqdm(type_addrs):
    #     for j in tqdm(range(i, i - 2000, -1)):  # -addr_len):
    #         key_bytes = read_key_bytes(pm.process_handle, j, addr_len)
    #         if key_bytes == None:
    #             continue
    #         # decoded = key_bytes.decode(errors="ignore")
    #         # print(f'Trying {i=} {j=}\n{key_bytes=}\n{decoded=}\n')
    #         if verify_key(key_bytes, MicroMsg_path):
    #             return key_bytes.hex()
    # raise ValueError(f'Failed on all keys')

# %% ---- 2024-06-22 ------------------------
# Play ground


# %% ---- 2024-06-22 ------------------------
# Pending


# %% ---- 2024-06-22 ------------------------
# Pending
