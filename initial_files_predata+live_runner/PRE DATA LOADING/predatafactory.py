# ============================================
# ⭐ PRE-LOADING ENGINE: NSE + MT5 (FINAL) ⭐
# ============================================

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from datetime import datetime, timedelta
import MetaTrader5 as mt5


# ============================
# STEP 1 — GET ETF DATA (NSE)
# ============================

def get_etf_data(symbol="GOLDIETF"):
    driver = webdriver.Chrome()
    url = f"https://www.nseindia.com/get-quotes/equity?symbol={symbol}"

    driver.get(url)
    driver.maximize_window()

    time.sleep(5)

    inav = driver.find_element(By.XPATH, '//*[@id="dashboard"]/div/div/div[2]/div/div[2]/div[5]/div/div/div[2]').text
    close_price = driver.find_element(By.XPATH, '//*[@id="midBody"]/div[2]/div[2]/div/div[1]/div/div[1]/span[2]').text
    raw_date = driver.find_element(By.XPATH, '//*[@id="midBody"]/div[2]/div[1]/div[2]/div[2]/div').text

    print("\n--- NSE DATA EXTRACTED ---")
    print("Raw INAV        :", inav)
    print("Raw LTP         :", close_price)
    print("Raw NSE Date    :", raw_date)

    driver.quit()
    return inav, close_price, raw_date


# =======================================
# STEP 2 — CONVERT NSE DATE INTO YYYY-MM-DD
# =======================================

def parse_nse_date(raw):
    """
    Converts a date like:  '28-Nov-2025 16:00:00'
    into:                  '2025-11-28'
    """
    dt = datetime.strptime(raw, "%d-%b-%Y %H:%M:%S")
    return dt.date().isoformat()   # YYYY-MM-DD


# ============================================
# STEP 3 — FETCH GOLD XAUUSD @ 15:30 IST (MT5)
# ============================================

SYMBOL = "XAUUSD"
TARGET_HOUR = 15        # 15:30 IST
TARGET_MIN = 30


def get_gold_1530(india_date_str):
    if not mt5.initialize():
        raise RuntimeError(f"MT5 init failed: {mt5.last_error()}")

    try:
        y, m, d = map(int, india_date_str.split("-"))

        # XAUUSD at 15:30 IST (MT5 is using IST on your system)
        anchor = datetime(y, m, d, TARGET_HOUR, TARGET_MIN)

        start = anchor - timedelta(minutes=20)
        end = anchor + timedelta(minutes=5)

        rates = mt5.copy_rates_range(
            SYMBOL,
            mt5.TIMEFRAME_M1,
            start,
            end
        )

        if rates is None or len(rates) == 0:
            raise RuntimeError("No XAUUSD data found in MT5")

        anchor_ts = int(anchor.timestamp())
        best = None

        for r in rates:
            if int(r["time"]) <= anchor_ts:
                if best is None or int(r["time"]) > int(best["time"]):
                    best = r

        if best is None:
            raise RuntimeError("No 15:30 IST gold candle found")

        price = float(best["close"])
        candle_time = datetime.fromtimestamp(int(best["time"]))

        print("\n--- MT5 GOLD DATA ---")
        print("MT5 Candle Time :", candle_time)
        print("XAUUSD @ 15:30  :", price)

        return price, candle_time

    finally:
        mt5.shutdown()


# ============================
# STEP 4 — MERGE EVERYTHING
# ============================

if __name__ == "__main__":

    # ✔ Step 1: Get ETF data from NSE
    inav, close_price, raw_date = get_etf_data("GOLDIETF")

    # ✔ Step 2: Convert “28-Nov-2025 16:00:00” → “2025-11-28”
    india_date = parse_nse_date(raw_date)

    print("\n--- DATE PARSED ---")
    print("Parsed Indian Date :", india_date)

    # ✔ Step 3: Fetch XAUUSD @ 15:30 IST for that date
    gold_price, candle_time = get_gold_1530(india_date)

    # ✔ Step 4: Final PRELOAD DATA OUTPUT
    preload_packet = {
        "date": india_date,
        "ETF_inav": inav,
        "ETF_ltp": close_price,
        "Gold_1530_IST": gold_price,
        "Gold_candle_time": str(candle_time)
    }

    print("\n========================")
    print("⭐ PRELOADED DATA PACKET ⭐")
    print("========================")
    print(preload_packet)
