import requests
import csv
import os
import time
from datetime import datetime

def fetch_markets(api_key: str):
    """
    همه مارکت‌ها رو از API میاره
    """
    url = "https://api.wallex.ir/hector/web/v1/markets"
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("result", {}).get("markets", [])

def save_first_30_to_csv(api_key: str, filename: str = "markets.csv"):
    markets = fetch_markets(api_key)

    unique_assets = {}
    for market in markets:
        en_base = market.get("en_base_asset")
        if en_base and en_base not in unique_assets:
            unique_assets[en_base] = market
        if len(unique_assets) >= 30:
            break

    all_keys = set()
    for features in unique_assets.values():
        all_keys.update(features.keys())
    all_keys = sorted(all_keys)

    fieldnames = ["date", "time", "en_base_asset"] + all_keys

    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for en_base, features in unique_assets.items():
            now = datetime.now()
            row = {
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M:%S"),
                "en_base_asset": en_base
            }
            row.update(features)
            writer.writerow(row)

    print(f"✅ داده جدید ذخیره شد ({len(unique_assets)} ردیف).")

if __name__ == "__main__":
    my_api_key = "YOUR_API_KEY_HERE"

    while True:
        save_first_30_to_csv(my_api_key, "markets.csv")
        print("⏳ منتظر ۵ دقیقه بعدی...")
        time.sleep(300)  
