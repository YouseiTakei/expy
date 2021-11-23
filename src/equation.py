import math
import numpy as np
import sympy as sym
import pandas as pd
from sympy import sqrt, sin, cos, tan, exp, log, diff
from pyperclip import copy
from pyperclip import paste
from IPython.display import display, Math, Latex, Image, Markdown, HTML
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


'''Eq object----------------------------------------------------------------'''
'''This object responsible for processing ----------------------------------'''


class Eq:
    def __init__(self, leq, req, ans_sym=None, label='', **kwargs):
        self.label = label
        self.func, self.todiff, self.diffed = [None]*3
        self.subs_str, self.subs_val, self.subs_ans = [None]*3
        self.func_val, self.func_ans, self.func_rslt = [None]*3
        self.syn_val, self.syn_ans, self.syn_rslt = [None]*3
        self.eq = sym.Eq(leq, req)   # 方程式
        self.vars = {}                 # 方程式を構成する変数の辞書.
        self.ans = None               # ans tyoe is Var obj
        self.ans_val = 0
        self.err_val = 0
        if ans_sym:
            # ans = Var();self.ans.set_var(leq)
            self.set_func(self.vars[ans_sym].var)
        elif leq in self.vars:
            self.set_func(self.vars[leq].var)

    # latex process ----------------------------------------------------------
    def latex(self, cp=True, nb=True, rqs=[1]*5):
        self.set_tex()
        eqs = [self.ans.var, self.func, self.func_val, self.func_ans, self.func_rslt]
        latex_text = align_asta_latex([e for r, e in zip(rqs, eqs) if r], cp, nb)
        if nb:
            display(latex_text)
        else:
            return latex_text

    # error mainprocess -------------------------------------------------------
    def syn(self, cp=True, nb=True, sub_val=True):
        self.set_syn()
        eqs = [
            self.ans.d_tex(),
            sym.latex(self.todiff),
            sym.latex(self.diffed),
            self.syn_val if sub_val else None,
            self.syn_ans,
            self.syn_rslt,
        ]
        latex_text = align_asta_latex(eqs, cp, nb)
        if nb:
            display(latex_text)
        else:
            return latex_text

    # init setting -----------------------------------------------------------
    # 辞書varsに追加
    def set_var(self, obj):
        self.vars[obj.var] = obj

    def set_err(self, var, err):
        self.vars[var].err = err

    def set_func(self, ans_sym=None):
        # 入力があったらself.ansの変更
        if ans_sym:
            self.ans = self.vars[ans_sym]
        # 方程式から関数へ変形
        if self.ans:
            self.func = sym.solve(self.eq, self.ans.var)[0]
        else:
            print("please set ans_var_object as 'eq_obj.set_ans(var_obj )'")

    # 非推奨.未使用
    def set_ans(self, obj):
        self.set_func(obj.var)
        self.ans = obj

    # 非推奨.未使用
    def set_eq(self, leq, req):
        self.eq = sym.Eq(leq, req)
        self.set_func()

    # set_ansだとfuncがNoneのままなので注意
    def set_obj(self, var=None, val=None, rm='', dig=3, ans=False):
        obj = Var()
        obj.set_var(var, val, rm, dig)
        self.set_var(obj)
        if (val is None) or ans:
            self.set_func(obj.var)

    # 非推奨
    def set_err(self, var, err):
        self.vars[var].err = err

    # manage process ---------------------------------------------------------
    # set_objされていない変数をreturn
    def not_setting_obj(self):
        return [v for v in self.eq.atoms(sym.Symbol) if not v in self.vars]

    # eqの代入状態を返す
    def status(self):
        for v in self.not_setting_obj():
            print('{0} is not setting. please run "f.set_obj({0})"'.format(v))
        display(pd.DataFrame({
            ' $%s$ ' % sym.latex(var): [
                obj.val, r'$\mathrm{%s}$' % obj.rm, obj.dig,
                var == self.ans.var
            ] for var, obj in self.vars.items()
        }, index=['val', 'rm', 'dig', 'is ans']).T)

    # latex sub process ------------------------------------------------------
    # subs 代入処理
    # Sym.subs_str:  vars -> vars or str
    def set_tex(self, err=False):
        if self.ans is None:
            _ = [self.set_obj(var, None) for var in self.not_setting_obj()]
        # 初期化  # subs str
        self.subs_str = self.func
        for var, obj in self.vars.items():
            self.subs_str = obj.subs_str(self.subs_str)
        # 初期化 # subs val and ans(subs_valは使われていない...)
        self.subs_ans = self.func
        for var, obj in self.vars.items():
            self.subs_ans = obj.subs_ans(self.subs_ans)
        self.ans_val = float(self.subs_ans)
        # self.func_valの初期化
        self.func_val = sym.latex(self.subs_str)
        # 数字をマーキング
        self.func_val = mark_number(self.func_val)
        # 変数マーキング+数値代入
        for var, obj in self.vars.items():
            txt = r'{# %s\mathrm{%s} #}' % (to_sf(float(obj.val), int(obj.dig)), obj.rm)
            self.func_val = self.func_val.replace('%s' % obj.tex(), txt)
            # print("\t1", to_sf(float(obj.val), int(obj.dig)), '\t\t', txt )
            # print("\t2", '{#%s#}'%obj.tex(), "\t\t", '{#%s#}'%txt, '\t\t', self.func_val)
        self.func_val = self.func_val.replace(' ', '').replace('#}{#', r'\times').replace('{#', '').replace('#}', '')
        self.func_ans = r'%s\mathrm{%s}' % (to_sf(self.ans_val, self.ans.dig*2), self.ans.rm)
        self.func_rslt = r'%s\mathrm{%s}' % (to_sf(self.ans_val, 1 if err else self.ans.dig, up=True), self.ans.rm)

    def set_syn(self):
        pass

    def ans_align(self):
        rslt_ans_align(self.ans_val, self.err_val, self.ans.tex_name(rm=False), self.ans.rm, self.ans.dig)

    """TODO
    def set_syn(self)
        pass
        for i, [var, obj] in enumerate(self.vars.items()):
            # Var()によるtodiffとdiffedのリセット
            obj.set_diff(self.ans, self.func)
            diff_new = [Delta_(var)**2*obj.todiff, Delta_(var)**2*obj.diffed]
            if var is self.ans.var:
                pass
            elif float(obj.err) <= 0:
                pass
            elif self.todiff is None or self.diffed is None:
                self.todiff, self.diffed = diff_new
            else:
                self.todiff, self.diffed = [self.todiff+diff_new[0], self.diffed + diff_new[1]]
        self.todiff = self.ans.var*sqrt(self.todiff)
        self.diffed = self.ans.var*sqrt(self.diffed)
        # saved past value-------------------------
        past_eq = self.eq
        past_func = self.func.copy()
        past_vars = self.vars.copy()
        # print(past_ans.var)
        past_ans = self.ans
        past_rslt = self.ans_val
        # set err ---------------------------------
        # print(sym.sympify(self.diffed).atoms(sym.Symbol))
        self.set_eq(Delta_(past_ans.var), self.diffed)
        self.set_obj(Delta_(past_ans.var), None, past_ans.rm, past_ans.dig, ans=1)
        # Var()によるtodiffとdiffedのリセット
        for var, obj in past_vars.items():
            obj.set_diff(self.ans, self.func)
            self.set_obj(Delta_(var), obj.err, obj.rm, obj.dig)
        self.set_obj(past_ans.var, past_rslt, past_ans.rm, past_ans.dig, ans=0)
        self.set_tex(err=True);
        self.syn_val = self.func_val
        self.syn_ans = self.func_ans
        self.syn_rslt = self.func_rslt
        # register the new value
        self.err_val = self.ans_val
        # reset value -----------------------------------
        self.eq = past_eq
        self.func = past_func
        self.vars = past_vars
        self.ans = past_ans
        self.ans_val = past_rslt
    """
