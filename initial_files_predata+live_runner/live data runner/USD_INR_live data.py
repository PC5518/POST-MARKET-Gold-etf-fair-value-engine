import yfinance as yf
import time

def get_usd_inr_once():
    ticker = yf.Ticker("USDINR=X")
    data = ticker.history(period="1d", interval="1m")
    if data.empty:
        return None
    return float(data['Close'][-1])

def stream_usd_inr():
    print("Streaming live USD/INR... (Ctrl + C to stop)")
    while True:
        try:
            price = get_usd_inr_once()
            if price is not None:
                print("USD/INR:", price)
            else:
                print("Error fetching data.")
            
            time.sleep(2)  # fetch every 2 seconds
            
        except KeyboardInterrupt:
            print("\nStopped by user.")
            break
        except Exception as e:
            print("Error:", e)
            time.sleep(2)

stream_usd_inr()
