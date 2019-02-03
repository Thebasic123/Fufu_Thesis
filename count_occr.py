import csv 

file_name = "WRDS_us_stock_recommendation.csv"
with open(file_name) as fp:
    lines = fp.readlines()
analyst_d = dict()
stock_d = dict()
counter = 1
for row in lines:
	curr_row = row.split(',')
	if curr_row[5] in analyst_d:
		analyst_d[curr_row[5]] += 1
	else:
		analyst_d[curr_row[5]] = 1
	if curr_row[2] in stock_d:
		stock_d[curr_row[2]] += 1
	else:
		stock_d[curr_row[2]] = 1
	print(counter)
	counter += 1
print("there are",len(analyst_d.keys()),"analysts")
print("averge number of recommendations made by an analyst is",counter/len(analyst_d.keys()))
print("there are",len(stock_d.keys()),"stocks")

# for key, value in sorted(stock_d.iteritems(), key=lambda (k,v): (v,k)):
# 	print "%s: %s" % (key, value)
