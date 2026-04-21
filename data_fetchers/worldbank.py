"""
Lay du lieu kinh te vi mo tu World Bank API (mien phi, khong can API key)
"""

import requests
import time
from config import COUNTRIES, INDICATORS


class WorldBankFetcher:
    BASE_URL = "https://api.worldbank.org/v2"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "MacroAgent/1.0"})

    def fetch_indicator(self, country_code: str, indicator_code: str, years: int = 3) -> list:
        url = f"{self.BASE_URL}/country/{country_code}/indicator/{indicator_code}"
        params = {"format": "json", "per_page": years, "mrv": years}
        try:
            resp = self.session.get(url, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            if len(data) >= 2 and data[1]:
                return [
                    {
                        "year": item.get("date"),
                        "value": item.get("value"),
                        "country": item.get("country", {}).get("value"),
                    }
                    for item in data[1]
                    if item.get("value") is not None
                ]
        except Exception as e:
            print(f"   Warning: Loi lay {indicator_code} cho {country_code}: {e}")
        return []

    def fetch_all(self) -> dict:
        result = {}
        for country_code, country_name in COUNTRIES.items():
            result[country_code] = {"name": country_name, "indicators": {}}
            for indicator_code, indicator_name in INDICATORS.items():
                data = self.fetch_indicator(country_code, indicator_code)
                if data:
                    result[country_code]["indicators"][indicator_name] = data
                time.sleep(0.3)
        result["exchange_rates"] = self._fetch_exchange_rates()
        return result

    def _fetch_exchange_rates(self) -> dict:
        try:
            resp = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10)
            data = resp.json()
            rates = data.get("rates", {})
            return {
                "USD_VND": rates.get("VND"),
                "USD_CNY": rates.get("CNY"),
                "USD_JPY": rates.get("JPY"),
                "USD_EUR": rates.get("EUR"),
                "USD_GBP": rates.get("GBP"),
                "updated": data.get("time_last_update_utc"),
            }
        except Exception as e:
            print(f"   Warning: Loi lay ty gia: {e}")
            return {}
