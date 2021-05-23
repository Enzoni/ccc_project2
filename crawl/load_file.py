# -*- coding: utf-8 -*-

# COMP90024 Assignment 2
# Team: 38
# City: Melbourne
# Members:
# Ziran Gu (1038782)
# Jueying Wang (1016724)
# Yifei Zhou(980429)
# Jiakai Ni (988303)
# Ziyue Liu (1036109)

import os

def bounding(file_name):
    """
    read bounding box information from file
    :param file_name: (str)
    :return: (dic) bounding box information
    """
    dic = {}
    f = open('./config/' + file_name, mode='r')
    for i in f:
        state, west, south, east, north, = i.strip().split(',')
        _value = list(map(float, [west, south, east, north]))
        dic[state] = str(_value)[1:-1]
    return dic


def account(file_name):
    """
    read account information form file
    :param file_name: (str)
    :return: (dic) account information
    """
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