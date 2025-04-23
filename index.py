from APIConnect.APIConnect import APIConnect
api_key = ""  # Your API key here
api_secret = "" # Your API secret here
request_id = "" # Your request ID here which can be obtained from the login response

settings_file = "" # Path to your settings file 
api = APIConnect(api_key, api_secret, request_id,True,settings_file) 


from constants.exchange import ExchangeEnum
from constants.order_type import OrderTypeEnum
from constants.product_code import ProductCodeENum
from constants.duration import DurationEnum
from constants.action import ActionEnum
import csv
def get_exchange_token_and_trading_symbol(symbol_name, exchange):
    csv_file_path = ""  # Path to your CSV file which is should be in the same directory with folder name instruments and file name instruments.csv , copy the absolute path here
    # Example: csv_file_path = "C:/path/to/your/instruments.csv"
    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["symbolname"].strip().upper() == symbol_name.upper() and row["exchange"].strip().upper() == exchange.upper():
                    exchange_token = row["exchangetoken"]
                    trading_symbol = row["tradingsymbol"]
                    return {"Exchange Token": exchange_token, "Trading Symbol": trading_symbol}
        print(f"Symbol '{symbol_name}' with exchange '{exchange}' not found in the CSV.")
        return None
    except FileNotFoundError:
        print(f"CSV file not found at path: {csv_file_path}")
        return None
    except KeyError as e:
        print(f"Missing column in CSV: {e}")
        return None
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None



def placebuyorder(symbol_name,qty,limit_price,exchange):
    print(" calling placebuyorder")
    exchange_token_and_trading_symbol = get_exchange_token_and_trading_symbol(symbol_name, exchange)
    print(" exchange_token_and_trading_symbol",exchange_token_and_trading_symbol)
    if exchange_token_and_trading_symbol:
        streaming_symbol = exchange_token_and_trading_symbol["Exchange Token"]
        trading_symbol = exchange_token_and_trading_symbol["Trading Symbol"]
        exch = exchange.upper()
        if exch == "NSE":
            exchange = ExchangeEnum.NSE
        elif exch == "BSE":
            exchange = ExchangeEnum.BSE
        else:
            print("Invalid exchange. Only NSE and BSE are supported.")
            return None
        try:
            order = api.PlaceTrade(
                Trading_Symbol=trading_symbol,
                Exchange= exchange,
                Action=ActionEnum.BUY,
                Duration=DurationEnum.DAY,
                Order_Type=OrderTypeEnum.LIMIT,
                Quantity=qty,
                Streaming_Symbol=streaming_symbol,
                Limit_Price=limit_price,
                Disclosed_Quantity="0",
                TriggerPrice="0",
                ProductCode=ProductCodeENum.CNC
            )
            return order
        except Exception as e:
            print(f"Error placing order: {e}")
            return None
                
    else:
        print("Failed to get exchange token and trading symbol.")
        return None


def placesellorder(symbol_name,qty,limit_price,exchange):
    exchange_token_and_trading_symbol = get_exchange_token_and_trading_symbol(symbol_name, exchange)
    if exchange_token_and_trading_symbol:
        streaming_symbol = exchange_token_and_trading_symbol["Exchange Token"]
        trading_symbol = exchange_token_and_trading_symbol["Trading Symbol"]
        exch = exchange.upper()
        if exch == "NSE":
            exchange = ExchangeEnum.NSE
        elif exch == "BSE":
            exchange = ExchangeEnum.BSE
        else:
            print("Invalid exchange. Only NSE and BSE are supported.")
            return None
        try:
            order = api.PlaceTrade(
                Trading_Symbol=trading_symbol,
                Exchange= exchange,
                Action=ActionEnum.SELL,
                Duration=DurationEnum.DAY,
                Order_Type=OrderTypeEnum.LIMIT,
                Quantity=qty,
                Streaming_Symbol=streaming_symbol,
                Limit_Price=limit_price,
                Disclosed_Quantity="0",
                TriggerPrice="0",
                ProductCode=ProductCodeENum.CNC
            )
            return order
        except Exception as e:
            print(f"Error placing order: {e}")
            return None
        
        
    else:
        print("Failed to get exchange token and trading symbol.")
        return None

import json
def get_holdings():
    try:
        holdings = api.Holdings()
        
        # Parse the response as JSON
        holdings_data = json.loads(holdings)
        
       
        filtered_holdings = [
            {
                "Company Name": holding["cpName"].strip(),
                "Shares Held": holding["totalQty"],
                "Price": holding["ltp"]
            }
            for holding in holdings_data["eq"]["data"]["rmsHdg"]
        ]
        return filtered_holdings
    except json.JSONDecodeError:
        print("Error decoding JSON response from API.")
        return None
    except KeyError as e:
        print(f"Missing key in holdings data: {e}")
        return None
    except Exception as e:
        print(f"Error fetching holdings: {e}")
        return None

# Example usage
# print(get_holdings())

# print(placesellorder("RELIANCE", 1, 1200, "NSE"))