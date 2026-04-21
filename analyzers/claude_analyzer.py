"""
Phan tich kinh te vi mo su dung Claude AI (Anthropic)
"""

import anthropic
from config import CLAUDE_MODEL, MAX_TOKENS


class ClaudeAnalyzer:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def analyze(self, economic_data: dict, news_data: dict) -> dict:
        econ_summary = self._summarize_economic_data(economic_data)
        news_summary = self._summarize_news(news_data)

        prompt = f"""Ban la chuyen gia kinh te vi mo hang dau. Hay phan tich toan dien tinh hinh kinh te hien tai dua tren du lieu sau:

## DU LIEU KINH TE VI MO:
{econ_summary}

## TIN TUC KINH TE MOI NHAT:
{news_summary}

Hay tao mot ban phan tich day du theo cau truc sau (viet bang tieng Viet):

1. **TONG QUAN KINH TE THE GIOI**
   - Tinh trang tang truong toan cau
   - Xu huong lam phat va lai suat
   - Rui ro dia chinh tri va thuong mai

2. **PHAN TICH CAC NEN KINH TE LON**
   - Hoa Ky
   - Trung Quoc
   - Nhat Ban va chau Au

3. **PHAN TICH KINH TE VIET NAM**
   - Tang truong GDP va dong luc
   - Lam phat va chinh sach tien te
   - Xuat nhap khau va FDI
   - Ty gia VND

4. **TAC DONG DOI VOI VIET NAM**
   - Co hoi tu boi canh toan cau
   - Thach thuc va rui ro
   - Nganh nao huong loi / chiu ap luc

5. **DU BAO VA KHUYEN NGHI**
   - Trien vong ngan han (3-6 thang)
   - Trien vong dai han (1-2 nam)
   - Khuyen nghi chinh sach

Hay phan tich cu the, dua tren so lieu thuc te va dua ra nhan dinh chuyen sau."""

        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "full_analysis": response.content[0].text,
            "highlights": self._extract_highlights(economic_data),
            "model_used": CLAUDE_MODEL,
        }

    def _summarize_economic_data(self, data: dict) -> str:
        lines = []
        for code, info in data.items():
            if code == "exchange_rates":
                rates = info
                lines.append("\nTY GIA HIEN TAI:")
                if rates.get("USD_VND"):
                    lines.append(f"  USD/VND: {rates['USD_VND']:,.0f}")
                lines.append(f"  USD/CNY: {rates.get('USD_CNY', 'N/A')}")
                lines.append(f"  USD/JPY: {rates.get('USD_JPY', 'N/A')}")
                lines.append(f"  USD/EUR: {rates.get('USD_EUR', 'N/A')}")
                continue
            country_name = info.get("name", code)
            lines.append(f"\n{country_name} ({code}):")
            for ind_name, values in info.get("indicators", {}).items():
                if values:
                    v = values[0]
                    val = v.get("value")
                    year = v.get("year")
                    if val is not None:
                        lines.append(f"  - {ind_name}: {val:.2f} ({year})")
        return "\n".join(lines)

    def _summarize_news(self, news_data: dict) -> str:
        lines = []
        for source, articles in news_data.items():
            if articles:
                lines.append(f"\n[{source.upper()}]")
                for art in articles[:5]:
                    lines.append(f"  * {art['title']}")
        return "\n".join(lines)

    def _extract_highlights(self, data: dict) -> dict:
        def get_latest(indicators, key):
            vals = indicators.get(key, [])
            return vals[0].get("value") if vals else None
        vnm = data.get("VNM", {}).get("indicators", {})
        wld = data.get("WLD", {}).get("indicators", {})
        return {
            "vietnam_gdp_growth": get_latest(vnm, "Tang truong GDP (%)"),
            "vietnam_inflation":  get_latest(vnm, "Lam phat CPI (%)"),
            "world_gdp_growth":   get_latest(wld, "Tang truong GDP (%)"),
            "world_inflation":    get_latest(wld, "Lam phat CPI (%)"),
            "exchange_rates":     data.get("exchange_rates", {}),
        }
