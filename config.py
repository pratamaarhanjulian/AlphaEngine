"""
AUREA PRIME ELITE - Configuration Module
=========================================
Load configuration from environment variables
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ============================================
# TELEGRAM BOT CONFIGURATION
# ============================================
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))
CHAT_SUPPORT = os.getenv("CHAT_SUPPORT", "AurEA_PRIME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")

# ============================================
# VPS CONFIGURATION
# ============================================
VPS_IP = os.getenv("VPS_IP", "")
VPS_PORT = int(os.getenv("VPS_PORT", "1207"))
VPS_USERNAME = os.getenv("VPS_USERNAME", "Administrator")
VPS_PASSWORD = os.getenv("VPS_PASSWORD", "")

# ============================================
# GITHUB CONFIGURATION
# ============================================
GITHUB_REPO = os.getenv("GITHUB_REPO", "https://github.com/pratamaarhanjulian/AlphaEngine")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")

# ============================================
# PAYMENT INFORMATION
# ============================================
BANK_BRI = os.getenv("BANK_BRI", "")
BANK_JAGO = os.getenv("BANK_JAGO", "")
GOPAY_NUMBER = os.getenv("GOPAY_NUMBER", "")
ACCOUNT_NAME = os.getenv("ACCOUNT_NAME", "")

# ============================================
# AI SERVICES
# ============================================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "qwen/qwen3-4b:free")

# ============================================
# NEWS CALENDAR API
# ============================================
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")

# ============================================
# SYSTEM CONFIGURATION
# ============================================
WEBSOCKET_HOST = os.getenv("WEBSOCKET_HOST", "0.0.0.0")
WEBSOCKET_PORT = int(os.getenv("WEBSOCKET_PORT", "8080"))

# Paths
BASE_DIR = Path(__file__).parent
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "database" / "aurea.db"))
MODELS_PATH = os.getenv("MODELS_PATH", str(BASE_DIR / "models"))
LOGS_PATH = os.getenv("LOGS_PATH", str(BASE_DIR / "logs"))

# ============================================
# TRADING CONFIGURATION
# ============================================
DEFAULT_RISK_PERCENT = float(os.getenv("DEFAULT_RISK_PERCENT", "1.0"))
DEFAULT_LOT_MODE = os.getenv("DEFAULT_LOT_MODE", "AUTO")
DEFAULT_FIXED_LOT = float(os.getenv("DEFAULT_FIXED_LOT", "0.01"))
DEFAULT_RR_MODE = os.getenv("DEFAULT_RR_MODE", "AUTO")
DEFAULT_FIXED_RR = float(os.getenv("DEFAULT_FIXED_RR", "2.0"))
MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", "85.0"))

# ============================================
# DEBUG MODE
# ============================================
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ============================================
# TIER DEFINITIONS
# ============================================
TIERS = {
    "FREE": {
        "name": "FREE",
        "emoji": "🆓",
        "daily_signals": 5,
        "auto_notification": False,
        "auto_execution": False,
        "ea_token": False,
        "news_alerts": False,
        "pairs": ["XAUUSD"]
    },
    "PREMIUM": {
        "name": "PREMIUM",
        "emoji": "💎",
        "daily_signals": -1,
        "auto_notification": True,
        "auto_execution": False,
        "ea_token": False,
        "news_alerts": True,
        "pairs": []
    },
    "SUPER": {
        "name": "SUPER",
        "emoji": "⚡",
        "daily_signals": -1,
        "auto_notification": True,
        "auto_execution": True,
        "ea_token": True,
        "news_alerts": True,
        "pairs": []
    },
    "SUPREME": {
        "name": "SUPREME",
        "emoji": "👑",
        "daily_signals": -1,
        "auto_notification": True,
        "auto_execution": True,
        "ea_token": True,
        "news_alerts": True,
        "pairs": ["ALL"]
    }
}

# ============================================
# PRICING (in IDR)
# ============================================
PRICING = {
    "XAU": {
        "name": "XAU Only",
        "emoji": "🟡",
        "pairs": ["XAUUSD"],
        "premium": {
            "1M": 49000,
            "3M": 119000,
            "6M": 299000,
            "12M": 499000,
            "LIFETIME": 999000
        }
    },
    "BTC": {
        "name": "BTC Only",
        "emoji": "🔵",
        "pairs": ["BTCUSD"],
        "premium": {
            "1M": 39000,
            "3M": 99000,
            "6M": 179000,
            "12M": 319000,
            "LIFETIME": 799000
        }
    },
    "ALL": {
        "name": "All Pairs",
        "emoji": "❤️",
        "pairs": ["XAUUSD", "BTCUSD", "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "NZDUSD"],
        "premium": {
            "1M": 99000,
            "3M": 219000,
            "6M": 389000,
            "12M": 699000,
            "LIFETIME": 1499000
        }
    },
    "SUPREME": {
        "name": "SUPREME",
        "emoji": "👑",
        "pairs": ["ALL"],
        "price": 2999000
    }
}

def calculate_super_price(package: str, duration: str) -> int:
    """Calculate SUPER tier price based on PREMIUM price"""
    if package not in PRICING or duration not in PRICING[package].get("premium", {}):
        return 0
    
    premium_price = PRICING[package]["premium"][duration]
    days_map = {"1M": 30, "3M": 90, "6M": 180, "12M": 365, "LIFETIME": 3650}
    days = days_map.get(duration, 30)
    
    return int((premium_price / 30) * days * 0.6)

ALL_PAIRS = [
    "XAUUSD", "BTCUSD", "EURUSD", "GBPUSD", 
    "USDJPY", "AUDUSD", "USDCAD", "NZDUSD",
    "USDCHF", "EURGBP", "EURJPY", "GBPJPY"
]

def validate_config():
    """Validate required configuration"""
    errors = []
    if not BOT_TOKEN:
        errors.append("BOT_TOKEN is required")
    if not ADMIN_CHAT_ID:
        errors.append("ADMIN_CHAT_ID is required")
    return errors

if __name__ == "__main__":
    errors = validate_config()
    if errors:
        print("Configuration errors:")
        for e in errors:
            print(f"  - {e}")
    else:
        print("Configuration OK!")
