# Retail dataset generator

The goal of this project is to create a dataset of online retail transactions for demonstrating streaming data applications.  Some example records:

InvoiceNo | StockCode | Description | Quantity | InvoiceDate | UnitPrice | CustomerID | Country
-- | -- | -- | -- | -- | -- | -- | --
536365	| 85123A	| WHITE HANGING HEART T-LIGHT HOLDER	|  6	| 01/12/2010 08:26	| 2.55	| 17850	|  United Kingdom
536365	| 71053	| WHITE METAL LANTERN	6	01/12/2010 08:26	| 3.39	| 17850	| United Kingdom
536365	| 84406B	| CREAM CUPID HEARTS COAT HANGER	| 8	| 01/12/2010 08:26	| 2.75	| 17850	| United Kingdom


This project starts with a real dataset of online transactions (see credits section below).  The data volumes in the original dataset are quite low and would not be very interesting for a streaming demo - you may have to wait for a long time to see a transaction.  For a streaming demo, it is more interesting if user's can see transactions happening every second, therefore, the original data is modified.  

The original dataset transactions span one year (1st Dec 2010 to 9th Dec 2011).  The main processing logic is to change all of the transaction dates so that they all happen in the same day.  Note that this approach simulates 0.5M transactions/day.

The dataset can be created with:

```
# setup python libaries
$ pip install -r requirements.txt
```
and then 

```
# download and prepare the dataset
$ python prepare.py
```

Note that the processing is performed entirely in memory.

# Credits for the original data

Daqing Chen, Sai Liang Sain, and Kun Guo, Data mining for the online retail industry: A case study of RFM model-based customer segmentation using data mining, Journal of Database Marketing and Customer Strategy Management, Vol. 19, No. 3, pp. 197â€“208, 2012 (Published online before print: 27 August 2012. doi: 10.1057/dbm.2012.17).
