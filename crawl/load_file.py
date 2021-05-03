import os

def bounding(file_name):
    dic = {}
    f = open('./config/' + file_name, mode='r')
    for i in f:
        state, west, south, east, north, = i.strip().split(',')
        _value = list(map(float, [west, south, east, north]))
        dic[state] = str(_value)[1:-1]
    return dic


def account(file_name):
    dic = {}
    f = open('./config/account_' + file_name + '.csv', mode='r')
    for i in f:
        key, value = i.strip().split(',')
        dic[key] = value
    return dic


if __name__ == '__main__':


    print(os.getcwd())
    print(os.listdir(os.getcwd() ))

    print(bounding('bounding.csv'))