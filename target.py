#!/usr/bin/env python3
# targets.py - Target list

TARGETS = [
    # Format: (name, url, type)
    ("HRS-BRE", "https://career.hrs-bre.site", "register"),
    ("Erafone", "https://jeanne.eraspace.com", "otp"),
    ("PlanetBan", "https://api.planetban.com", "otp"),
    ("TuneUp", "https://api.tuneup.id", "otp"),
    ("Klook", "https://www.klook.com", "otp"),
    ("InternetRakyat", "https://internetrakyat.id", "otp"),
    ("Ultramilk", "https://ultramilk-clp.kata.ai", "register"),
    ("Kaniva", "https://daftar.kanivainternationalbali.com", "otp"),
    ("Jembatani", "https://api.jembatani.co.id", "otp"),
    ("RCX", "https://sso.rcx.co.id", "otp"),
    ("SahabatTeknisi", "https://www.sahabatteknisi.co.id", "otp"),
    ("Auto2000", "https://auto2000.co.id", "otp"),
    ("AstraDaihatsu", "https://www.astra-daihatsu.id", "otp"),
    ("RoyalCanin", "https://club.royalcanin.id", "otp"),
    ("Watsons", "https://api.watsons.co.id", "otp"),
    ("99.co", "https://www.99.co", "otp"),
    ("BeliRumah", "https://api.belirumah.co", "otp"),
    ("Fastwork", "https://api.fastwork.id", "otp"),
    ("Beautyhaul", "https://www.beautyhaul.com", "otp"),
    ("Hainaya", "https://app.hainaya.id", "otp"),
    ("MinumYukKaka", "https://minumyukkaka.com", "otp"),
    ("Sidemang", "https://sidemang.palembang.go.id", "otp"),
    ("LaporMasBup", "https://lapormasbup.klaten.go.id", "otp"),
    ("PTSP Kemenag", "https://dev-ptsp.kemenag.go.id", "otp"),
]

def get_targets():
    return TARGETS

def get_target_names():
    return [t[0] for t in TARGETS]
