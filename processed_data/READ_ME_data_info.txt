all the data and data matrix are made under the data set in 2012 and 2013.

interested stocks:
The top 10 most popular stocks in terms of the number of recommendation
DB 1590
HPQ 1675
PXD 1738
GOOG 1738
AFL 1836
MA 1855
PCP 1874
AMZN 1895
PCLN 2054
AAPL 2521

Each stock has all the processed data files in a folder named by the stock name

In each folder for stock data, we have the folliwng files:
1.xxxx_training_data.txt #contains data for IF training,genearted by stock_training_data_extractor.py
2.xxxx_test_data.txt #contains test data for trading days in 2014,genearted by stock_testing_data_extractor.py

Data Format in each training data file:
1.number of total recommendations
2.training data matrix for current stock
3.info of training data matrix
4.number of recommendations made by each analysts(sorted)
5.analysts ids which are the column index in the data matrix
6.dates used by training data matrix
7.final trustworthiness for each analyst for the current stock

Data Format in each testing data file (in order to auto-read data matrix, we put data matrix on a fixed line number): 
1.analysts ids which are the column index in the data matrix(same one with training data file)
2.testing data matrix (same format with training data matrix,-1 means short,0 means hold,1 means long)
3. dates of trading days used by testing data set ,number of recommendation on that day and their price change 
(for price change we use the format in the raw data set,#price in 5 trading days / current price#)

Data in analyst_historial_performance.txt:
1. performance score of each analyst (sorted)
2. Python dict format of performance score of each analyst

