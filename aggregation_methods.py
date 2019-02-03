#standard aggregation strategy, all the analysts have the same weight
def average_aggregate(testing_data_matrix):
	result = []
	for row in testing_data_matrix:
		curr_sum = 0
		for elem in row:
			curr_sum += elem
		result.append(curr_sum/len(row))
	return result
#aggregation strategy with IF result, all the analysts have the weight of their normalized trustworthiness
def IF_aggregate(IF_result,testing_data_matrix):
	result = []
	for row in testing_data_matrix:
		curr_sum = 0
		for i in range(len(row)):
			curr_sum += row[i]*IF_result[i]
		result.append(curr_sum)
	return result
#aggregation strategy with the help of historical data, we use the historical performance score
#we need to pass in the analyst id dict we are using
def history_corrected_aggregate(analyst_ids,testing_data_matrix):
	#we get the analyst performance score dict from processed data folder
	analyst_scores = {'Big_100': 0.6409999999999982, 'Big_500': 0.6980000000000005, 'Big_750': 0.6840000000000018, 'SPSm600': 0.5529999999999993, 'S2-CapGood': 0.9480000000000004, 'S4-Cons-Cyc': 0.06699999999999862, 'S6-Energy': 0.9269999999999994, 'S11-Transp': 1.5069999999999997, 'S12-Util': 0.9309999999999995, 'AllCap': 2.599999999999995, 'Cap_2-250m': 4.556, 'Cap_250-1000m': 1.1089999999999987, 'Cap_20-1000m': 3.866000000000003, 'Cap_1B+': 1.177999999999998, 'Cap_5B+': 0.7720000000000011, 'Big_250': 0.729000000000001, 'Big_1000': 0.7989999999999982, 'Big_1500': 1.1389999999999993, 'Big_2000': 0.8269999999999992, 'SP500': 1.2680000000000002, 'SPMid400': 0.6639999999999993, 'S1-BasicInd': 1.9789999999999965, 'S7-Fin': 1.5430000000000008, 'S7-Fin(exAllETF)': 0.8809999999999981, 'S8-Health': 1.6680000000000004, 'S9-Services': 1.0110000000000003, 'S10-Tech': 1.6239999999999988, 'SIC-ETFs-ext-FOF': -0.36700000000000055, 'SICs-AllTech': 1.6099999999999977, 'SIC-1311-OGOps': 0.10999999999999999, 'SIC-3674-SemiCond': 1.4010000000000018, 'SICs-Insurance': 1.0170000000000012, 'SICs-Banks': 0.5739999999999968, 'SIC-6798-REOps': 0.796, 'Cap_1-5B': 0.9339999999999999, 'Low_Liquidity': 2.9809999999999945, 'Mid_Liquidity': 0.9960000000000013, 'High_Liquidity': 0.8740000000000011, 'Very_High_Liquidity': 0.5129999999999962}
	#get a normalized weight
	weights = []
	total_weight = 0
	for analyst in analyst_ids:
		total_weight += analyst_scores[analyst]
	#insert all the weights in their index order
	for i in sorted(analyst_ids.keys(), key = lambda x: analyst_ids[x]):
		weights.append(analyst_scores[i]/total_weight)
	#find the final result
	result = []
	for row in testing_data_matrix:
		curr_sum = 0
		for i in range(len(row)):
			curr_sum += row[i]*weights[i]
		result.append(curr_sum)
	return result