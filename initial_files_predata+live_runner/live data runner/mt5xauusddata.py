# =========================================
#  LIVE XAUUSD HIGH-FREQUENCY TICK STREAM
#  MT5 Python API — Aditya's HFT Gold Feed
# =========================================

import MetaTrader5 as mt5
from datetime import datetime
import time

SYMBOL = "XAUUSD"  # change to GOLD if your broker uses that name


def init_mt5():
    if not mt5.initialize():
        raise RuntimeError(f"MT5 init failed: {mt5.last_error()}")
    print("MT5 Connected.")


def live_ticks():
    print("\n🔥 LIVE XAUUSD FEED STARTED (tick-by-tick) 🔥")
    print("Press CTRL + C to stop.\n")

    last_tick_time = 0

    while True:
        # Get latest 1 tick
        ticks = mt5.copy_ticks_from(SYMBOL, datetime.now(), 1, mt5.COPY_TICKS_ALL)

        if ticks is not None and len(ticks) > 0:
            tick = ticks[-1]

            # avoid repeating same tick
            if tick['time'] != last_tick_time:
                last_tick_time = tick['time']

                bid = tick['bid']
                ask = tick['ask']
                volume = tick['volume']
                ts = datetime.fromtimestamp(tick['time'])

                print(
                    f"Time: {ts} | "
                    f"Bid: {bid:.2f} | "
                    f"Ask: {ask:.2f} | "
                    f"Spread: {(ask - bid):.2f} | "
                    f"Volume: {volume}"
                )

        # loop speed — lower = faster (but don’t use 0)
        time.sleep(0.001)    # **1 millisecond refresh**


if __name__ == "__main__":
    init_mt5()

    try:
        live_ticks()

    except KeyboardInterrupt:
        print("\nStopped by user.")

    finally:
        mt5.shutdown()
        print("MT5 Disconnected.")
