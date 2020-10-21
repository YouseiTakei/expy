""" here is a process of simple numerical calculations.
    define a function that return a value calculated on the input value.
    - expy-python ver.1.2.2 ©tseijp
"""



### package
import math
import numpy as np
import pandas as pd
import sympy as sym
from sympy import init_printing
from sympy import sqrt,sin,cos,tan,exp,log,diff

### helper
from .base import to_multi_d

'''1.解析-------------------------------------------------------------------------'''
#平均
def mean(a):func=lambda a:np.mean(a);return to_multi_d(func,a,1)

#関数のすべての変数に値を代入
def subs(func,sym,val):
    for i in range(len(val)):
        func = func.subs([(sym[i],val[i])])
    return func

#標準不確かさ計算
def stdev(data):
    def stdev_unit(d):
        #unit
        ave = np.sum(d) / len(d)
        siguma = 0
        for i in range(len(d)):
            siguma += math.pow(d[i] - ave, 2)
        if len(d)<=1:
            return 0
        else:
            output = math.sqrt( siguma / (len(d)-1) )
            return output
    func=lambda d:stdev_unit(d)
    return to_multi_d(func,data,1)

#平均値の不確かさ計算
def uncrt(data):
    def uncrt_unit (data):
        output = stdev(data) / math.sqrt(len(data))
        return output
    func=lambda d:uncrt_unit(d)
    return to_multi_d(func,data,1)

#相対不確かさ
def rlt_uncrt(data):
    def rlt_uncrt_unit (data):
        return uncrt(data) / np.mean(data)
    func=lambda d:rlt_uncrt_unit(d)
    return to_multi_d(func,data,1)

def cul(data,p=0):
    def cul_unit(data):
        mean  = np.mean (data)
        uncrt = ep.uncrt(data)
        rslt  = ep.rslt(mean,uncrt)
        rlt   = ep.rlt_uncrt(data)
        #結果まとめ
        df_cul = pd.DataFrame([uncrt,rslt,rlt],index=['uncrt','rslt','rlt/%',])
        df_cul = pd.Series(data).describe().append(df_cul)
        if p==1:display(df_cul.T)
        return df_cul.T
    unit=lambda d:cul_unit(d)
    return to_multi_d(unit,data,1)

#二乗和平均
def mean_sq(data):
    def mean_sq_unit(data1,data2):
        synth = math.sqrt(math.pow(data1,2)+math.pow(data2,2))
        return synth
    func=lambda d1,d2:mean_sq_unit(d1,d2)
    synth = data[0]
    for i in range(1,len(data)):
        synth = to_multi_d(func,synth,0,data[i])
    return synth

#加重平均       （不確かさの二乗の逆数で重みを浸けて平均）
def weighted_mean(mean_all, uncrt_all):
    def weighted_uncrt_unit(mean_all, uncrt_all):
        numer1 = mean_all / np.square(uncrt_all)
        denom1 =     1 / np.square(uncrt_all)
        mean  = np.sum(numer1) / np.sum(denom1)
        denom2 = 1 / np.square(uncrt_all)
        uncrt = 1 / np.sqrt(np.sum(denom2))
        return mean, uncrt
    func=lambda m,u:weighted_uncrt_unit(m,u)
    return to_multi_d(func,mean_all,1,uncrt_all)
