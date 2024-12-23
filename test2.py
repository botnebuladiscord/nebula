def connect3(id, connect4):
    ii = 0
    currentlist = -1
    for i in connect4[id]:
        currentlist += 1
        #HORIZONTAL CHECK
        try:
            ii = 0
            for j in i:
                ii += 1
                if j != 'n':
                    for l in range(2):
                        if i[ii+l] != j:
                            break
                    else:
                        return currentlist-1
        except:
            pass
    ii = 0
    currentlist = -1
    for i in connect4[id]:
        currentlist += 1
        #VERTICAL CHECK
        try:
            ii = 0
            for j in i:
                ii += 1
                if j != 'n':
                    for l in range(2):
                        if connect4[id][currentlist+l+1][ii-1] != j:
                            break
                    else:
                        return currentlist
        except:
            pass
    ii = 0
    currentlist = -1
    for i in connect4[id]:
        currentlist += 1
        #DIAGONAL CHECK 1
        try:
            ii = 0
            for j in i:
                ii += 1
                if j != 'n':
                    for l in range(3):
                        if connect4[id][currentlist+l+1][ii+l+1] != j:
                            break
                    else:
                        return j
        except:
            pass
    ii = 0
    currentlist = -1
    for i in connect4[id]:
        currentlist += 1
        #DIAGONAL CHECK 2
        try:
            ii = 0
            for j in i:
                ii += 1
                if j != 'n':
                    for l in range(4):
                        if connect4[id][currentlist+l][ii-(l+1)] != j:
                            break
                    else:
                        return j
        except:
            pass
    return 'random'

connect3l = {1:[['n','n','n','n','n','n','n'], ['n','n','n','n','n','n','n'], ['n','n','n','n','n','n','n'], ['1','n','n','n','n','n','n'], ['1','n','n','n','n','n','n'], ['1','n','n','n','n','n','n']]}

print(connect3(1, connect3l))