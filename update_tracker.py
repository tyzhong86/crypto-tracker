import os
import subprocess
import requests

# ==========================================
# 📊 配置中心：在这里锁定你的核心资产
# ==========================================
PORTFOLIO = {
    "BTC":  {"qty": 0.15, "avg_buy": 55000, "apy": 0.0},
    "WLD":  {"qty": 2500.0, "avg_buy": 0.45, "apy": 5.2},
    "AXS":  {"qty": 25.22, "avg_buy": 1.20, "apy": 1.62},
    "BNB":  {"qty": 0.00002, "avg_buy": 580, "apy": 0.17},
}

def get_live_prices():
    """从币安公开 API 批量获取实时价格"""
    print("🔄 正在从交易所获取最新价格...")
    url = "https://api.binance.com/api/v3/ticker/price"
    try:
        response = requests.get(url).json()
        prices = {item['symbol']: float(item['price']) for item in response if 'USDT' in item['symbol']}
        # 兼容一些基础稳定币或者特殊对
        prices["USDC"] = 1.0
        return prices
    except Exception as e:
        print(f"❌ 获取价格失败: {e}")
        return {}

def auto_push_to_github():
    """核心爽点：数据更新后，自动打包推送到云端触发 Netlify 更新"""
    print("📤 正在启动本地 Git 自动化管道...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "chore: 机器人全自动同步最新资产账目"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("🎉 [KPI 达成] 数据已成功上云，Netlify 正在全网秒级同步中！")
    except Exception as e:
        print(f"⚠️ Git 自动推送失败，可能无新数据变动。")

if __name__ == "__main__":
    # 测试价格获取
    market_prices = get_live_prices()
    if market_prices:
        print(f"✅ 成功抓取到 BTC 当前价: ${market_prices.get('BTCUSDT')}")
        # 接下来我们会用 Python 动态重写 HTML...
        # auto_push_to_github()import os
import re
import ccxt
import requests
from dotenv import load_module, load_dotenv

# 加载本地保密凭证
load_dotenv()

def get_exchange_balances():
    """全自动去交易所抓取你的真实持仓数量"""
    print("🔑 正在安全验证本地钥匙，连线交易所...")
    
    # 初始化交易所实例
    exchange_id = os.getenv("EXCHANGE_TYPE", "bitget").lower()
    if not os.getenv("API_KEY"):
        print("❌ 未在 .env 中检测到 API Key，请先填写！")
        return {}

    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({
        'apiKey': os.getenv("API_KEY"),
        'secret': os.getenv("API_SECRET"),
        'password': os.getenv("API_PASSWORD"), # Bitget/OKX 通常需要
        'enableRateLimit': True,
    })

    try:
        # 抓取现货真实余额
        balance = exchange.fetch_balance()
        positions = {}
        
        # 只筛选出数量大于 0 的资产
        for coin, amount in balance['total'].items():
            if amount > 0.0001:  # 过滤掉碎屑小币
                positions[coin] = amount
        
        print(f"✅ 成功从交易所对齐资产数量: {positions}")
        return positions
    except Exception as e:
        print(f"❌ 交易所连线失败: {e}")
        return {}

def update_html_panel(balances):
    """【黑科技】自动读取并重写你的 HTML 面板，对齐最新持仓"""
    html_file = "gemini-code-1782892791229.html" # 锁定你当前的面板文件名
    
    if not os.path.exists(html_file):
        print(f"❌ 找不到 HTML 文件: {html_file}")
        return

    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # TODO: 接下来我们会用正则或者 BeautifulSoup 
    # 动态把刚才得到的 balances 数量注入到 HTML 表格的 QTY 字段里
    print("🎯 持仓数据已在本地注入内存，等待下一步混合渲染...")

if __name__ == "__main__":
    real_positions = get_exchange_balances()
    if real_positions:
        update_html_panel(real_positions)
        