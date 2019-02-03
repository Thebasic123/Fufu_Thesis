from datetime import date, timedelta

#we need to change target stock variable to extract different stock information
targetStockStr = 'PCLN'
#analyst id dict should be changed with target stock, we can find it in training data file
targetStockAnalyst_ids = {'AllCap': 0, 'Big_2000': 1, 'Cap_1B+': 2, 'Big_1500': 3, 'Big_1000': 4, 'Big_100': 5, 'Cap_5B+': 6, 'Big_750': 7, 'S9-Services': 8, 'SP500': 9, 'Big_500': 10, 'S7-Fin(exAllETF)': 11, 'Big_250': 12, 'Very_High_Liquidity': 13}
# Datetime stuff for iterating through files
#data in testing data set are from 2014
start = date(2014, 1, 1)
end = date(2014, 12, 31)
delta = end - start

analysts = {}
popularStocks = {}
targetStockAnalysts = {}
targetStockDays = {}
targetStockActionDict = {}
targetStockPriceDict = {}

for i in range(delta.days + 1):
    date = start + timedelta(i)
    folder = 'sNewsListWResults3yr/sNewsListWResults'+str(date.year)+'/'
    filename = folder + 'sNewsListWResults' + str(date.year) + (str(date.month) if date.month > 9 else '0' + str(date.month)) + (str(date.day) if date.day > 9 else '0' + str(date.day)) + '.txt'

    try:
        #if a share has already been reviewed by a analyst in the current file, we won't double count it
        visited_share_by_analyst = dict()
        for line in open(filename, 'r'):
            line = line.strip()
            if line != '':
                data = line.split(', ')
                analyst = data[0].split(' ')[-1]
                if not analyst.endswith('_LONG_SHORT_F.pdf'):
                    continue
                size = analyst.split('_')[-4]
                if size != '20':
                    continue
                analyst = '_'.join(analyst.split('_')[:-4])
                if analyst not in visited_share_by_analyst:
                    visited_share_by_analyst[analyst] = dict()
                action = data[1]
                recommendations = data[2:-1]
                recommendedStocks = []
                for r in recommendations:
                    if r.split(' ')[0] == targetStockStr:
                        if date not in targetStockPriceDict:
                            targetStockPriceDict[str(date)] = r.split(' ')[1]+r.split(' ')[2]
                    if r.split(' ')[0] not in visited_share_by_analyst[analyst]:
                        #mark share has been visited by the current analyst
                        visited_share_by_analyst[analyst][r.split(' ')[0]] = 1
                        recommendedStocks.append(r.split(' ')[0])
                        if r.split(' ')[0] in popularStocks:
                            popularStocks[r.split(' ')[0]] += 1
                        else:
                            popularStocks[r.split(' ')[0]] = 1
                performance = data[-1].split(' ')[-1]
                if analyst in analysts:
                    analysts[analyst].append((i, size, action, recommendedStocks))
                else:
                    analysts[analyst] = [(i, size, action, recommendedStocks)]
                if analyst in targetStockAnalysts:
                    targetStockAnalysts[analyst] += recommendedStocks.count(targetStockStr)
                else:
                    targetStockAnalysts[analyst] = recommendedStocks.count(targetStockStr)
                if recommendedStocks.count(targetStockStr) > 0:
                    if str(date) in targetStockDays:
                        targetStockDays[str(date)] += recommendedStocks.count(targetStockStr)
                    else:
                        targetStockDays[str(date)] = recommendedStocks.count(targetStockStr)
                    if analyst in targetStockActionDict:
                        targetStockActionDict[analyst][str(date)] = action
                    else:
                        targetStockActionDict[analyst] = dict()
                        targetStockActionDict[analyst][str(date)] = action

    except:
        print('No entry', date)

    print(str(i)+'/365')

targetStockTargetDays = []

for i in sorted(targetStockDays.keys(), key = lambda x: targetStockDays[x]):
    #get all the targeted days
    if targetStockDays[i] >= 8:
        targetStockTargetDays.append(i)
        print(i, targetStockDays[i],targetStockPriceDict[i])

targetStockDataMatrix = []

#generate Iterative filtering training data matrix for current stock
for i in range(len(targetStockTargetDays)):
    curr_data_row = [0] * len(targetStockAnalyst_ids)
    for j in sorted(targetStockAnalyst_ids.keys(), key = lambda x: targetStockAnalyst_ids[x]):
        if j not in targetStockActionDict:
            curr_data_row[targetStockAnalyst_ids[j]] = 0
            continue
        if targetStockTargetDays[i] in targetStockActionDict[j]:
            if targetStockActionDict[j][targetStockTargetDays[i]] == 'L':
                curr_data_row[targetStockAnalyst_ids[j]] = 1
            elif targetStockActionDict[j][targetStockTargetDays[i]] == 'S':
                curr_data_row[targetStockAnalyst_ids[j]] = -1
        else:
            #since there is no action data available, we use hold
            curr_data_row[targetStockAnalyst_ids[j]] = 0
    targetStockDataMatrix.append(curr_data_row)

#show testing data matrix
print(targetStockDataMatrix)
