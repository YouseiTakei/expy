# import math
# import numpy as np
# import sympy as sym
# import pandas as pd
# import matplotlib.pyplot as plt
# from sympy import init_printing
# from IPython.display import Latex
# from sympy import sqrt,sin,cos,tan,exp,log,diff
# from .function import F


# init process in jupyter ----------------------------------------------------
def init_ep():
    # init_printing()
    init_pd()
    init_plt()
    global added


def init_pd():
    try:
        def _repr_html_(self):
            return '<center> %s </center>' % self.to_html()

        def _repr_latex_(self):
            return "\\begin{center} %s \\end{center}" % self.to_latex(escape=False)

        # nbconvert: using pandas DataFrame by xelatex
        # monkey patch pandas DataFrame
        pd = globals()['pd']
        pd.set_option('display.notebook_repr_html', True)
        pd.set_option('display.max_colwidth', -1)
        pd.DataFrame._repr_html_ = _repr_html_
        pd.DataFrame._repr_latex_ = _repr_latex_
    except ImportError:
        print('UserError: you can\'t init pd')


def init_plt(name='test.jpg'):
    try:
        # plt.rcParams['font.family'] ='IPAGothic'# 'sans-serif'
        plt = globals()['plt']
        plt.rcParams['mathtext.default'] = 'regular'
        plt.rcParams['xtick.top'] = 'True'
        plt.rcParams['ytick.right'] = 'True'
        # x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
        plt.rcParams['xtick.direction'] = 'in'
        # y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
        plt.rcParams['ytick.direction'] = 'in'
        # x軸主目盛り線の線幅
        plt.rcParams['xtick.major.width'] = 1.0
        # y軸主目盛り線の線幅
        plt.rcParams['ytick.major.width'] = 1.0
        plt.rcParams['axes.grid'] = 'True'
        plt.rcParams['axes.xmargin'] = '0'
        plt.rcParams['axes.ymargin'] = '.05'
        # 軸の線幅edge linewidth。囲みの太さ
        plt.rcParams['axes.linewidth'] = 1.0
        # plt.rcParams['savefig.facecolor'] = 'None'
        # plt.rcParams['savefig.edgecolor'] = 'None'
        plt.rcParams['savefig.bbox'] = 'tight'
        plt.rcParams['font.size'] = 8
        plt.rcParams['xtick.labelsize'] = 8
        plt.rcParams['ytick.labelsize'] = 8
    except ImportError:
        print('UserError: you can\'t init plt')


init_ep()
