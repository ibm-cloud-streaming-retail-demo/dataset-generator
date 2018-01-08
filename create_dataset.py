#!/usr/bin/env python

ONLINE_RETAIL_XLSX  = 'OnlineRetail.xlsx'
ONLINE_RETAIL_CSV   = 'OnlineRetail.csv'
ONLINE_RETAIL_JSON  = 'OnlineRetail.json'

def download_spreadsheet():
    print('Starting download_spreadsheet() ...')

    # support python 2 and 3
    try:
        # python 3
        import urllib.request as urlrequest
    except ImportError:
        import urllib as urlrequest

    source_url = "http://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
    urlrequest.urlretrieve(source_url, ONLINE_RETAIL_XLSX)

    print('Finished download_spreadsheet() ...')
    
def create_csv():
    print('Starting create_csv() ...')
    import pandas as pd
    import datetime

    df = pd.read_excel(ONLINE_RETAIL_XLSX, sheetname='Online Retail')

    # remove nan customer IDs
    df = df[pd.notnull(df['CustomerID'])] 
    df['CustomerID'] = df['CustomerID'].astype(int)

    # remove negative quantities - this also removes non-numeric InvoiceNo's
    df = df.ix[df['Quantity'] > 0] 

    # Add a line item number for each item in an invoice
    df['LineNo'] = df.groupby(['InvoiceNo']).cumcount()+1

    # the dataset starts at approx 6am and finishes at approx 10pm
    # we want to data to span 24 hours so that it is interesting for UK and American
    # demos.  We may also want to do a similar thing for Asia Pacific, perhaps 
    # we should have three regions and an 8 hour difference between each region?

    df_UK_Day = df.copy()
    df_US_Day = df.copy()

    df_UK_Day['InvoiceNo'] = (df_UK_Day['InvoiceNo'].astype('str') + '1').astype(int)
    df_US_Day['InvoiceNo'] = (df_US_Day['InvoiceNo'].astype('str') + '2').astype(int)

    # Let's approximate the overall time difference between US and UK as 12 hours
    df_US_Day['InvoiceDate'] = df_US_Day['InvoiceDate'] + datetime.timedelta(hours=12)

    df = pd.concat([df_UK_Day, df_US_Day])

    # Sort dataframe
    df['InvoiceTime'] = pd.DatetimeIndex(df['InvoiceDate']).time
    df.sort_values(by=['InvoiceTime', 'InvoiceNo'], inplace=True)

    # finally save
    df.to_csv(ONLINE_RETAIL_CSV, index=False, encoding='utf-8', header=False)
    df.to_json('OnlineRetail.json', orient='records', lines=True, date_format='epoch', date_unit='ms')
    print('Finished create_csv() ...')

def compress_files():
    print('Starting compress_files() ...')
    import gzip
    import shutil
    
    for filename in [ONLINE_RETAIL_XLSX, ONLINE_RETAIL_CSV, ONLINE_RETAIL_JSON]:
        with open(filename, 'rb') as f_in, gzip.open(filename + '.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print('Finished compress_files() ...')

def remove_file(filename):
    import os
    try:
        os.remove(filename)
    except OSError:
        pass

if __name__ == "__main__":
    for filename in [ONLINE_RETAIL_XLSX, ONLINE_RETAIL_CSV, ONLINE_RETAIL_JSON]:
        remove_file(filename)

    for filename in [ONLINE_RETAIL_XLSX + '.gz', ONLINE_RETAIL_CSV + '.gz', ONLINE_RETAIL_JSON + '.gz']:
        remove_file(filename)
        
    download_spreadsheet()
    create_csv()
    compress_files()
