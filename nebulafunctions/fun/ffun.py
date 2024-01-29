import os
import pyimgur
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random
import datetime
import requests
import json
import urllib.parse

def extractid(arg):
    arg = str(arg).replace('<', '')
    arg = str(arg).replace('>', '')
    arg = str(arg).replace(' ', '')
    arg = str(arg).split('@')
    id = None
    for i in arg:
        if i.isnumeric():
            id = i
            break
    return id

# def uploadimgur(path, id):
#     IMGUR_ID = os.getenv('IMGUR')
#     IMGUR_SECRET = os.getenv('IMGUR_SECRET')
#     imgur = pyimgur.Imgur(IMGUR_ID, IMGUR_SECRET)
#     img = imgur.upload_image(path=path, title=f"Gameboard {id}")
#     return img.link
#     # return 'attachment://'+str(path)

def genboard(id, tictactoe):
    img = Image.open('assets/tictactoe/board.png')
    x = Image.open('assets/tictactoe/x.png')
    o = Image.open('assets/tictactoe/o.png')
    newsize = (120, 120)
    o = o.resize(newsize)
    x = x.resize(newsize)
    one = (70, 20)
    two = (250, 20)
    three = (420, 20)
    four = (70, 190)
    five = (250, 190)
    six = (420, 190)
    seven = (70, 360)
    eight = (250, 360)
    nine = (420, 360)
    board = tictactoe[id]["board"]
    for i in board:
        usesymbol = board[i]
        if str(i) == 'pos1':
            use = one
        elif str(i) == 'pos2':
            use = two
        elif str(i) == 'pos3':
            use = three
        elif str(i) == 'pos4':
            use = four
        elif str(i) == 'pos5':
            use = five
        elif str(i) == 'pos6':
            use = six
        elif str(i) == 'pos7':
            use = seven
        elif str(i) == 'pos8':
            use = eight
        elif str(i) == 'pos9':
            use = nine
            
        if usesymbol == 'x':
            xo = x
        elif usesymbol == 'o':
            xo = o
        else:
            xo = None
        if xo != None:
            img.paste(xo, use)
    img.save('assets/tictactoe/currentboard.png', quality=95)
    tbox1 = board["pos1"]
    tbox2 = board["pos2"]
    tbox3 = board["pos3"]
    tbox4 = board["pos4"]
    tbox5 = board["pos5"]
    tbox6 = board["pos6"]
    tbox7 = board["pos7"]
    tbox8 = board["pos8"]
    tbox9 = board["pos9"]
    if tbox9 == tbox8 == tbox7 != 'n':
        return 'yes'
    elif tbox6 == tbox5 == tbox4 != 'n':
        return 'yes'
    elif tbox3 == tbox2 == tbox1 != 'n':
        return 'yes'
    elif tbox1 == tbox5 == tbox9 != 'n':
        return 'yes'
    elif tbox3 == tbox5 == tbox7 != 'n':
        return 'yes'
    elif tbox1 == tbox4 == tbox7 != 'n':
        return 'yes'
    elif tbox2 == tbox5 == tbox8 != 'n':
        return 'yes'
    elif tbox3 == tbox6 == tbox9 != 'n':
        return 'yes'
    elif tbox1 != 'n' and tbox2 != 'n' and tbox3 != 'n' and tbox4 != 'n' and tbox5 != 'n' and tbox6 != 'n' and tbox7 != 'n' and tbox8 != 'n' and tbox9 != 'n':
        return 'draw'
    else:
        return None
    
def convert(num):
    try:
        return f'pos{num}'
    except:
        return None
    
def check(boxn, id, tictactoe):
    use = convert(int(boxn))
    if tictactoe[id]["board"][use] == 'n':
        return True
    else:
        return False    

def findone(id, tictactoe):
    while True:
        snum = random.choice(list(range(1,10,1)))
        a = check(snum, id, tictactoe)
        if a == True:
            return snum
    
