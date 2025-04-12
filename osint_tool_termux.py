import os
import requests
from bs4 import BeautifulSoup
import subprocess

def get_ip():
    return subprocess.check_output(['hostname', '-I']).decode('utf-8').strip()

def scrape_social_media(username):
    results = {}
    
    # Facebook
    url = f"https://www.facebook.com/{username}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    if soup.find('meta', property='og:title'):
        results['Facebook'] = url
    
    # Instagram
    url = f"https://www.instagram.com/{username}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    if soup.find('meta', property='og:title'):
        results['Instagram'] = url
    
    # Twitter
    url = f"https://twitter.com/{username}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    if soup.find('meta', property='og:title'):
        results['Twitter'] = url
    
    return results

def main():
    username = input("Enter the username: ")
    print(f"\nScraping information for {username}...")
    
    social_media = scrape_social_media(username)
    ip_address = get_ip()
    
    print("\nSocial Media Accounts:")
    for platform, link in social_media.items():
        print(f"{platform}: {link}")
    
    print(f"\nIP Address: {ip_address}")

if __name__ == "__main__":
    main()
