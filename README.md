# Retail dataset generator

## Overview

The goal of this project is to create a dataset of online retail transactions for demonstrating streaming data applications.  
This project starts with a real dataset of online transactions (see credits section below).  The data volumes in the original dataset are quite low and would not be very interesting for a streaming demo - you may have to wait for a long time to see a transaction.  For a streaming demo, it is more interesting if user's can see transactions happening every second, therefore, the original data is modified.  

The main [processing logic](./create_dataset.py) is:

- remove records with missing customer ids
- remove records with negative quantities (see [here](https://github.com/ibm-cloud-streaming-retail-demo/dataset-generator/issues/1) for a better approach)
- add a line item number for each record
- create a copy of the entire data
  - The first copy represents UK timezone
    - add a suffix to the invoice number of `1`
  - The second copy repsenets US timezone
    - add a suffix to the invoice number of `2`
    - shift the invoice datetime by 12 hours

The original dataset transactions span one year (1st Dec 2010 to 9th Dec 2011).  Note that we haven't changed the date of the record. We can change the date of the record when we load the record (e.g. into Kafka).  We do this at time of load because we want to set the date to the load date rather than the date at which the dataset is created.

## Creating the dataset

The dataset can be created with:

- local python
- dockerised python

### Local Python

```
# First grab this project
git clone https://github.com/ibm-cloud-streaming-retail-demo/dataset-generator
cd dataset-generator

# setup a virtualenv (optional but recommended)
cd dataset-generator
virtualenv venv
source venv/bin/activate

# setup the python libary dependency
$ pip3 install -r requirements.txt

# download and prepare the dataset
$ python3 create_dataset.py
```

### Dockerised Python

```
docker run -it --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3 bash -c "pip3 install -r requirements.txt && python3 create_dataset.py"
```

Note that the processing is performed entirely in memory.

# Original dataset

Some example records from the original dataset:

InvoiceNo | StockCode | Description | Quantity | InvoiceDate | UnitPrice | CustomerID | Country
-- | -- | -- | -- | -- | -- | -- | --
536365	| 85123A	| WHITE HANGING HEART T-LIGHT HOLDER	|  6	| 01/12/2010 08:26	| 2.55	| 17850	|  United Kingdom
536365	| 71053	| WHITE METAL LANTERN	| 6	| 01/12/2010 08:26	| 3.39	| 17850	| United Kingdom
536365	| 84406B	| CREAM CUPID HEARTS COAT HANGER	| 8	| 01/12/2010 08:26	| 2.75	| 17850	| United Kingdom

The full dataset is available here: http://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx

## Credits

Daqing Chen, Sai Liang Sain, and Kun Guo, Data mining for the online retail industry: A case study of RFM model-based customer segmentation using data mining, Journal of Database Marketing and Customer Strategy Management, Vol. 19, No. 3, pp. 197â€“208, 2012 (Published online before print: 27 August 2012. doi: 10.1057/dbm.2012.17).