def getanum(id, tictactoe):
    board = tictactoe[id]["board"]
    tbox1 = board["pos1"]
    tbox2 = board["pos2"]
    tbox3 = board["pos3"]
    tbox4 = board["pos4"]
    tbox5 = board["pos5"]
    tbox6 = board["pos6"]
    tbox7 = board["pos7"]
    tbox8 = board["pos8"]
    tbox9 = board["pos9"]
    if tbox1 == tbox2 != 'n':
        d = 3
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox1 == tbox3 != 'n':
        d = 2
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox2 == tbox3 != 'n':
        d = 1
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox4 == tbox5 != 'n':
        d = 6
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox4 == tbox6 != 'n':
        d = 5
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox5 == tbox6 != 'n':
        d = 4
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox7 == tbox8 != 'n':
        d = 9
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox8 == tbox9 != 'n':
        d = 7
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox7 == tbox9 != 'n':
        d = 8
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox1 == tbox5 != 'n':
        d = 9
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox1 == tbox9 != 'n':
        d = 5
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox5 == tbox9 != 'n':
        d = 1
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox3 == tbox7 != 'n':
        d = 5
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox5 == tbox7 != 'n':
        d = 3
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox3 == tbox5 != 'n':
        d = 7
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox1 == tbox4 != 'n':
        d = 7
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox1 == tbox7 != 'n':
        d = 4
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox4 == tbox7 != 'n':
        d = 1
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox5 == tbox8 != 'n':
        d = 2
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox2 == tbox5 != 'n':
        d = 8
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox2 == tbox8 != 'n':
        d = 5
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox3 == tbox6 != 'n':
        d = 9
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox6 == tbox9 != 'n':
        d = 3
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    elif tbox3 == tbox9 != 'n':
        d = 6
        a = check(d, id, tictactoe)
        if a == True:
            return d
        else:
            return findone(id, tictactoe)
    else:
        return findone(id, tictactoe)
    
async def fwanted(avatar_url):
    wantedimg = Image.open('assets/wanted/template.jpg')
    asset = avatar_url
    data = BytesIO(await asset.read())
    x = Image.open(data)
    x = x.resize((177, 177))
    wanted = wantedimg.copy()
    wanted.paste(x, (120, 212), x)
    wanted.save('assets/wanted/wanted.png', quality=95)
    
async def fprison(avatar_url):
    x = Image.open('assets/prison/template.png')
    asset = avatar_url
    data = BytesIO(await asset.read())
    wantedimg = Image.open(data)
    width, height = x.size
    width = int(width / 2)
    height = int(height / 2)
    wantedimg = wantedimg.resize((width,height))
    x = x.resize((width,height))
    wantedimg = wantedimg.copy()
    wantedimg.paste(x, (0, 0),x)
    wantedimg.save('assets/prison/prison.png', quality=95)
    
