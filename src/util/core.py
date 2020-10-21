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
    plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))#y軸小数点以下3桁表示.
    plt.gca().xaxis.get_major_formatter().set_useOffset(False)
    plt.locator_params(axis='x',nbins=12)#軸目盛りの個数指定.x軸，6個以内
    plt.locator_params(axis='y',nbins=12,rotation=30)#軸目盛りの個数指定.y軸，6個以内
    plt.gca().yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
    plt.xticks(rotation=70)### x軸目盛を重ならないように

def end_plt(figname='test.jpg'):
    plt.tight_layout()#グラフが重ならず，設定した図のサイズ内に収まる。
    plt.savefig(figname, dpi=600)
    return plt


### for using in ipynb ---------------------------------------------------------
def newpage(): display(Latex('\\newpage'))
def tiny()   : display(Latex(r'\tiny'))
def norm()   : display(Latex(r'\normalsize'))
def md(text= '')           : display( Md(text))
def caption(text= '')      : display( Caption(text) )
def figure(filepath,cap=''): display( Image(filepath), Caption(cap))

def table(data, cap='', text=None, index=None, is_sf= False, is_tiny=False):
    result = pd.DataFrame(data, index=index if index else ['']*len(list(data.values())[0])) if type(data) is type({}) else data
    if is_sf: result = df_to_sf(result)
    if text : display(Caption(text)) if type(text)==type('') else md('以上より, 以下の表を得る')
    if cap  : display(Caption(cap))
    if is_tiny:tiny()
    display(result)
    if is_tiny:norm()

def freehand(text= '', line=10):
    for i in range(line):
        display(Markdown('<p style="page-break-after: always;">&nbsp;</p>'))
    display(Caption(text))
