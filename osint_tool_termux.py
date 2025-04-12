#!/usr/bin/env python3
import requests
import time
import os
import subprocess

def scrape_instagram_profile(username):
    print(f"[+] جارٍ سحب بيانات إنستغرام لـ {username}...")
    try:
        url = f"https://www.instascraper.org/api/profile/{username}"
        response = requests.get(url)
        data = response.json()

        if "username" in data:
            print(f"المستخدم: {data['username']}")
            print(f"الاسم الكامل: {data.get('full_name', 'غير متوفر')}")
            print(f"المتابعين: {data['followers']}")
            print(f"يتابع: {data['following']}")
            print(f"المنشورات: {data['posts']}")
            print(f"البايو: {data['biography']}")
            return data
        else:
            print("[-] فشل جلب البيانات أو المستخدم غير موجود.")
            return None

    except Exception as e:
        print(f"[-] خطأ في سحب بيانات إنستغرام: {str(e)}")
        return None

def get_location_from_ip(ip_address):
    print(f"[+] جارٍ تتبع موقع الـ IP: {ip_address}...")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        if data["status"] == "success":
            print(f"IP: {ip_address}")
            print(f"المدينة: {data['city']}")
            print(f"المنطقة: {data['regionName']}")
            print(f"الدولة: {data['country']}")
            print(f"الإحداثيات: {data['lat']}, {data['lon']}")
            return data
        else:
            print("[-] فشل جلب الموقع لهذا الـ IP!")
            return None
    except Exception as e:
        print(f"[-] خطأ في تتبع الـ IP: {str(e)}")
        return None

def scan_network():
    print("[+] جارٍ مسح الشبكة للعثور على الأجهزة...")
    try:
        result = subprocess.check_output(["nmap", "-sn", "192.168.1.0/24"]).decode()
        print(result)
        return result
    except Exception as e:
        print(f"[-] فشل مسح الشبكة: {str(e)}")
        return None

def lookup_phone_number(phone_number):
    print(f"[+] جارٍ تحليل رقم الهاتف: {phone_number}...")
    try:
        response = requests.get(f"https://api.numlookupapi.com/v1/validate/{phone_number}?apikey=free")
        data = response.json()
        if data.get("valid"):
            print(f"الرقم: {phone_number}")
            print(f"الدولة: {data['country_name']}")
            print(f"المزود: {data['carrier']}")
            return data
        else:
            print("[-] الرقم غير صالح!")
            return None
    except Exception as e:
        print(f"[-] خطأ في تحليل الرقم: {str(e)}")
        return None

def ultimate_osint_tool(target):
    print(f"[*] جارٍ استهداف: {target}")
    
    if "instagram.com" in target:
        username = target.strip("/").split("/")[-1]
        scrape_instagram_profile(username)
    elif not (target.startswith("+") or target.count(".") == 3):
        scrape_instagram_profile(target)
    elif target.startswith("+"):
        lookup_phone_number(target)
    elif target.count(".") == 3:
        get_location_from_ip(target)
    else:
        print("[-] نوع الهدف غير مدعوم! حاول اسم مستخدم، رقم هاتف، أو IP.")

    scan_network()

if __name__ == "__main__":
    target = input("أدخل الهدف (اسم مستخدم، رقم هاتف، أو IP): ")
    ultimate_osint_tool(target)
