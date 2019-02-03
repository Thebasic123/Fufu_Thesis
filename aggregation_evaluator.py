import aggregation_methods as am
import blindIterativeFiltering as it

#change target stock string to evaluate different stock recommendation performance
targetStockStr = 'GOOG'

print('Currently testing the performance of',targetStockStr,'recommendation evaluation\n')

#get data for target stock
print('Getting data for aggregation')
training_data_file = 'processed_data/'+targetStockStr+'/'+targetStockStr+'_training_data.txt'
testing_data_file = 'processed_data/'+targetStockStr+'/'+targetStockStr+'_testing_data.txt'
print('Getting training data matrix')
f = open(training_data_file)
lines = f.readlines()
training_data_matrix = eval(lines[3])
f.close()
print('Getting testing data matrix')
f = open(testing_data_file)
lines = f.readlines()
testing_data_matrix = eval(lines[4])
print('Getting analyst ids')
analyst_ids = eval(lines[1])
print('Getting price changes list')
price_changes = []
for line in lines[7:]:
	price_changes.append(float(line.split(' ')[2].split('=')[0]))
f.close()
print('Got all the data\n')

#calculate trustworthiness through IF
print('Calculating',targetStockStr,'IF weights')
it.changeThreshold(0.1)
IF_result = it.iterativeFiltering(training_data_matrix)
print('IF Result',IF_result)
print('Calculated',targetStockStr,'IF weights\n')

#aggregate testing data
print('Finding aggregated recommendation through 3 different methods')
print('Calculating normal average aggregation')
average_aggregation_result = am.average_aggregate(testing_data_matrix)
print('Calculating IF aggregation')
IF_aggregation_result = am.IF_aggregate(IF_result,testing_data_matrix)
print('Calculating historical correction aggregation')
history_corrected_aggregation_result = am.history_corrected_aggregate(analyst_ids,testing_data_matrix)
print('Got all the aggregated data\n')

#evaluate performance of three aggregation strategies with two methods
print('Evaluate aggregated',targetStockStr,'stock recommendation performance')
print('======================================')
print('======================================\n')
#purely weighted evaluation, since the aggregated value is from -1 to 1, we use 
#aggregated value times by the price change to get the profit margin
print('Running Purely weighted evaluation strategy')
print('======================================')
curr_sum = 0
for i in range(len(price_changes)):
	if average_aggregation_result[i] > 0:
		curr_sum += (price_changes[i] - 1) * average_aggregation_result[i]
	elif average_aggregation_result[i] < 0:
		curr_sum += (1 - price_changes[i]) * average_aggregation_result[i]
print('average aggregation under Purely weighted evaluation strategy has performance score',curr_sum)
curr_sum = 0
for i in range(len(price_changes)):
	if IF_aggregation_result[i] > 0:
		curr_sum += (price_changes[i] - 1) * IF_aggregation_result[i]
	elif IF_aggregation_result[i] < 0:
		curr_sum += (1 - price_changes[i]) * IF_aggregation_result[i]
print('IF aggregation under Purely weighted evaluation strategy has performance score',curr_sum)
curr_sum = 0
for i in range(len(price_changes)):
	if history_corrected_aggregation_result[i] > 0:
		curr_sum += (price_changes[i] - 1) * history_corrected_aggregation_result[i]
	elif history_corrected_aggregation_result[i] < 0:
		curr_sum += (1 - price_changes[i]) * history_corrected_aggregation_result[i]
print('historical correctness aggregation under Purely weighted evaluation strategy has performance score',curr_sum)
print('======================================\n')
#we set a range of value be the rejection region, once the data lies in the rejection region
# we don't do anything, we regard it as hold, as otherwise, we treat it as buy or sell
#For example, if the rejection region is (-0.2,0.2),then if we get a value of -0.1, we will treat it
#as hold, if we get a value of -0.3, we will treat it as sell.
print('Running Rejection region evaluation strategy')
print('======================================')
#try out different rejection region ranges
rejection_regions = [0.2,0.3,0.4,0.5]
for rejection_region in rejection_regions:
	print('Current rejection region [{},{}]'.format(rejection_region*-1,rejection_region))
	curr_sum = 0
	for i in range(len(price_changes)):
		if average_aggregation_result[i] > rejection_region:
			curr_sum += (price_changes[i] - 1)
		elif average_aggregation_result[i] < (-1*rejection_region):
			curr_sum += (1 - price_changes[i])
	print('average aggregation under Rejection region evaluation strategy has performance score',curr_sum)
	curr_sum = 0
	for i in range(len(price_changes)):
		if IF_aggregation_result[i] > rejection_region:
			curr_sum += (price_changes[i] - 1)
		elif IF_aggregation_result[i] < (-1*rejection_region):
			curr_sum += (1 - price_changes[i])
	print('IF aggregation under Rejection region evaluation strategy has performance score',curr_sum)
	curr_sum = 0
	for i in range(len(price_changes)):
		if history_corrected_aggregation_result[i] > rejection_region:
			curr_sum += (price_changes[i] - 1)
		elif history_corrected_aggregation_result[i] < (-1*rejection_region):
			curr_sum += (1 - price_changes[i])
	print('historical correctness aggregation under Rejection region evaluation strategy has performance score',curr_sum)
	print('======================================')