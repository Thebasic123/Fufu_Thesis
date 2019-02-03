from datetime import date, timedelta

# Datetime stuff for iterating through files
start = date(2012, 1, 3)
end = date(2013, 12, 31)
delta = end - start

analysts = {}
popularStocks = {}

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

    except:
        print('No entry', date)

    print(str(i)+'/730')

print('TOTAL:', len(analysts.keys()))

print(sorted(analysts.keys()))

for i in sorted(popularStocks.keys(), key = lambda x: popularStocks[x]):
   print(i, popularStocks[i])

print(len(popularStocks))