async def ftweet(avatar_url, name, hash, body):
    text = f' {body}'
    n = 1
    n2 = -1
    newtext = ''
    lastspace = 0
    for i in text:
        n2+=1
        if i == ' ':
            lastspace = n2
        if n == 0:
            if newtext[lastspace-1] == ' ':
                change = 2
            else:
                change = 0
            newtext1 = newtext[:lastspace+change]
            newtext2 = newtext[lastspace+change:]
            newtext = f'{newtext1}\n{newtext2}{i}'
            n2 += 1
        else:
            newtext = f'{newtext}{i}'
        n+=1
        if n == 67:
            n = 0

    if len(newtext.split('\n')) > 13:
        return 0

    tweetimg = Image.open('assets/twitter/template.png')
    # asset = Image.open('testimg.png')
    asset = avatar_url
    data = BytesIO(await asset.read())
    x = Image.open(data)
    x = x.resize((48, 48))

    img=x.convert('RGB')
    height,width = img.size
    lum_img = Image.new('L', [height,width] , 0)
    
    draw = ImageDraw.Draw(lum_img)
    draw.pieslice([(0,0), (height,width)], 0, 360, fill = 255, outline = "black")
    img_arr =np.array(img)
    lum_img_arr =np.array(lum_img)
    final_img_arr = np.dstack((img_arr,lum_img_arr))
    x = Image.fromarray(final_img_arr)

    font = ImageFont.truetype("assets/twitter/fontbold.ttf", 15)
    font2 = ImageFont.truetype("assets/twitter/font.ttf", 15)
    font3 = ImageFont.truetype("assets/twitter/font.ttf", 17)

    tweet = tweetimg.copy()
    tweet.paste(x, (15,5), x)
    I1 = ImageDraw.Draw(tweet)
    I1.text((74, 11), name, fill=(231, 233, 234), font=font)
    I1.text((74, 30), f'@{name}#{hash}', fill=(113, 118, 123), font=font2)
    I1.text((14, 67), newtext, fill=(231, 233, 234), font=font2)
    
    tweetimg = Image.open('assets/twitter/template.png')
    asset = Image.open('assets/twitter/person.png')
    x = asset
    x = x.resize((48, 48))
    tweet.paste(x, (16, 489), x)
    I1 = ImageDraw.Draw(tweet)
    replynames = ['Adam', 'Jeffery', 'Gale', 'Harry', 'Tom', 'Rohit', 'Ramesh', 'Antonia', 'Lily', 'Rita', 'Emma', 'Kylie', 'Sonia']
    replyname = random.choice(replynames)
    pos = len(replyname)*8+8+8
    I1.text((76, 492), replyname, fill=(231, 233, 234), font=font)
    I1.text((76+pos, 492), f'@{random.choice(["thereal_", ""])}{replyname}{random.randint(1,10000)}', fill=(113, 118, 123), font=font2)
    replies = ['Thats garbage', 'Stupidity', 'Makes slight sense', '?', 'That is workable', 'No, No, No', 'Yes sure', 'Thats dumpster fire']
    reply = random.choice(replies)
    I1.text((76, 525), reply, fill=(231, 233, 234), font=font2)
    
    views = str(random.randint(0,1000000))
    time = datetime.datetime.now().strftime('%I:%M %p · %b %d, %Y ·')
    pos = len(time)*6.6417
    spaceslen = len(views)*2.7
    spaces = ''
    for i in range(int(spaceslen)):
        spaces = f'{spaces} '
    likes = str(random.randint(0,10000))
    likeslen = len(likes)*2.7
    likespaces = ''
    for i in range(int(likeslen)):
        likespaces = f'{likespaces} '
    I1.text((14, 340), f'{time} {spaces}Views', fill=(113, 118, 123), font=font2)
    I1.text((14+pos, 340), f' {views}', fill=(231, 233, 234), font=font)
    I1.text((84, 390), f'{likes}', fill=(231, 233, 234), font=font)
    I1.text((84, 390), f'{likespaces} Likes', fill=(231, 233, 234), font=font2)
    I1.text((84, 390), f'{likespaces} Likes', fill=(231, 233, 234), font=font2)

    tweet.save('assets/twitter/tweet.png', quality=95)
    
def question(num=None, difficulty=None):
    if num != None and difficulty != None:
        url = f"https://opentdb.com/api.php?amount=1&category={num}&difficulty={difficulty}&encode=url3986"
    elif num != None and difficulty == None:
        url = f"https://opentdb.com/api.php?amount=1&category={num}&encode=url3986"
    elif num == None and difficulty != None:
        url = f"https://opentdb.com/api.php?amount=1&difficulty={difficulty}&encode=url3986"
    else:
        url = "https://opentdb.com/api.php?amount=1&encode=url3986"
    r = requests.get(url)
    json_data = json.loads(r.text)
    qs = json_data['results'][0]['question']
    d = json_data["results"][0]['difficulty']
    incorrect = json_data['results'][0]['incorrect_answers']
    correct = json_data['results'][0]['correct_answer']
    qs = urllib.parse.unquote(qs)
    correct = urllib.parse.unquote(correct)
    incorrect2 = []
    for i in incorrect:
        i = urllib.parse.unquote(i)
        incorrect2.append(i)
    incorrect = incorrect2
    
    return(qs, incorrect, correct, d)

def getpoints(member):    
    member = str(member)
    try:
        with open('storage/quiz.json') as file:
            data = json.load(file)
            return data[member]["points"]
    except:
        return 0
    
def getwins(member):    
    member = str(member)
    try:
        with open('storage/quiz.json') as file:
            data = json.load(file)
            return data[member]["won"]
    except:
        return 0
    
def getgameslost(member):    
    member = str(member)
    try:
        with open('storage/quiz.json') as file:
            data = json.load(file)
            return data[member]["lost"]
    except:
        return 0

