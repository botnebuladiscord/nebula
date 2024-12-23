inputdata = '`/start`\n`/farm`\n`/balance`\n`/plant`\n`/inventory`\n`/sell`\n`/market`\n`/work`\n`/leaderboard`\n`/beg`\n`/journey`\n`/pets`\n`/mypets`'
inputdata = inputdata.replace('`', '')
inputdata = inputdata.replace('/', '')

inputdata = inputdata.split('\n')

for i in inputdata:
    print(i.capitalize())