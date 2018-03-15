#!/usr/bin/env python

ONLINE_RETAIL_XLSX  = 'OnlineRetail.xlsx'
ONLINE_RETAIL_CSV   = 'OnlineRetail.csv'
ONLINE_RETAIL_JSON  = 'OnlineRetail.json'
ONLINE_RETAIL_CUSTOMERS = 'OnlineRetailCustomers.csv'

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

    # add a suffix to the invoice number so that UK and US records have a unique id
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

def create_customers():
    print('Starting create_customers() ...')
    import pandas as pd
    import datetime
    from faker import Faker
    import numpy as np

    # Load data
    df_data_1 = pd.read_csv(ONLINE_RETAIL_CSV, header=None, usecols=[6])
    # Get unique customer IDs
    df_data_1 = df_data_1[6].unique()

    # initiate faker
    fake = Faker('en_GB')

    # create lists of names and addresses
    names = [ fake.name() for i in range(0,len(df_data_1)) ]
    addresses = [ fake.address().replace("\n", " ") for i in range(0, len(df_data_1)) ]

    # build df
    df = pd.DataFrame({'CustomerID': df_data_1, 'Name': names, 'Address': addresses})
    df['validFrom'] = datetime.datetime.now()
    # df['validTo'] = np.NaN

    # Sort dataframe
    df.sort_values(by=['CustomerID'], inplace=True)

    # finally save
    df.to_csv(ONLINE_RETAIL_CUSTOMERS, index=False, encoding='utf-8', header=False)
    print('Finished create_customers() ...')

def compress_files():
    print('Starting compress_files() ...')
    import gzip
    import shutil

    for filename in [ONLINE_RETAIL_XLSX, ONLINE_RETAIL_CSV, ONLINE_RETAIL_JSON, ONLINE_RETAIL_CUSTOMERS]:
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
    for filename in [ONLINE_RETAIL_XLSX, ONLINE_RETAIL_CSV, ONLINE_RETAIL_JSON, ONLINE_RETAIL_CUSTOMERS]:
        remove_file(filename)

    for filename in [ONLINE_RETAIL_XLSX + '.gz', ONLINE_RETAIL_CSV + '.gz', ONLINE_RETAIL_JSON + '.gz', ONLINE_RETAIL_CUSTOMERS + '.gz']:
        remove_file(filename)

    download_spreadsheet()
    create_csv()
    create_customers()
    compress_files()
