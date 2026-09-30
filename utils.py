#!/usr/bin/env python3
# utils.py - Utility functions

import random
import re
import requests

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Redmi Note 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36",
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def get_headers_with_random_ua(extra=None):
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    if extra:
        headers.update(extra)
    return headers

def fmt_08(phone):
    """Format nomor jadi 08xx"""
    p = re.sub(r'\D', '', str(phone))
    if p.startswith('62'):
        p = '0' + p[2:]
    elif p.startswith('8'):
        p = '0' + p
    if not p.startswith('08'):
        p = '08' + p.lstrip('0')
    return p

def fmt_nocode(phone):
    """Format nomor tanpa kode negara (8xx)"""
    p = re.sub(r'\D', '', str(phone))
    if p.startswith('62'):
        p = p[2:]
    elif p.startswith('0'):
        p = p[1:]
    return p

def fmt_plus(phone):
    """Format nomor jadi +62xx"""
    p = re.sub(r'\D', '', str(phone))
    if p.startswith('0'):
        p = '62' + p[1:]
    elif p.startswith('8'):
        p = '62' + p
    elif not p.startswith('62'):
        p = '62' + p
    return '+' + p

def fmt_phone_only(phone):
    """Format nomor jadi 62xx (tanpa +)"""
    p = re.sub(r'\D', '', str(phone))
    if p.startswith('0'):
        p = '62' + p[1:]
    elif p.startswith('8'):
        p = '62' + p
    elif not p.startswith('62'):
        p = '62' + p
    return p

def get_public_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        return '127.0.0.1'

def extract_csrf(html):
    """Extract CSRF token dari HTML"""
    patterns = [
        r'<meta\s+name="csrf-token"\s+content="([^"]+)"',
        r'<input\s+type="hidden"\s+name="_csrf"\s+value="([^"]+)"',
        r'<input\s+type="hidden"\s+name="_token"\s+value="([^"]+)"',
        r'name="csrf-token"\s+content="([^"]+)"',
    ]
    for p in patterns:
        m = re.search(p, html, re.IGNORECASE)
        if m:
            return m.group(1)
    return None
