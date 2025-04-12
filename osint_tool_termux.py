#!/usr/bin/env python3
import requests
import subprocess

def scrape_instagram_profile(username):
    print(f"[+] Fetching Instagram data for {username}...")
    try:
        url = f"https://www.instascraper.org/api/profile/{username}"
        response = requests.get(url)
        data = response.json()

        if "username" in data:
            print(f"Username: {data['username']}")
            print(f"Full Name: {data.get('full_name', 'Not available')}")
            print(f"Followers: {data['followers']}")
            print(f"Following: {data['following']}")
            print(f"Posts: {data['posts']}")
            print(f"Bio: {data['biography']}")
            return data
        else:
            print("[-] Failed to retrieve profile data or user not found.")
            return None

    except Exception as e:
        print(f"[-] Error fetching Instagram data: {str(e)}")
        return None

def get_location_from_ip(ip_address):
    print(f"[+] Getting location for IP: {ip_address}...")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        if data["status"] == "success":
            print(f"IP: {ip_address}")
            print(f"City: {data['city']}")
            print(f"Region: {data['regionName']}")
            print(f"Country: {data['country']}")
            print(f"Coordinates: {data['lat']}, {data['lon']}")
            return data
        else:
            print("[-] Failed to get IP location.")
            return None
    except Exception as e:
        print(f"[-] Error fetching IP info: {str(e)}")
        return None

def scan_network():
    print("[+] Scanning local network for devices...")
    try:
        result = subprocess.check_output(["nmap", "-sn", "192.168.1.0/24"]).decode()
        print(result)
        return result
    except Exception as e:
        print(f"[-] Network scan failed: {str(e)}")
        return None

def lookup_phone_number(phone_number):
    print(f"[+] Looking up phone number: {phone_number}...")
    try:
        response = requests.get(f"https://api.numlookupapi.com/v1/validate/{phone_number}?apikey=free")
        data = response.json()
        if data.get("valid"):
            print(f"Phone Number: {phone_number}")
            print(f"Country: {data['country_name']}")
            print(f"Carrier: {data['carrier']}")
            return data
        else:
            print("[-] Invalid phone number.")
            return None
    except Exception as e:
        print(f"[-] Error looking up phone number: {str(e)}")
        return None

def ultimate_osint_tool(target):
    print(f"[*] Target: {target}")

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
        print("[-] Unsupported input. Try a username, phone number, or IP address.")

    scan_network()

if __name__ == "__main__":
    target = input("Enter target (Instagram username, phone number, or IP): ")
    ultimate_osint_tool(target)
