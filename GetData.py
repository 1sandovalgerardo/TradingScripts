import pandas as pd
import pandas_datareader.data as web
import os
import argparse 
import datetime 
import logging
import csv

def create_log(debug):
    if debug:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

        fileHandler = logging.FileHandler('log_get_data_script.log', 'w')
        fileHandler.setLevel(logging.INFO)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

        shellHandler = logging.StreamHandler()
        shellHandler.setLevel(logging.WARNING)
        logger.addHandler(shellHandler)
        logging.debug('logging established')

    else:
        pass

def parser_gs():
    logging.info('parser_gs() called')
    parser = argparse.ArgumentParser(description='Get Stock Price History')
    parser.add_argument('--path',
                        dest='path',
                        type=str,
                        help='Enter the path you with the data to be saved to.')
    args = parser.parse_args()
    return args
    
def check_parser(parser):
    logging.info('check_parser() called')
    parser = parser_gs()
    path = parser.path

def start_end_dates(startDate=None, endDate=None):
    # if start and end dates passed, set value to this
    logging.info('start_end_dates() called')
    if startDate:
        logging.info('start date supplied: {startDate}')
        year, month, day = startDate
        startDate = datetime.date(year, month, day)
    else:
        startDate = datetime.date(2000, 1, 1)
    if endDate:
        logging.info('end date supplied: {endDate}')
        year, month, day = endDate
        endDate = datetime.date(year, month, day-1)
    else:
        endDate = datetime.date.today()
    return (startDate, endDate)
    

def download_price_history_OHLC(ticker, startDate, endDate):
    logging.info(f'download_price_history_OHLC() called on {ticker}')
    ticker = ticker.upper()
    filePath = f'{ticker}.csv'
    try:
        stockData = web.DataReader('SPY', 'yahoo', startDate, endDate)
    except Exception as error:
        logging.error(f'Ticker: {ticker} not valid')
        print(error)
        print(f'Ticker: {ticker} not valid')
    save_data(stockData, ticker)

def save_data(dataToSave, ticker):
    logging.info('save_data() called')
    if type(dataToSave)==type(pd.DataFrame()):
        fileName = f'{ticker}.csv'
        dataToSave.to_csv(fileName, header=True)
    else:
        logging.error(f'data for ticker: {ticker} in incorrect data type.')

def move_to_dir(dirToSave):
    logging.info('move_to_dir() called.')
    if dirToSave==None:
        return None
    if os.path.exists(dirToSave):
        os.chdir(dirToSave)
    else:
        os.makedirs(dirToSave)
        os.chdir(dirToSave)

def _get_tickers(tickerPath='/home/gerardo/Documents/Trading/Scripts/tickers_spy_holdings.csv'):
    logging.info('_get_tickers() called')
    tickers = []
    with open(tickerPath, 'r') as tickerFile:
        reader = csv.reader(tickerFile)
        for t in reader:
            tickers.append(t[0])
    return tickers

def main():
    create_log(True) 
    logging.info('main() called')
    Parser = parser_gs()
    saveTo = Parser.path
    move_to_dir(saveTo)
    print(os.getcwd())
    startDate, endDate = start_end_dates(startDate=(2020, 1, 1))
    tickers = _get_tickers()
    startDate, endDate = start_end_dates()
    for sym in tickers:
        download_price_history_OHLC(sym, startDate, endDate)



if __name__=='__main__':
    main()
    

    

