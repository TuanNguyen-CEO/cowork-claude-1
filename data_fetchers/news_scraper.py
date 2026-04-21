"""
Thu thap tin tuc kinh te tu cac nguon RSS va trang web
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from bs4 import BeautifulSoup
from config import NEWS_SOURCES


class NewsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; MacroAgent/1.0)"
        })

    def fetch_latest_news(self, max_per_source: int = 10) -> dict:
        news = {}
        print("     -> Reuters RSS...")
        news["reuters"] = self._fetch_rss(NEWS_SOURCES["reuters_rss"], max_per_source)
        print("     -> VnEconomy...")
        news["vneconomy"] = self._fetch_vneconomy(max_per_source)
        print("     -> CafeF...")
        news["cafef"] = self._fetch_cafef(max_per_source)
        return news

    def _fetch_rss(self, url: str, limit: int) -> list:
        articles = []
        try:
            resp = self.session.get(url, timeout=15)
            root = ET.fromstring(resp.content)
            items = root.findall(".//item")[:limit]
            for item in items:
                title = item.findtext("title", "").strip()
                link  = item.findtext("link", "").strip()
                desc  = item.findtext("description", "").strip()
                date  = item.findtext("pubDate", "").strip()
                if desc:
                    soup = BeautifulSoup(desc, "html.parser")
                    desc = soup.get_text(separator=" ").strip()
                if title:
                    articles.append({
                        "title": title, "link": link,
                        "summary": desc[:300] if desc else "",
                        "date": date, "source": "Reuters",
                    })
        except Exception as e:
            print(f"     Warning: Loi Reuters RSS: {e}")
        return articles

    def _fetch_vneconomy(self, limit: int) -> list:
        articles = []
        try:
            resp = self.session.get(NEWS_SOURCES["vneconomy"], timeout=15)
            soup = BeautifulSoup(resp.content, "html.parser")
            items = soup.select("h3.story__heading a, h2.story__heading a")[:limit]
            for item in items:
                title = item.get_text(strip=True)
                link  = item.get("href", "")
                if link and not link.startswith("http"):
                    link = "https://vneconomy.vn" + link
                if title:
                    articles.append({
                        "title": title, "link": link, "summary": "",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "source": "VnEconomy",
                    })
        except Exception as e:
            print(f"     Warning: Loi VnEconomy: {e}")
        return articles

    def _fetch_cafef(self, limit: int) -> list:
        articles = []
        try:
            resp = self.session.get(NEWS_SOURCES["cafef"], timeout=15)
            soup = BeautifulSoup(resp.content, "html.parser")
            items = soup.select("h3.title a, .knswli-title a")[:limit]
            for item in items:
                title = item.get_text(strip=True)
                link  = item.get("href", "")
                if link and not link.startswith("http"):
                    link = "https://cafef.vn" + link
                if title:
                    articles.append({
                        "title": title, "link": link, "summary": "",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "source": "CafeF",
                    })
        except Exception as e:
            print(f"     Warning: Loi CafeF: {e}")
        return articles
