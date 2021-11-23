# import math
import numpy as np
import sympy as sym
import pandas as pd
# from sympy import sqrt, sin, cos, tan, exp, log, diff
# from pyperclip import copy
# from pyperclip import paste
# from IPython.display import display, Math, Latex, Image, Markdown, HTML
# my create
from .util.base import eff_dig, to_sf, align_asta_latex
from .util.calc import weighted_mean, uncrt
from .util.disp import df_to_sf, rslt_ans, rslt_ans_array, rslt_ans_align
from .util.symb import *


# sub process ------------


def dollar(arr):
    return [' $%s$ ' % v for v in arr] if type(arr) != type('') else ' $%s$ ' % arr


def mark_number(text):
    rslt = text
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "pi"]
    for i, j in zip(['%s' % i for i in nums], ['{#%s#}' % i for i in nums]):
        rslt = rslt.replace(i, j)
    return rslt.replace("#}{#", "")


''' Var object--------------------------------------------------------------'''


class Var:
    # set
    def __init__(self, var=sym.Symbol('x')):
        # base ---------------------------------
        self.var = var
        self.val = 0
        self.dig = 3
        self.rm = ''
        # err --------------------------------
        # vals type is np.array
        self.array = np.array([0])
        # err  type is float
        self.err = 1
        # todiff type is sym.Symbols of(pa_*func)/(pa_*self.var)
        self.todiff = None
        # diffed type is diffed function of sym.Symbol by self
        self.diffed = None

    # init process -----------------------------------------------------------
    def set_var(self, var=None, val=None, rm=None, dig=None):
        if val is not None:
            self.set_array(val)
        if var:
            self.var = var
        if rm:
            self.rm = str(rm)
        if dig:
            self.dig = int(dig)

    def set_array(self, val):
        self.array = np.array(val)
        if self.array.size == 1:
            self.val = val
            self.err = 0
            self.dig = eff_dig(self.val)
        else:
            self.val = np.mean(val)
            self.err = np.std(val)/np.sqrt(len(val)-1)
            self.dig = eff_dig(self.array[0])

    # err process ----------------------------------------------------------
    def set_diff(self, ans_obj, function):
        self.todiff = sym.Symbol(r'(\frac{{ \partial {} }}{{ \partial {} }})^2'.format(sym.latex(ans_obj.var), sym.latex(self.var)))
        self.diffed = sym.diff(function, self.var)**2

    # latex subs process -----------------------------------------------------
    # vars to vars or str: varをマーキング
    def subs_str(self, func):
        return func.subs(self.var, '%'+sym.latex(self.var)+'%')

    # vars to vars or float: varに数値を代入
    def subs_ans(self, func):
        return func.subs(self.var, self.val)

    # vars to vars or str: varにstr(数値.round)+単位を代入
    def subs_val(self, func):
        return func.subs(self.var, r'%s\mathrm{%s}' % (round(self.val, self.dig), self.rm))

    def tex(self):
        return r'%s' % sym.latex(self.var)

    def d_tex(self):
        return r'\Delta{%s}' % sym.latex(self.var)

    def tex_name(self, err=True, rm=True):
        text = r'%s\pm %s' % (self.tex(), self.d_tex()) if err else self.tex()
        return r'%s(%s)%s' % ('(' if rm else '', text, r'/\mathrm{%s}' % self.rm if rm else '')

    # latex output process ---------------------------------------------------
    def df(self, df_name='', name=''):
        # md('%s回計測した%s $%s$ を記すと, 以下の表を得る.'%(self.array.size,(name if name else ''), self.tex()))
        data = {'%s' % name:self.array}
        df = pd.DataFrame(data, index=['']*len(self.array))
        return df.T

    def latex_mean(self, max=10, cp=True, nb=True):
        denom = ''
        N = self.array.size
        for i in range(N):
            if i != 0:
                denom = denom + '+'
            if i >= max:
                denom = denom + '..'
                break
            denom += r'%s \mathrm{%s}' % (to_sf(self.array[i], self.dig), self.rm)
        display(frac(denom, str(N), np.mean(self.array), self.tex(), self.rm, cp=True, nb=True))

    def latex_err(self, cp=True, nb=True):
        N = self.array.size
        m = to_sf(np.mean(self.array), self.dig)
        s = r'\sqrt{\frac{1}{%s\cdot%s}\sum_{i=1}^%s(%s_i-%s)^2}'%(N, N-1, N, self.tex(), m)
        display(to_latex(s, uncrt(self.array), self.d_tex(), self.rm, self.dig, cp=True, nb=True))

    def latex(self, max=10, cp=True, nb=True):
        if self.err:
            self.latex_mean(max, cp, nb)
            self.latex_err(cp, nb)
            rslt_ans_align(self.val, self.err, self.tex_name(rm=False), self.rm, self.dig)
