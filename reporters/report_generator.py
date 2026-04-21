"""
Tao bao cao phan tich kinh te vi mo dang Markdown
"""

import os
from datetime import datetime
from config import REPORT_DIR


class ReportGenerator:
    def __init__(self):
        os.makedirs(REPORT_DIR, exist_ok=True)

    def generate(self, analysis: dict, economic_data: dict, news_data: dict) -> str:
        now = datetime.now()
        filename = f"macro_report_{now.strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(REPORT_DIR, filename)
        content = self._build_report(now, analysis, economic_data, news_data)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath

    def _build_report(self, now, analysis, economic_data, news_data) -> str:
        highlights = analysis.get("highlights", {})
        full_analysis = analysis.get("full_analysis", "")

        def fmt(val, suffix="%"):
            return f"{val:.2f}{suffix}" if val is not None else "N/A"

        vn_gdp  = highlights.get("vietnam_gdp_growth")
        vn_inf  = highlights.get("vietnam_inflation")
        wld_gdp = highlights.get("world_gdp_growth")
        wld_inf = highlights.get("world_inflation")
        rates   = highlights.get("exchange_rates", {})

        report = f"""# BAO CAO KINH TE VI MO
**Ngay tao:** {now.strftime('%d/%m/%Y %H:%M:%S')}
**Tao boi:** AI Agent - Claude {analysis.get('model_used', '')}

---

## SO LIEU NOI BAT

| Chi so | The gioi | Viet Nam |
|--------|----------|----------|
| Tang truong GDP | {fmt(wld_gdp)} | {fmt(vn_gdp)} |
| Lam phat CPI | {fmt(wld_inf)} | {fmt(vn_inf)} |

"""
        if rates:
            usd_vnd = rates.get("USD_VND")
            report += "### Ty gia hoi doai\n"
            report += f"- USD/VND: {usd_vnd:,.0f}\n" if usd_vnd else "- USD/VND: N/A\n"
            report += f"- USD/CNY: {rates.get('USD_CNY', 'N/A')}\n"
            report += f"- USD/JPY: {rates.get('USD_JPY', 'N/A')}\n"
            report += f"- USD/EUR: {rates.get('USD_EUR', 'N/A')}\n"

        report += f"""
---

## PHAN TICH CHI TIET (Claude AI)

{full_analysis}

---

## TIN TUC TONG HOP

"""
        for source, articles in news_data.items():
            if articles:
                report += f"### {source.upper()}\n"
                for art in articles[:8]:
                    report += f"- [{art['title']}]({art.get('link', '#')})\n"
                report += "\n"

        report += f"""
---

## DU LIEU KINH TE RAW

"""
        for code, info in economic_data.items():
            if code == "exchange_rates":
                continue
            country_name = info.get("name", code)
            indicators = info.get("indicators", {})
            if indicators:
                report += f"### {country_name} ({code})\n\n"
                report += "| Chi so | Gia tri | Nam |\n|--------|---------|-----|\n"
                for ind_name, values in indicators.items():
                    if values:
                        v = values[0]
                        val = v.get("value")
                        year = v.get("year")
                        report += f"| {ind_name} | {val:.2f} | {year} |\n" if val else f"| {ind_name} | N/A | {year} |\n"
                report += "\n"

        report += f"\n---\n*Bao cao duoc tao tu dong boi AI Agent | {now.strftime('%Y-%m-%d %H:%M:%S')}*\n"
        return report