def updatepoints(member,points,won,lost):
    with open('storage/quiz.json') as file:
        data = json.load(file)
    data[str(member)] = {"points":points, "won":won, "lost":lost}
    with open('storage/quiz.json', 'w') as file:
        json.dump(data, file)
        
def convertquiz(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def genconnect4(id, connect4):
    gameboard = Image.open('assets/connect4/board.png').convert('RGBA')
    yellow = Image.open('assets/connect4/yellow.png').convert('RGBA').resize((75,75))
    red = Image.open('assets/connect4/red.png').convert('RGBA').resize((75,75))
        
    def trans_paste(fg_img,bg_img,alpha=1.0,box=(0,0)):
        fg_img_trans = Image.new("RGBA",fg_img.size)
        fg_img_trans = Image.blend(fg_img_trans,fg_img,alpha)
        bg_img.paste(fg_img_trans,box,fg_img_trans)
        return bg_img
    

    row = 80
    column = 90
    totalcolumn = 12
    totalrow = 2
    indexc = -1
    for i in connect4[id]:
        indexc += 1
        indexr = -1
        for j in i:
            indexr+=1
            if j == '1':
                totalcolumn = 12
                totalrow = 2
                for l in range(indexc):
                    totalrow+=row
                for l in range(indexr):
                    totalcolumn+=column
                gameboard = trans_paste(yellow,gameboard,1,(totalcolumn,totalrow))
            elif j == '2':
                totalcolumn = 12
                totalrow = 2
                for l in range(indexc):
                    totalrow+=row
                for l in range(indexr):
                    totalcolumn+=column
                gameboard = trans_paste(red,gameboard,1,(totalcolumn,totalrow))

    gameboard.save('assets/connect4/currentboard.png') 
    
def connect4move(id, columnno, color, connect4):
    for i in range(6,0,-1):
        i -= 1
        if connect4[id][i][columnno-1] == 'n':
            if color == "yellow":
                connect4[id][i][columnno-1] = '1'
                break
            elif color == "red":
                connect4[id][i][columnno-1] = '2'    
                break
    else:
        return False
    
def checkconnect4(id, connect4):
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
                    for l in range(3):
                        if i[ii+l] != j:
                            break
                    else:
                        return j
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
                    for l in range(3):
                        if connect4[id][currentlist+l+1][ii-1] != j:
                            break
                    else:
                        return j
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
                        return currentlist
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
        
# def connect3(id, connect4):
#     # ii = 0
#     # currentlist = -1
#     # for i in connect4[id]:
#     #     currentlist += 1
#     #     #HORIZONTAL CHECK
#     #     try:
#     #         ii = 0
#     #         for j in i:
#     #             ii += 1
#     #             if j != 'n':
#     #                 for l in range(2):
#     #                     if i[ii+l] != j:
#     #                         break
#     #                 else:
#     #                     if column != None:
#     #                         if currentlist+l+3 != column:
#     #                             return currentlist+l+3
#     #                     else:
#     #                         print(currentlist)
#     #                         print(l)
#     #                         print('h')
#     #                         return currentlist+l+3
#     #     except:
#     #         pass
    
#     ii = 0
#     currentlist = -1
#     connect42 = connect4[id].copy()
#     connect42.reverse()
#     for i in connect42:
#         currentlist += 1
#         #HORIZONTAL CHECK
#         try:
#             ii = 0
#             for j in i:
#                 if j != 'n':
#                     for z in range(1,3):
#                         if connect42[currentlist][ii+z] != j:
#                             break
#                     else:
#                         if connect4[currentlist][ii+4] != 'n':
#                             return connect42[currentlist][ii+4]
#                 ii += 1
#         except:
#             pass
    
    
    
#     # ii = 0
#     # currentlist = -1
#     # for i in connect4[id]:
#     #     currentlist += 1
#     #     #VERTICAL CHECK
#     #     try:
#     #         ii = 0
#     #         for j in i:
#     #             ii += 1
#     #             if j != 'n':
#     #                 ll = 0
#     #                 for l in range(2):
#     #                     if connect4[id][currentlist+l+1][ii-1] != j:
#     #                         break
#     #                     else:
#     #                         ll = l
#     #                 else:
#     #                     if column != None:
#     #                         if currentlist+ll+3 != column:
#     #                             return currentlist+ll+3
#     #                     else:
#     #                         print(currentlist)
#     #                         print(l)
#     #                         print('v')
#     #                         return currentlist+ll+3
#     #     except:
#     #         pass
    
#     ii = 0
#     currentlist = -1
#     connect42 = connect4[id].copy()
#     connect42.reverse()
#     for i in connect42:
#         currentlist += 1
#         #VERTICAL CHECK
#         try:
#             ii = 0
#             for j in i:
#                 if j != 'n':
#                     for z in range(1,3):
#                         if connect42[currentlist+z][ii] != j:
#                             break
#                     else:
#                         if connect4[currentlist+3][ii] == 'n':
#                             return connect42[currentlist+1][ii]
#                 ii += 1
#         except:
#             pass
    
#     # ii = 0
#     # currentlist = -1
#     # for i in connect4[id]:
#     #     currentlist += 1
#     #     #DIAGONAL CHECK 1
#     #     try:
#     #         ii = 0
#     #         for j in i:
#     #             ii += 1
#     #             if j != 'n':
#     #                 for l in range(2):
#     #                     if connect4[id][currentlist+l+1][ii+l+1] != j:
#     #                         break
#     #                 else:
#     #                     if column != None:
#     #                         if currentlist+l+3 != column:
#     #                             return currentlist+l+3
#     #                     else:
#     #                         print(currentlist)
#     #                         print(l)
#     #                         print('d1')
#     #                         return currentlist+l+3
#     #     except:
#     #         pass
#     # ii = 0
#     # currentlist = -1
#     # for i in connect4[id]:
#     #     currentlist += 1
#     #     #DIAGONAL CHECK 2
#     #     try:
#     #         ii = 0
#     #         for j in i:
#     #             ii += 1
#     #             if j != 'n':
#     #                 for l in range(2):
#     #                     if connect4[id][currentlist+l][ii-(l+1)] != j:
#     #                         break
#     #                 else:
#     #                     if column != None:
#     #                         if currentlist+l+3 != column:
#     #                             return currentlist+l+3
#     #                     else:
#     #                         print(currentlist)
#     #                         print(l)
#     #                         print('d2')
#     #                         return currentlist+l+3
#     #     except:
#     #         pass
#     return 'random'

# # def connect3(id, connect4):
# #     ii = 0
# #     currentlist = -1
# #     for i in connect4[id]:
# #         currentlist += 1
# #         #HORIZONTAL CHECK
# #         try:
# #             ii = 8
# #             for j in i:
# #                 ii -= 1
# #                 if j != 'n':
# #                     for l in range(2):
# #                         if i[ii+l] != j:
# #                             break
# #                     else:
# #                         if ii <= 4:
# #                             return 
# #         except:
# #             pass
# #     ii = 0
# #     currentlist = -1
# #     for i in connect4[id]:
# #         currentlist += 1
# #         #VERTICAL CHECK
# #         try:
# #             ii = 8
# #             for j in i:
# #                 ii -= 1
# #                 if j != 'n':
# #                     for l in range(2):
# #                         if connect4[id][currentlist+l+1][ii-1] != j:
# #                             break
# #                     else:
# #                         return ii
# #         except:
# #             pass
# #     ii = 0
# #     currentlist = -1
# #     for i in connect4[id]:
# #         currentlist += 1
# #         #DIAGONAL CHECK 1
# #         try:
# #             ii = 8
# #             for j in i:
# #                 ii -= 1
# #                 if j != 'n':
# #                     for l in range(2):
# #                         if connect4[id][currentlist+l+1][ii+l+1] != j:
# #                             break
# #                     else:
# #                         return j
# #         except:
# #             pass
# #     ii = 0
# #     currentlist = -1
# #     for i in connect4[id]:
# #         currentlist += 1
# #         #DIAGONAL CHECK 2
# #         try:
# #             ii = 8
# #             for j in i:
# #                 ii -= 1
# #                 if j != 'n':
# #                     for l in range(2):
# #                         if connect4[id][currentlist+l][ii-(l+1)] != j:
# #                             break
# #                     else:
# #                         return j
# #         except:
# #             pass
    
# #     return 'random'