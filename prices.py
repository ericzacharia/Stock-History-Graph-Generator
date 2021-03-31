'''
Command Line: python prices.py StockSymbol
Example: python prices.py AAPL
'''

import csv
import json
import requests
import sys
from matplotlib import pyplot as plt

symbol = sys.argv[1]
output_size = 'full'
function = 'TIME_SERIES_DAILY'
API_KEY = 'QJXHD8NZP1YZ53E2'


def get_csv_data():  # I haven't figured out how to use csv files yet.
    csv_url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize={output_size}" \
              f"&apikey={API_KEY}&datatype=csv"
    response = requests.get(csv_url)
    contents = response.text
    # Option to use csv.DictReader to get a list of dictionaries instead of a list of lists.
    contents_list = list(csv.reader(contents.splitlines()))
    print(contents_list)

    # Create a text file from the response data we get from the API
    with open("prices_csv.txt", "w") as file:
        file.write(response.text)


def get_json_data():
    with open(f"prices.{symbol}.txt", "w") as file:
        json_url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize={output_size}" \
                  f"&apikey={API_KEY}&datatype=json"  # default data type is json
        response = requests.get(json_url)
        data = json.loads(response.text)
        date_plot = []
        price_plot = []

        for day in range(len(data["Time Series (Daily)"])):
            price = float(data["Time Series (Daily)"][list(data["Time Series (Daily)"])[day]]["4. close"])
            date = list(data["Time Series (Daily)"])[day]
            price_plot.insert(0, price)
            date_plot.insert(0, date)
            stock = f'{date}  ${price:.2f}'
            file.write(stock)
            file.write('\n')

    # Creates a text file from the response data we get from an API
    with open(f"prices_json.txt", "w") as file:
        file.write(response.text)

    plt.plot(date_plot, price_plot, label=f'{symbol}')
    plt.xscale('linear')
    plt.title(f'Stock Price for {symbol} for the Past 20+ Years')
    plt.legend()
    plt.show()
    plt.savefig(f'{symbol}.png')


# get_csv_data()
get_json_data()

print(f"Wrote historical price data for {symbol} to file prices.{symbol}.txt")
