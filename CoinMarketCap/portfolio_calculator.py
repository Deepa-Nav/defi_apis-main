import requests
from prettytable import PrettyTable



symbols = []
quantity = []
buy_prices = []
symbol_ids = [0] * len(symbols)
with open("/Users/deepa/JST/defi_apis-main/CoinMarketCap/portfolio.txt", "r") as file:  
    for line in file.readlines()[1:]:
        line = line.split(',')
        symbols.append(line[0])
        quantity.append(float(line[1]))
        buy_prices.append(float(line[2]))

    # print(symbols)
    # print(quantity)
    # print(buy_prices)
listing_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
listings_data = requests.get(listing_url, headers={"X-CMC_PRO_API_KEY": "58160cd4-a7be-414c-8671-7828e8b7a2d9"}).json()['data']

for currency in listings_data:
    if currency['name'] in symbols:
        symbol_ids[symbols.index(currency['name'])] = currency['id']

table = PrettyTable(['Name', 'Quantity','Buy_Price','Profit', 'Change (1h)', 'Change (24h)', 'Change (7d)'])
for i in range(len(symbols)):
    temp_api = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id={str(symbol_ids[i])}"
    temp_data = requests.get(temp_api, headers={"X-CMC_PRO_API_KEY": "58160cd4-a7be-414c-8671-7828e8b7a2d9"}).json()
    current_price = temp_data['data']['quote']['USD']['price']
    current_price = float(current_price)
    change_1h = temp_data['data']['quote']['USD']['percent_change_1h']
    change_24h = temp_data['data']['quote']['USD']['percent_change_24h']
    change_7d = temp_data['data']['quote']['USD']['percent_change_7d']
    profit = round((current_price / buy_prices[i]) * 100 - 100,2)
    table.add_row([symbols[i], quantity[i], buy_prices[i], profit, change_1h, change_24h, change_7d])
print(table)
