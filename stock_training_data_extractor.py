from datetime import date, timedelta

#we need to change target stock variable to extract different stock information
targetStockStr = 'HPQ'

# Datetime stuff for iterating through files
start = date(2012, 1, 3)
end = date(2013, 12, 31)
delta = end - start

analysts = {}
popularStocks = {}
targetStockAnalysts = {}
targetStockDays = {}
targetStockActionDict = {}

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

    print(str(i)+'/730')

targetStockTargetDays = []
targetStockAnalyst_ids = {}
counter = 0
for i in sorted(targetStockAnalysts.keys(), key = lambda x: targetStockAnalysts[x]):
    #if current analyst makes more recommendation on the particular share more than the average
    if targetStockAnalysts[i] > popularStocks[targetStockStr] / len(analysts):
        targetStockAnalyst_ids[i] = counter
        counter += 1
        print(i,targetStockAnalysts[i])

for i in sorted(targetStockDays.keys(), key = lambda x: targetStockDays[x]):
    #get all the targeted days
    if targetStockDays[i] >= 8:
        targetStockTargetDays.append(i)
        print(i, targetStockDays[i])

targetStockDataMatrix = []

#generate Iterative filtering training data matrix for current stock
for i in range(len(targetStockTargetDays)):
    curr_data_row = [0] * len(targetStockAnalyst_ids)
    for j in sorted(targetStockAnalyst_ids.keys(), key = lambda x: targetStockAnalyst_ids[x]):
        if targetStockTargetDays[i] in targetStockActionDict[j]:
            if targetStockActionDict[j][targetStockTargetDays[i]] == 'L':
                curr_data_row[targetStockAnalyst_ids[j]] = 1
            elif targetStockActionDict[j][targetStockTargetDays[i]] == 'S':
                curr_data_row[targetStockAnalyst_ids[j]] = -1
        else:
            #since there is no action data available, we use hold
            curr_data_row[targetStockAnalyst_ids[j]] = 0
    targetStockDataMatrix.append(curr_data_row)

zero_count = 0
one_count = 0
negative_count = 0
for i in range(len(targetStockDataMatrix)):
    for j in range(len(targetStockDataMatrix[i])):
        if targetStockDataMatrix[i][j] == 0:
            zero_count += 1
        elif targetStockDataMatrix[i][j] == 1:
            one_count += 1
        elif targetStockDataMatrix[i][j] == -1:
            negative_count += 1
#show analysts ids
print(targetStockAnalyst_ids)
#show the data matrix
print(str(targetStockDataMatrix))
print('\n')
print('Data matrix info:')
print('total number of elements is',len(targetStockDataMatrix)*len(targetStockDataMatrix[0]))
print('total number of value zero is',zero_count)
print('total number of value one is',one_count)
print('total number of value negative one is',negative_count)