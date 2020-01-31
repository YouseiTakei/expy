""" here is a basic process that is also used many times,
    such as conversion of numerical values ​​and character.

    - expy-python ver.1.2.0 ©tseijp
"""
import math
import numpy as np
import sympy as sym
import pandas as pd
import matplotlib.pyplot as plt
from sympy import sqrt,sin,cos,tan,exp,log,diff
from IPython.display import Markdown, Latex, Math
from pyperclip import copy
from pyperclip import paste

### the process for digit -----------------------------------------------
#丸め
def roundup(x,dig=2):
    func=lambda x:(math.ceil(x*(10**dig))) / (10**dig)
    return to_multi_d(func,x,0)
def rounder(x,dig=2):
    func=lambda x:round(x,dig)
    return to_multi_d(func,x,0)

# 桁数
def num_dig(x):
    y = abs(x)+abs(x)*0.0000000000001
    if y>=1 : return  np.floor(np.log10(float(y)))
    if 1>y>0: return -np.floor(np.log10(float(1/y))+1)
    if y==0 : return  0


def eff_dig(num):### 有効数字何桁か   e.g. 0.03412/100000 -> 4
    num_str = str( num*(10**-num_dig(num)) )
    num_i, num_d = num_str.split('.') if '.' in num_str else (num_str, '0')
    if   '0000'in num_d: num_d = num_d.split('0000')[0]
    elif '9999'in num_d: num_d = num_d.split('9999')[0]
    return len(num_d)+1

# 有効n桁 (return float) ### this is used in tex.py
def sgnf(n_in,num_sgnf= 3):# 有効n桁
    dig = num_dig(n_in)
    n_rslt = n_in * (10**(-dig))
    n_rslt = np.round(float(n_rslt),int(num_sgnf-1));
    n_rslt = n_rslt * (10**(dig))
    return n_rslt

#多次元化df_to_sf
def to_list(data):
    if type(data) is  type(pd.Series([])):
        return data.values.tolist()
    if type(data) is  type(pd.DataFrame([])):
        return data.values.tolist()
    if type(data) is  type(np.array([])):
        return data.tolist()
    else:
        return data

def to_sf(n_in, sf_in=None, up=False):# 有効数字化
    dig = num_dig(n_in)
    sf  = sf_in if sf_in is not None  else eff_dig(n_in)
    n_rslt = n_in * (10**(-dig))
    n_rslt = roundup(float(n_rslt),int(sf-1)) if up else np.round(float(n_rslt),int(sf-1));
    if dig==0:return '%s'% roundup(n_in,sf-1) if up else np.round(n_in, sf-1)
    if dig==1:return r'%s\times 10'%(n_rslt)
    return r'%s\times 10^{%s}'%(n_rslt, int(dig))

### latex ----------------------------------------------------------------------
def align_asta_latex(unit=[],cp=False, nb=True):
    tex=""
    for i in range(len(unit)):
        if unit[i]:
            if i!=0:tex+='\n\t&='
            tex +=sym.latex(unit[i])
            if i!=0:tex+=r'\\'
    tex = r'\begin{align*}'+'\n\t'+tex+'\n\t'+r'\end{align*}'
    if cp   : copy( tex )
    if nb: return Latex( tex )
    else    : return tex

def to_latex(s='x^2+y^2',ans=0, x='z', rm='',dig=3, cp=False,nb=True,label=''):
    return align_asta_latex(['%s'%x, '%s'%s, r'%s\mathrm{%s}'%(to_sf(ans, dig*2), rm),
                      r'%s\mathrm{%s}'%(to_sf(ans, dig),rm)],cp,nb)

def frac(denom,numer,ans=0, x='z', rm='',dig=3, cp=True,nb=True,label=''):
    return to_latex(r'{\tiny \frac{%s}{%s}}'%(denom, numer), ans, x,rm,dig, cp,nb,label)

def mean_disp(data, x='%%', rm='%%',cp=True,nb=True, label=''):
    denom =  ''
    for i in range(len(data)):
        if i != 0:denom=denom+'+'
        denom += str(data[i])+rm
    #LaTeX作成
    return frac(denom,str(len(data)), np.mean(data), x, rm,p,label)

def uncrt_disp(data, x='%%', rm='%%',cp=True,nb=True, label=''):
    N=len(data);m=np.mean(data);u=uncrt(data)
    #LaTeX作成
    s = '\\sqrt{\\frac{1}{'+str(N)+'\\cdot'+str(N-1)+'}\\sum_{i=1}^'+str(N)+'('+x+'_i-'+str(m)+')^2}'
    return to_latex(s, uncrt(data), r'\Delta'+x,rm,p,label)

