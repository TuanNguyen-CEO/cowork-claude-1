"""
AI Agent theo doi & phan tich kinh te vi mo the gioi va Viet Nam
Tac gia: TuanNguyen-CEO
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from data_fetchers.worldbank import WorldBankFetcher
from data_fetchers.news_scraper import NewsScraper
from analyzers.claude_analyzer import ClaudeAnalyzer
from reporters.report_generator import ReportGenerator


def run_agent():
    print("=" * 60)
    print("AI AGENT KINH TE VI MO")
    print(f"Khoi dong luc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Loi: Thieu ANTHROPIC_API_KEY trong file .env")
        sys.exit(1)

    print("\n[1/4] Dang thu thap du lieu kinh te vi mo tu World Bank...")
    wb_fetcher = WorldBankFetcher()
    economic_data = wb_fetcher.fetch_all()
    print(f"   Thu thap duoc du lieu cua {len(economic_data)} quoc gia/khu vuc")

    print("\n[2/4] Dang thu thap tin tuc kinh te moi nhat...")
    news_scraper = NewsScraper()
    news_data = news_scraper.fetch_latest_news()
    total_news = sum(len(v) for v in news_data.values())
    print(f"   Thu thap duoc {total_news} bai tin tu cac nguon")

    print("\n[3/4] Dang phan tich voi Claude AI...")
    analyzer = ClaudeAnalyzer(api_key=api_key)
    analysis = analyzer.analyze(economic_data, news_data)
    print("   Phan tich hoan tat")

    print("\n[4/4] Dang tao bao cao...")
    reporter = ReportGenerator()
    report_path = reporter.generate(analysis, economic_data, news_data)
    print(f"   Bao cao luu tai: {report_path}")

    print("\n" + "=" * 60)
    print("HOAN THANH! Agent da chay xong.")
    print("=" * 60)
    return report_path


if __name__ == "__main__":
    run_agent()
