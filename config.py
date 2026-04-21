"""
Cau hinh trung tam cho AI Agent kinh te vi mo
"""

# Danh sach quoc gia theo doi
COUNTRIES = {
    "WLD": "The gioi",
    "VNM": "Viet Nam",
    "USA": "Hoa Ky",
    "CHN": "Trung Quoc",
    "JPN": "Nhat Ban",
    "DEU": "Duc",
    "GBR": "Anh",
    "SGP": "Singapore",
    "THA": "Thai Lan",
}

# Cac chi so kinh te can theo doi (World Bank API codes)
INDICATORS = {
    "NY.GDP.MKTP.KD.ZG": "Tang truong GDP (%)",
    "FP.CPI.TOTL.ZG":    "Lam phat CPI (%)",
    "SL.UEM.TOTL.ZS":    "Ty le that nghiep (%)",
    "NE.EXP.GNFS.ZS":    "Xuat khau (% GDP)",
    "NE.IMP.GNFS.ZS":    "Nhap khau (% GDP)",
    "GC.DOD.TOTL.GD.ZS": "No cong (% GDP)",
    "NY.GDP.PCAP.CD":    "GDP binh quan dau nguoi (USD)",
    "FM.LBL.BMNY.GD.ZS": "Cung tien M2 (% GDP)",
}

# Nguon tin tuc
NEWS_SOURCES = {
    "vneconomy":   "https://vneconomy.vn/kinh-te-the-gioi.htm",
    "cafef":       "https://cafef.vn/vi-mo-dau-tu.chn",
    "reuters_rss": "https://feeds.reuters.com/reuters/businessNews",
}

# Cai dat bao cao
REPORT_DIR = "reports"
REPORT_LANGUAGE = "vi"

# Model Claude
CLAUDE_MODEL = "claude-opus-4-6"
MAX_TOKENS = 4096
