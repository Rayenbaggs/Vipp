#!/usr/bin/env python3
import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import sys

def save_page_locally(url, save_dir="/data/data/com.termux/files/home/storage/shared/hosts"):
    print(f"[+] Grabbing the damn page from {url}...")
    try:
        # Create directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # Get the page
        headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code!= 200:
            print(f"[-] Shit, failed to grab {url}. Status code: {response.status_code}")
            return None
        
        # Parse URL to create a safe filename
        parsed_url = urlparse(url)
        filename = f"{parsed_url.netloc.replace('.', '_')}.html"
        filepath = os.path.join(save_dir, filename)
        
        # Save the HTML
        with open(filepath,"w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"[+] Saved the fucking page to {filepath}")
        
        return filepath
    except Exception as e:
        print(f"[-] Fuck, something broke while grabbing the page: {str(e)}")
        return None

def extract_hosts_offline(filepath, base_url):
    print(f"[+] Ripping hosts from {filepath} offline like a badass...")
    try:
        # Read the saved HTML
        with open(filepath,"r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html_content,"html.parser")
        hosts = set()
        
        # Extract from href attributes
        for link in soup.find_all("a", href=True):
            href = link["href"]
            parsed_href = urlparse(urljoin(base_url, href))
            if parsed_href.netloc:
                hosts.add(parsed_href.netloc)
        
        # Extract from src attributes (scripts, images, etc.)
        for tag in soup.find_all(["script","img","iframe"], src=True):
            src = tag["src"]
            parsed_src = urlparse(urljoin(base_url, src))
            if parsed_src.netloc:
                hosts.add(parsed_src.netloc)
        
        # Regex to catch any sneaky hosts in the raw HTML
        host_pattern = r"(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}|(?:\d{1,3}\.){3}\d{1,3}"
        raw_hosts = re.findall(host_pattern, html_content)
        for host in raw_hosts:
            hosts.add(host)
        
        # Filter out bullshit and print the results
        if hosts:
            print("[*] Found these juicy hosts:")
            for host in sorted(hosts):
                print(f" - {host}")
            return hosts
        else:
            print("[-] No fucking hosts found. This site’s dry as hell.")
            return None
    except Exception as e:
        print(f"[-] Shit went wrong while ripping hosts: {str(e)}")
        return None

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: python host_ripper.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    if not url.startswith(("http://","https://")):
        url ="https://" + url
    
    # Step 1: Download the page
    saved_file = save_page_locally(url)
    if not saved_file:
        print("[-] Can’t proceed without the damn page. Check your URL or connection.")
        sys.exit(1)
    
    # Step 2: Extract hosts offline
    extract_hosts_offline(saved_file, url)

if __name__ == "__main__":
    main()
