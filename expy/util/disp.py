""" here is the process related to the display, such as graphs and tables.
    you use here method in ipynb, and this help to convert ipynb to pdf.
    - expy-python ver.1.2.2 ©tseijp
"""

### packages
import math
import numpy  as np
import pandas as pd
import sympy  as sym
import matplotlib.pyplot as plt
from pyperclip import copy
from pyperclip import paste
from IPython.display import display, Latex

### my create
from .base import *

'''to interpret the results (結果の表示)--------------------------------------'''
def rslt_ans(mean, uncrt=None, rm=None, dig=None, dollar=False):
    #def roundup(x,dig):return (np.ceil(x*(10**dig))) / (10**dig)
    sf  = dig if dig else eff_dig(mean)
    if not uncrt:return '%s%s'%(to_sf(mean, sf), r'\mathrm{%s}'%rm if rm else '')
    dig_u = int(-num_dig(uncrt)) ### 以降はuncrtに桁を合わせる
    ans = r"%s\pm %s"%(to_sf(round(mean, dig_u)), to_sf(roundup(uncrt,dig_u)))
    rslt= r'%s%s%s'%('('if rm else '', ans, r')/\mathrm{%s}'%rm if rm else '')
    return ' $%s$ '%rslt if dollar else rslt

def rslt_ans_array(mean,uncrt=None,rm=None,dig=None):
    return [rslt_ans(m, u, rm, dig) for m, u in zip(mean, uncrt)]

def rslt_ans_align(mean, uncrt,x, rm='',dig=None):
    def _align_asta_latex(unit=[],cp=True, nb=True):
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
    display(_align_asta_latex([x, rslt_ans(mean, uncrt, rm, dig)]))

def df_to_sf(data, dig=3): #DataFrameの数値をto_sf する
    df = data.copy()
    for key, val in data.items():
        df[key] = ['$%s$'%to_sf(v, dig) if type(v)!= type('') else v for v in val]
    return df

### pd--------------------------------------------------------------------------
def mkdf(in_data):
    ind = []
    col = in_data[0]
    data= []
    for i in in_data:
        ind.append(i[0])
        data.append(i[1:])
    if ind[1]==0:### DATA_IS_NO_INDEX
        return pd.DataFrame(data[1:],index=None,columns=col[1:])
    elif col[1]==0:### DATA_IS_NO_COLUMNS
        return pd.DataFrame(data[1:],index=ind[1:],columns=None)
    else: return pd.DataFrame(data[1:],index=ind[1:],columns=col[1:])

### plt  -----------------------------------------------------------------------
def rslt_polyfit(x,y,dig=3):
    a,b = np.polyfit(x,y,1)
    return 'y='+str(round(a,dig))+'x+'+str(round(b,dig))

def rslt_polyfit_plot(x, y1, graph=None,point='v--',line=0.75,back=False, plot=True, input=True):
    a,b = np.polyfit(x, y1, 1)
    y2=[]
    for i in x:
        y2.append(i*a+b)
    if plot:
        if graph: [fig.plot(x,y,point, lw=line) for y in [y1, y2]]
        else    : [plt.plot(x,y,point, lw=line) for y in [y1, y2]]
    if back: return a, b

def begin_plt():#by
    plt.figure(figsize=(3.14,3.14))    #3.14 インチは約8cm
    #軸の数値の桁数指定
    plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))#y軸小数点以下3桁表示.
    #軸の数字が整数になるようにする
    plt.gca().xaxis.get_major_formatter().set_useOffset(False)
    plt.locator_params(axis='x',nbins=12)#軸目盛りの個数指定.x軸，6個以内
    plt.locator_params(axis='y',nbins=12,rotation=30)#軸目盛りの個数指定.y軸，6個以内
    ### plt.gca().yaxis.set_major_formatter(plt.ticker.MultipleLocator(20))           # 20ごと
    ### plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(5))                # 最大5個
    #軸目盛りの向きおよび枠のどの位置はありにするかを指定
    plt.gca().yaxis.set_tick_params(which='both', direction='in',bottom=True,
                                    top=True, left=True, right=True)
    plt.xticks(rotation=70)### x軸目盛を重ならないように

def end_plt(figname='test.jpg'):
    plt.tight_layout()#グラフが重ならず，設定した図のサイズ内に収まる。
    plt.savefig(figname, dpi=600)
    return plt



''' (非推奨) -----------------------------------------------------------------'''
# 有効数字化 (return str)==to_sf >> to_sgnf_fig is not recommended.
def rslt(mean,uncrt):
    def roundup(x,dig):return (math.ceil(x*(10**dig))) / (10**dig)
    def rslt_unit(mean,uncrt):
        dig = -num_dig(uncrt)
        return "{0}±{1}".format(rounder(mean, dig), roundup(uncrt,dig))
    func=lambda m,u: rslt_unit(m,u)
    return to_multi_d(func,mean,0,uncrt)
def to_sgnf_fig(n_in,num_sgnf):
    dig = num_dig(n_in)
    if dig==0:return str(np.round(n_in, num_sgnf))
    n_rslt = n_in * (10**(-dig))
    n_rslt = np.round(float(n_rslt),int(num_sgnf-1));
    rslt = r'{0}\times 10^{{{1}}}'.format(n_rslt, int(dig))
    return rslt
