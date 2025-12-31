# xauusd_12pm_server.py

from datetime import datetime, timedelta
import MetaTrader5 as mt5

SYMBOL = "XAUUSD"          # if your broker uses GOLD, change to GOLD

SERVER_TARGET_HOUR = 15    # FIXED: 12:00 server time ALWAYS
SERVER_TARGET_MINUTE = 30


def get_xauusd_at_noon_mt5(india_date_str: str):
    """
    Fetches the XAUUSD price at the MT5 server time 12:00 
    for the given Indian calendar date.
    """

    if not mt5.initialize():
        raise RuntimeError(f"MT5 init failed: {mt5.last_error()}")

    try:
        y, m, d = map(int, india_date_str.split("-"))

        # FIXED TARGET: 12:00 server time
        anchor_server = datetime(y, m, d, SERVER_TARGET_HOUR, SERVER_TARGET_MINUTE)

        # Fetch a window around 12:00
        start = anchor_server - timedelta(minutes=20)
        end   = anchor_server + timedelta(minutes=5)

        rates = mt5.copy_rates_range(
            SYMBOL,
            mt5.TIMEFRAME_M1,
            start,
            end
        )

        if rates is None or len(rates) == 0:
            raise RuntimeError(f"No MT5 data found for {SYMBOL}")

        anchor_ts = int(anchor_server.timestamp())

        # find last candle ≤ 12:00
        best = None
        for r in rates:
            if int(r["time"]) <= anchor_ts:
                if best is None or int(r["time"]) > int(best["time"]):
                    best = r

        if best is None:
            raise RuntimeError("No candle at/before 12:00 server time")

        price = float(best["close"])
        candle_server_dt = datetime.fromtimestamp(int(best["time"]))

        return price, candle_server_dt

    finally:
        mt5.shutdown()


if __name__ == "__main__":
    india_date = "2025-11-28"   # TODAY

    price, t_server = get_xauusd_at_noon_mt5(india_date)

    print("==== XAUUSD ETF-Close Price Extraction ====")
    print(f"Indian date        : {india_date}")
    print(f"Server candle time : {t_server} (should be 12:00 or just before)")
    print(f"XAUUSD price       : {price}")
