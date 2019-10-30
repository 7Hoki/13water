import requests

import re

used = [0 for i in range(13)]
pai = [0 for i in range(14)]

paise = [0 for i in range(14)]

maxnc = 0
qans1 = ""
qans2 = ""
qans3 = ""
ms1 = 0
ms2 = 0
ms3 = 0
duiyin = {0: '&', 1: '$', 2: '#', 3: '*'}


def lol(n, a, b):
    tt = ""
    for i in range(n):
        if i != 0:
            tt += ' '
        tt += duiyin[b[i]]
        if a[i] == 11:
            tt += 'J'
        elif a[i] == 12:
            tt += 'Q'
        elif a[i] == 13:
            tt += 'K'
        elif a[i] == 14:
            tt += 'A'
        else:
            tt += str(a[i])
    return tt


def score():
    global maxnc, qans2, qans1, qans3, ms1, ms2, ms3
    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    for i in range(13):
        if used[i] == 1:
            a.append(pai[i])
            b.append(paise[i])
        elif used[i] == 0:
            c.append(pai[i])
            d.append(paise[i])
        else:
            e.append(pai[i])
            f.append(paise[i])

    for i in range(2):
        for j in range(2 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                b[j], b[j + 1] = b[j + 1], b[j]
    for i in range(4):
        for j in range(4 - i):
            if c[j] > c[j + 1]:
                c[j], c[j + 1] = c[j + 1], c[j]
                d[j], d[j + 1] = d[j + 1], d[j]
    for i in range(4):
        for j in range(4 - i):
            if e[j] > e[j + 1]:
                e[j], e[j + 1] = e[j + 1], e[j]
                f[j], f[j + 1] = f[j + 1], f[j]
    ans1 = score1(a)
    ans2 = score2(c, d)
    if ans1 > ans2:
        return 0
    ans3 = score2(e, f)

    if ans1 < ans2 < ans3 and 3 * ans1 + 2 * ans2 + ans3 > maxnc:
        maxnc = 3 * ans1 + 2 * ans2 + ans3
        ms1, ms2, ms3 = ans1, ans2, ans3
        qans1 = lol(3, a, b)
        qans2 = lol(5, c, d)
        qans3 = lol(5, e, f)


def score1(a):
    if a[0] == a[1] and a[1] == a[2]:
        return 50 + a[2] / 100
    if a[0] == a[1]:
        return 20 + a[0] / 100 + a[2] / 1000
    if a[1] == a[2]:
        return 20 + a[2] / 100 + a[0] / 1000

    return 10 + a[2] / 10 + a[1] / 100


def score2(a, b):
    node = 1
    for i in range(4):
        if a[i] + 1 != a[i + 1] or b[i] != b[i + 1]:
            node = 0
    if 1 == node:
        return 170 + a[4] / 100
    if (a[0] == a[1] and a[1] == a[2] and a[2] == a[3]) or (a[3] == a[4] and a[1] == a[2] and a[2] == a[3]):
        return 120 + a[3] / 100
    # 葫芦
    if (a[0] == a[1] and a[1] == a[2] and a[4] == a[3]) or (a[3] == a[4] and a[1] == a[0] and a[2] == a[3]):
        return 80 + a[2] / 100
    # 同花
    if b[0] == b[1] and b[1] == b[2] and b[2] == b[3] and b[3] == b[4]:
        return 70 + a[4] / 100
    # 顺子
    if (a[0] + 1 == a[1]) and (a[1] + 1 == a[2]) and (a[4] == a[3] + 1) and (a[2] + 1 == a[3]):
        return 60 + a[4] / 100
    # 三条
    if (a[0] == a[1] and a[1] == a[2]) or (a[2] == a[3] and a[1] == a[2]) or (a[3] == a[2] and a[3] == a[4]):
        return 50 + a[2] / 100
    # 连对
    if ((a[0] == a[1]) and (a[2] == a[3]) and (a[2] == a[1] + 1)) or (
            (a[2] == a[1]) and (a[4] == a[3]) and (a[1] + 1 == a[3])):
        return 40 + a[3] / 100
    # 两对
    if ((a[0] == a[1]) and (a[2] == a[3])) or ((a[0] == a[1]) and (a[4] == a[3])) or (a[2] == a[1] and a[4] == a[3]):
        return 30 + a[3] / 100 + a[1] / 10000

    for i in range(4):
        if a[i] == a[i + 1]:
            if i == 3:
                return 20 + a[3] / 100 + a[2] / 10000
            else:
                return 20 + a[i] / 100 + a[3] / 10000

    return 10 + a[4] * 0.1 + a[3] / 100 + a[2] / 1000


def find2(pos, n):
    if pos == 13 and n == 0:
        score()
        return True
    if pos == 13:
        return False
    while used[pos] == 2:
        pos += 1
        if pos == 13 and n == 0:
            score()
            return True
        if pos == 13:
            return False
    if n > 0:
        used[pos] = 1
        find2(pos + 1, n - 1)
        used[pos] = 0
    find2(pos + 1, n)


def find1(pos, n):
    global ans
    if pos == 13 and n == 0:
        a = []
        b = []
        for i in range(13):
            if used[i] == 2:
                a.append(pai[i])
                b.append(paise[i])
        if score2(a, b) < 20:
            return False
        find2(0, 3)
        return True
    if pos == 13:
        return False
    if n > 0:
        used[pos] = 2
        find1(pos + 1, n - 1)
        used[pos] = 0
    find1(pos + 1, n)


def predeal(paii):
    paii = paii.split(" ")
    for i in range(13):
        if paii[i][0] == '&':
            paise[i] = 0
        elif paii[i][0] == '$':
            paise[i] = 1
        elif paii[i][0] == '#':
            paise[i] = 2
        else:
            paise[i] = 3

        if paii[i][1] == '1':
            pai[i] = 10
        elif paii[i][1] == 'J':
            pai[i] = 11
        elif paii[i][1] == 'Q':
            pai[i] = 12
        elif paii[i][1] == 'K':
            pai[i] = 13
        elif paii[i][1] == 'A':
            pai[i] = 14
        else:
            pai[i] = int(paii[i][1])


def run(t: str):
    global maxnc, qans3, qans2, qans1
    maxnc = 0
    predeal(t)
    find1(0, 5)
    print(qans1)
    print(qans2)
    print(qans3)


tokene = ""
idd = 0


def log_in():
    url = "http://api.revth.com/auth/register2"
    headers = {
        'content-type': 'application/json'
    }

    payload = "{\"username\":\"hhh\",\"password\":\"0000\"}"

    response = requests.request("POST", url, data=payload, headers=headers)

    aaa = str(response.text)
    global tokene, idd
    p = re.compile(r'token":"(.+?)"')
    tokene = p.findall(aaa)[0]
    # p = re.compile(r'user_id":(.+?),')
    # idd = int(p.findall(aaa)[0])
    # token = p.findall(response.text)[0]


def open_game():
    url = 'http://api.revth.com/game/open'

    headers = {'x-auth-token': tokene}
    response = requests.request("POST", url, headers=headers)

    tok1 = str(response.text)

    global idd
    p1 = re.compile(r'card":"(.+?)"')
    str0 = p1.findall(tok1)[0]
    p2 = re.compile(r'id":(.+?),')
    idd = int(p2.findall(tok1)[0])
    run(str0)


def submit():
    url = "http://api.revth.com/game/submit"
    headers = {
        'content-type': "application/json",
        'x-auth-token': tokene
    }
    payload = "{\"id\":"
    payload = payload + str(idd)
    payload = payload + ",\"card\":[\""
    payload = payload + str(qans1)
    payload = payload + "\",\""
    payload = payload + str(qans2)
    payload = payload + "\",\""
    payload = payload + str(qans3)
    payload = payload + "\"]}"

    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text


def validate():
    url = 'http://api.revth.com/auth/validate'
    headers = {
        "x-auth-token": tokene
    }
    requests.request("GET", url, headers=headers)


# a = [5,5,14]
# b=[0,1,2]
# c =[2,3,4,13,13]
# d = [2,3,3,2,1]
#
# print(score1(a,b),score2(c,d))
#
# a=[2,4,14]
# b=[2,3,2]
# c=[3,5,5,13,13]
# d=[3,0,1,2,1]
# print(score1(a,b),score2(c,d))


# 输入卡牌，输出答案请用这个
# while True:
#     ttt = input()
#     run(ttt)



# 刷分请用这个，并在225行改账号密码
log_in()
validate()
open_game()
ttt = 0
anss = submit()
while True:
    open_game()
    ans = submit()
    if ans != anss:
        print(ans)
        print("error")
        print(qans1)
        print(qans2)
        print(qans3)
        break
    if ttt > 1000:
        print("finish")
        break
    ttt += 1
    print(ttt)