def weighted(mean_all, uncrt_all, x='z', rm='',dig=3,cp=True,nb=True, label=''):
    def tex_weighted_mean(mean_all, uncrt_all, x='z', rm='',cp=True,nb=True, label=''):
        denom = ''#分子
        numer = ''#分母
        for i in range(len(mean_all)):
            denom += '\\frac{%s}{(%s)^2}'%(to_sf(mean_all[i], dig), to_sf(uncrt_all[i], dig))
            numer += '\\frac{1}{(%s)^2}' % to_sf(uncrt_all[i], dig)
            if i != len(mean_all)-1:
                denom += '+'
                numer += '+'
        return frac(denom,numer,weighted_mean(mean_all,uncrt_all)[0],x,rm,dig)
    def tex_weighted_uncrt(mean_all, uncrt_all,x='z', rm='',cp=True,nb=True, label=''):
        numer = '\\sqrt{'#分母
        for i in range(len(mean_all)):
            numer += '\\frac{1}{(%s)^2}'%to_sf(uncrt_all[i], dig)
            if i != len(mean_all)-1:
                numer += '+'
            if i == len(mean_all)-1:
                numer += '}'#sqrt
        #LaTeX作成
        return frac('1',numer,weighted_mean(mean_all,uncrt_all)[1],x,rm,dig)
    display( tex_weighted_mean (mean_all, uncrt_all,           x, rm,cp,nb, label) )
    display( tex_weighted_uncrt(mean_all, uncrt_all,r'\Delta '+x, rm,cp,nb, label) )
    #md('よって $%s$ は以下のようになる.' % x)
    #rslt_ans_align(weighted_mean(mean_all,uncrt_all)[0],weighted_mean(mean_all,uncrt_all)[1],x,rm,dig)


''' (非推奨) -----------------------------------------------------------------'''
def to_discrete(arr,method=lambda a,b: b-a,axis=0):
    if type(arr) is type(pd.DataFrame([]))and axis==0:
        arr=arr.T
    def _to_discrete(arr,method=lambda a,b: b-a):
        arr_rslt=[np.NaN]
        for i in range(len(arr)-1):
            arr_rslt.append(method(arr[i],arr[i+1]))
        return arr_rslt
    arr_in=to_list(arr)
    func=lambda arr:_to_discrete(arr,method)
    return to_multi_d(func,arr_in,1)

def reshape_df(arr,col_num,col=None): ### 非推奨
    ind = []
    data=[]
    for i in range(int(len(arr)/col_num)):
        n1=i*col_num+1;### print(n1)
        n2=(i+1)*col_num
        ind.append(str(n1)+'to'+str(n2))#;print(ind)
        data.append([arr[n1-1: n2]])#;print(data)
    else:
        n1 = int(len(arr)/col_num)*col_num+1#;print(n1)
        n2 = int(len(arr)/col_num+1)*col_num#;print(n2)
        ind.append(str(n1)+'to'+str(len(arr)))#;print(ind)
        data.append([arr[n1-1:]])#;print(data)
    return pd.DataFrame(data,ind,col)

#単位変換
def mm_to_cm(a):func=lambda a:a/10;return to_multi_d(func,a,0)
def cm_to_m(a):func=lambda a:a/100;return to_multi_d(func,a,0)
def cm_to_mm(a):func=lambda a:a*10;return to_multi_d(func,a,0)

def to_multi_d(func,data,is_list,data2=None,is_none=None):#(非推奨)
    data = to_list(data)
    #p(type(data),"data_type")
    #p(is_list,"is_list")
    def do(to_arr= 0):
        if data is None:
            return is_none
        if to_arr==0 :
            if data2 is None:
                return func(data)
            else:
                return func(data,data2)
        if to_arr==1:
            if data2 is None:
                return func([data])
            else:
                return func([data],[data2])
    def repeat():
        #print("repeat-------------------start")
        output=[];
        for i in range(len(data)):
            if data2 is None:
                output.append(to_multi_d(func,data[i],is_list,is_none))
            else:
                output.append(to_multi_d(func,data[i],is_list,data2[i],is_none))
        #print("repeat-------------------end")
        return output
    #1. 入力が数値の場合
    if type(data) is not list:
        if is_list==0: return do()
        if is_list==1: return do(1)
        else:p("not ? but 0")
    #2. 入力が配列の場合
    if type(data) is     list:
        if is_list==0:
            return repeat()
        elif is_list==1:
            if type(data[0]) is not list: return do()
            if type(data[0]) is     list: return repeat()
        else:p("not ? but 1")
    else:return "??"
