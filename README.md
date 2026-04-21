# AI Agent Phan Tich Kinh Te Vi Mo

Agent tu dong theo doi va phan tich tinh hinh kinh te vi mo the gioi va Viet Nam, su dung Claude AI de tao bao cao chuyen sau.

## Tinh nang

- Thu thap du lieu kinh te tu **World Bank API** (GDP, lam phat, that nghiep, no cong...)
- Lay **ty gia hoi doai** thoi gian thuc (ExchangeRate API)
- Scrape **tin tuc kinh te** tu Reuters, VnEconomy, CafeF
- Phan tich chuyen sau bang **Claude AI** (Anthropic)
- Tao **bao cao Markdown** co cau truc ro rang

## Cai dat

```bash
# 1. Clone repo
git clone https://github.com/TuanNguyen-CEO/cowork-claude-1.git
cd cowork-claude-1

# 2. Cai dependencies
pip install -r requirements.txt

# 3. Cau hinh API key
cp .env.example .env
# Mo .env va dien ANTHROPIC_API_KEY

# 4. Chay agent
python main.py
```

## Cau truc du an

```
.
├── main.py                    # Diem khoi chay
├── config.py                  # Cau hinh (quoc gia, chi so, nguon tin)
├── data_fetchers/
│   ├── __init__.py
│   ├── worldbank.py           # World Bank API fetcher
│   └── news_scraper.py        # Scrape tin tuc
├── analyzers/
│   ├── __init__.py
│   └── claude_analyzer.py     # Phan tich voi Claude AI
├── reporters/
│   ├── __init__.py
│   └── report_generator.py    # Tao bao cao Markdown
├── reports/                   # Bao cao duoc luu tai day
├── requirements.txt
└── .env.example
```

## Nguon du lieu

| Nguon | Loai | Chi phi |
|-------|------|---------|
| World Bank API | GDP, lam phat, that nghiep... | Mien phi |
| ExchangeRate API | Ty gia hoi doai | Mien phi |
| Reuters RSS | Tin tuc quoc te | Mien phi |
| VnEconomy | Tin tuc Viet Nam | Mien phi |
| CafeF | Tin tuc tai chinh VN | Mien phi |

## Tuy chinh

Chinh sua `config.py` de:
- Them/bot quoc gia theo doi
- Them/bot chi so kinh te
- Thay doi nguon tin tuc
- Chon model Claude khac

## Yeu cau

- Python 3.9+
- Anthropic API Key (lay tai [console.anthropic.com](https://console.anthropic.com))
