import requests
import os
import json
import time
from urllib.parse import urlparse
import argparse

class ProxyTester:
    def __init__(self, proxy_config_file):
        self.proxies_config = self._load_proxy_config(proxy_config_file)
        self.url = "https://httpbin.org/ip"
        self.test_sites = ["https://www.google.com", "https://www.github.com", "https://www.baidu.com", "https://www.bbc.com"]

    def _load_proxy_config(self, config_file):
        with open(config_file, 'r') as file:
            return json.load(file)

    def set_proxy_env(self):
        os.environ['HTTP_PROXY'] = self.proxies_config.get('HTTP_PROXY')
        os.environ['HTTPS_PROXY'] = self.proxies_config.get('HTTPS_PROXY')

    def clear_proxy_env(self):
        os.environ.pop('HTTP_PROXY', None)
        os.environ.pop('HTTPS_PROXY', None)

    def get_proxy_port(self, proxy_url):
        parsed_url = urlparse(proxy_url)
        return parsed_url.port

    def get_ip_location(self, ip):
        max_retries = 3
        retry_delay = 5  # 秒

        for attempt in range(max_retries):
            try:
                # 首选 API: ipapi.co
                location_url = f"https://ipapi.co/{ip}/json/"
                response = requests.get(location_url, timeout=10)
                response.raise_for_status()
                location_data = response.json()
                return location_data.get('city'), location_data.get('country_name')
            except requests.exceptions.RequestException as e:
                print(f"Error getting IP location information from ipapi.co: {e}")
                
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    # 备用 API: ipinfo.io
                    try:
                        backup_url = f"https://ipinfo.io/{ip}/json"
                        response = requests.get(backup_url, timeout=10)
                        response.raise_for_status()
                        location_data = response.json()
                        return location_data.get('city'), location_data.get('country')
                    except requests.exceptions.RequestException as backup_e:
                        print(f"Error getting IP location information from backup API: {backup_e}")
        
        return None, None


    def test_site_speed(self, site):
        try:
            start_time = time.time()
            response = requests.get(site, timeout=10)
            response.raise_for_status()
            end_time = time.time()
            return end_time - start_time
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to {site}: {e}")
            return None

    def run_tests(self):
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()

            ip = response.json()['origin']
            city, country = self.get_ip_location(ip)

            print(f"IP address when using proxy: {ip}")
            if city and country:
                print(f"IP location: {city}, {country}")
            else:
                print("Unable to get IP location information")

            http_proxy_port = self.get_proxy_port(self.proxies_config.get('HTTP_PROXY'))
            https_proxy_port = self.get_proxy_port(self.proxies_config.get('HTTPS_PROXY'))
            print(f"HTTP proxy port: {http_proxy_port}")
            print(f"HTTPS proxy port: {https_proxy_port}")

        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")

        print("\nNetwork Diagnosis:")
        for site in self.test_sites:
            speed = self.test_site_speed(site)
            if speed is not None:
                print(f"Speed connecting to {site} through proxy: {speed:.5f} seconds")
            else:
                print(f"Failed to connect to {site}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Proxy Tester")
    parser.add_argument("--proxy", action="store_true", help="Use proxy")
    parser.add_argument("--config", default="proxies.json", help="Path to proxy configuration file")
    args = parser.parse_args()

    tester = ProxyTester(args.config)

    if args.proxy:
        print("Enabling proxy...")
        tester.set_proxy_env()
    else:
        print("Not using proxy...")
        tester.clear_proxy_env()

    tester.run_tests()


# 运行命令:
# python script_name.py
# python script_name.py --proxy
# python script_name.py --proxy --config=proxies.json