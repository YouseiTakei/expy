import math
import numpy  as np
import sympy  as sym
import pandas as pd

from sympy import sqrt,sin,cos,tan,exp,log,diff
from pyperclip import copy
from pyperclip import paste
from IPython.display import display, Markdown

### my create
from .util.base import to_sf
from .util.disp import rslt_ans, rslt_ans_array, rslt_ans_align
from .util.symb import *

from .eq import Eq
''' F object--------------------------------------------------------------------
  * This object responsible for manipulating other objects
  * grammar
-----------------------------------------------------------------------------'''
class F:
    def __init__(self, leq, req, ans_sym=None, label='', **kwargs):
        ### init data -----------
        self.leq    = leq
        self.req    = req
        self.ans_sym= ans_sym
        self.label  = label
        ### process data --------
        self.obj    = Eq(self.leq, self.req, self.ans_sym, self.label)
        self.objs   = []
        ### get Eq_obj data -----
        self.eq = self.obj.eq
        ### TODO ----------------
        self.is_cp = True
        self.is_nb = True
        ### ---------------------
    ### main latex process in ipython -----------------------------------------
    def __call__(self, var=None, num=None, rqs=[1]*5):
        if self.objs==[]:self.save()
        for obj in self.objs: obj.latex(cp=self.is_cp, nb=self.is_nb, rqs=rqs)

    def save(self):
        self.obj.set_tex()
        self.objs.append(self.obj)
        self.obj = Eq(self.leq,self.req, self.ans_sym, self.label) ### リセット

    def syn(self, num=None, sub=True):pass#TODO
        #_=[obj.syn(nb=self.tex_num(i, num),sub_val=sub) for i,obj in enumerate(self.objs)]

    def tex(self, var=None, num=None, rqs=[1]*5):
        for obj in self.objs: obj.latex(cp=True, nb=True, rqs=rqs)
        pass#TODO
        #if self.objs==[]:self.save()
        #if var:self.tex_var(var,num) if var!=self.objs[-1].ans.var else self.tex_ans(num)
        #else  :self.tex_ans(var if var==0 else num)

    ### sub latex process in ipython
    #def latex(self, num=None):self.tex_ans(num)### 非推奨(昔使ってたので)
    #def tex_num(self,n,arr):return True if arr is None else True if n==arr or n in np.array(arr) else False
    #def tex_var(self,var,num):_=[obj.latex() for obj in self.get_vars(var, num)];
    #def tex_ans(self    ,num):_=[obj.latex(nb=self.tex_num(i,num)) for i,obj in enumerate(self.objs)]
    ### input process in ipython -----------------------------------------
    def set(self, var=None, val=None, rm='', dig=None, ans=False, err=None):
        self.obj.set_obj(var, val, rm, dig, ans)
        if err: self.obj.set_err(var, err)#var.set_objにはerrキーはないので注意！

    ### input sub process in ipython
    def set_obj(self, var=None, val=None, rm='', dig=None, ans=False):
        self.obj.set_obj(var, val, rm, dig, ans)
    def set_err(self, var, err):
        self.obj.set_err(var, err)

    ### output sub process in ipython ------------------------------------------
    def get(self, var=None, num=None, ans=False, err=False):
        if var:vals=self.get_rslt_var(var)if ans else self.get_var_err(var)if err else self.get_var_val(var)
        else  :vals=self.get_rslt_ans()   if ans else self.get_ans_err()   if err else self.get_ans_val()
        if type(num)==type(0) :return vals[num]
        if type(num)==type([]):return [vals[n] for n in num]
        ### if not var and len(self.objs)==1  :return vals[-1]
        return vals

    ### output sub process in ipython
    def get_var(self,var=None):return self.objs[-1].vars[var] if var else self.objs[-1].ans
    def get_ans_val(self)     :return[obj.ans_val         for obj in self.objs]
    def get_ans_err(self)     :return[obj.err_val         for obj in self.objs]
    def get_var_val(self,var) :return[obj.vars[var].val   for obj in self.objs]
    def get_var_err(self,var) :return[obj.vars[var].err   for obj in self.objs]
    def get_var_arr(self, var):return[obj.vars[var].array for obj in self.objs]
    def get_rslt_ans(self)    :return rslt_ans_array(self.get_ans_val()   ,self.get_ans_err()   ,self.get_var().rm   ,self.get_var().dig)
    def get_rslt_var(self,var):return rslt_ans_array(self.get_var_val(var),self.get_var_err(var),self.get_var(var).rm,self.get_var(var).dig)
    def get_vars(self, var, num= None):
        if type(num)==type(0) :return [self.objs[num].vars[var]]
        if type(num)==type([]):return [self.objs[i].vars[var] for i in num]
        if num is None:return [obj.vars[var] for obj in self.objs ]

    ### main dataframe process in ipython --------------------------------------
    def df(self, var=None, cap='', index=None, name='', text=False, ans=True, err=False, nb=True):
        ans  = self.objs[0].ans;
        vals = self.get(var, num=None, ans=ans, err=err);
        ### index
        if type(index)==type({}):dict = {key: ['$%s$'%v for v in val ] for key, val in index.items()}
        else: dict= {'回数':['%s回目'% (i+1) for i in range(len((vals)))]} if index else {}
        if var:dict.update( {'測定結果$%s$'%(r'/\mathrm{%s}'%ans.rm if ans.rm else''):[[' $%s$'%to_sf(v) for v in arr] for arr in self.get_var_arr(var)]} );
        dict.update( {'$%s%s%s$'%(name,ans.var,r'/\mathrm{%s}'%ans.rm if ans.rm else''): dollar(vals) } );
        ### md
        if text: md(text) if type(text)==type('') else md(r'全項目の計算結果を下表にまとめた.単位は $\mathrm{%s}$ である.'%self.get_var().rm)
        if nb: display(Caption(cap), pd.DataFrame(dict, index=['']*len(vals)) );
        else    : return pd.DataFrame(dict, index=['']*len(vals))

    def status(self):[obj.status() for obj in self.objs]

    def md(self, name=None, err= True, text=None):
        if text: md(text)
        else   : md('以上より, %s $%s$ を求めると, 次のようになる.'%(name if name else '', self.get_var().tex_name(rm=False)))
    ###  Markdown自動出力 -------------------------------------------------------
    def auto(self, f_num=0):
        vars_str = ''
        for i, var in enumerate(self.vars.keys()):
            if i==0: vars_str  = sym.latex(var)
            else   : vars_str += ', '+sym.latex(var)
        md('{}{}を代入して{}を求めると, 次のようになる.'.format(
            ['式({})に'.format(f_num) if f_num else ''][0], vars_str, sym.latex(self.ans.var)))

    def mkdf(self, cap='全項目の計算結果', index=None, ref=''):
        md(r'全項目の計算結果を下表にまとめた.単位は $\mathrm{%s}$ である.'%self.objs[0].ans.rm)
        if index: pass
        data = {}
        for i, obj in enumerate(self.objs):
            data['%s回目'%(i+1)] = r'($%s\pm %s$)/$\mathrm{%s}$'%(
            to_sf(obj.ans_val, 3), to_sf(obj.err_val,1,up=1), obj.ans.rm)
        caption(cap)
        display( pd.DataFrame(data, index=['']) )
