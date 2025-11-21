#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSA 实验一 完整实现
运行：python rsa_lab.py
"""

import math
import textwrap

# ---------- 1. 辅助：扩展欧几里得求逆 ----------
def exgcd(a: int, b: int):
    """return (g, x, y) 满足 a*x + b*y = g = gcd(a, b)"""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = exgcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

def modinv(a: int, m: int) -> int:
    """求 a 在模 m 下的逆元，若不存在抛异常"""
    g, x, _ = exgcd(a, m)
    if g != 1:
        raise ValueError("逆元不存在")
    return x % m

# ---------- 2. RSA 密钥生成 ----------
def rsa_keygen(p: int, q: int, e: int):
    n = p * q
    phi = (p - 1) * (q - 1)
    if math.gcd(e, phi) != 1:
        raise ValueError("e 与 phi 不互素")
    d = modinv(e, phi)
    return (n, e), (n, d)   # 公钥，私钥

# ---------- 3. 加密/解密 ----------
def rsa_encrypt(plain_int: int, pub_key) -> int:
    n, e = pub_key
    return pow(plain_int, e, n)

def rsa_decrypt(cipher_int: int, pri_key) -> int:
    n, d = pri_key
    return pow(cipher_int, d, n)

# ---------- 4. 字符串 ↔ 整数互转 ----------
def str2int(s: str) -> int:
    return int.from_bytes(s.encode('utf-8'), 'big')

def int2str(n: int) -> str:
    length = (n.bit_length() + 7) // 8
    return n.to_bytes(length, 'big').decode('utf-8', errors='ignore')

# ---------- 5. 封装：一键跑实验 ----------
def run_case(name: str, p, q, e, plain):
    print(f"========== {name} ==========")
    print(f"p={p}, q={q}, e={e}")
    print(f"明文: {plain}")
    # 1) 生成密钥
    pub, pri = rsa_keygen(p, q, e)
    print(f"公钥(n,e)={pub}")
    print(f"私钥(n,d)={pri}")
    # 2) 明文→整数
    if isinstance(plain, int):
        m = plain
    else:
        m = str2int(plain)
    print(f"明文转为大整数: {m}")
    # 3) 加密
    c = rsa_encrypt(m, pub)
    print(f"密文: {c}")
    # 4) 解密
    m2 = rsa_decrypt(c, pri)
    print(f"解密后大整数: {m2}")
    if isinstance(plain, int):
        print(f"解密后明文: {m2}")
    else:
        print(f"解密后明文: {int2str(m2)}")
    print()

# ---------- 6. 实验指导书给定数据 ----------
if __name__ == "__main__":
    # 数据1 小数据
    run_case("数据1（小）", p=3, q=11, e=7, plain=6)

    # 数据2 大数据
    big_p = 100000007
    big_q = 100000037
    big_e = 39839
    big_plain = 1000000000039
    run_case("数据2（大）", p=big_p, q=big_q, e=big_e, plain=big_plain)

    # 可选：字符串演示
    run_case("字符串演示", p=big_p, q=big_q, e=big_e, plain="Hello RSA!")