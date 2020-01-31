import math
import numpy  as np
import sympy  as sym
import pandas as pd
from sympy import sqrt,sin,cos,tan,exp,log,diff
from pyperclip import copy
from pyperclip import paste
from IPython.display import display, Math, Latex, Image, Markdown, HTML
### my create
from .util.base  import eff_dig, to_sf, align_asta_latex
from .util.calc  import weighted_mean, uncrt
from .util.disp  import df_to_sf, rslt_ans, rslt_ans_array, rslt_ans_align
from .util.symb   import *


### sub process ------------
def dollar(arr):
    return [' $%s$ '%v for v in arr] if type(arr)!=type('') else ' $%s$ '%arr
def mark_number(text):
    rslt = text
    nums = [0,1,2,3,4,5,6,7,8,9,"pi"]
    for i,j in zip(['%s'%i for i in nums], ['{#%s#}'%i for i in nums]):
        rslt = rslt.replace(i,j)
    return rslt.replace("#}{#", "")
### core process -----------
''' Var object--------------------------------------------------------------------
-----------------------------------------------------------------------------'''
class Var:
    ### set
    def __init__(self, var=sym.Symbol('x')):
        ### base ---------------------------------
        self.var = var ### var  type is sym.Symbol
        self.val = 0   ### val  type is float
        self.dig = 3   ### dig  type is int
        self.rm  = ''  ### rm   type is str
        ### err --------------------------------
        self.array = np.array([0])  ### vals type is np.array
        self.err = 1             ### err  type is float
        self.todiff= None           ### todiff type is sym.Symbols of (pa_*func)/(pa_*self.var)
        self.diffed= None           ### diffed type is diffed function of sym.Symbol by self
    ### init process -----------------------------------------------------------
    def set_var(self, var=None, val=None, rm=None, dig=None):
        if val is not None: self.set_array(val)
        if var: self.var = var
        if rm : self.rm  = str(rm)
        if dig: self.dig = int(dig)
    def set_array(self, val):
        self.array = np.array(val)
        if  self.array.size==1:
            self.val = val
            self.err = 0
            self.dig = eff_dig(self.val)
        else:
            self.val = np.mean(val)
            self.err = np.std(val)/np.sqrt(len(val)-1)
            self.dig = eff_dig(self.array[0])
    ### err process ----------------------------------------------------------
    def set_diff(self, ans_obj, function):
        self.todiff= sym.Symbol(r'(\frac{{ \partial {} }}{{ \partial {} }})^2'.format(sym.latex(ans_obj.var),sym.latex(self.var)))
        self.diffed= sym.diff(function, self.var)**2;   ### display(self.diffed)
    ### latex subs process -----------------------------------------------------
    def subs_str(self, func):return func.subs(self.var, '%'+sym.latex(self.var)+'%')###vars to vars or str   : varをマーキング
    def subs_ans(self, func):return func.subs(self.var, self.val)                   ###vars to vars or float: varに数値を代入
    def subs_val(self, func):return func.subs(self.var, r'%s\mathrm{%s}'%(round(self.val,self.dig),self.rm) )###vars to vars or str   : varにstr(数値.round)+単位を代入
    def tex     (self)      :return r'%s'        %sym.latex( self.var )
    def d_tex   (self)      :return r'\Delta{%s}'%sym.latex( self.var )
    def tex_name(self,err=True, rm=True):
        text = r'%s\pm %s'%(self.tex(),self.d_tex()) if err else self.tex()
        return r'%s(%s)%s'%('(' if rm else '', text, r'/\mathrm{%s}'%self.rm if rm else '')
    ### latex output process ---------------------------------------------------
    def df(self, df_name='', name=''):
        ### md('%s回計測した%s $%s$ を記すと, 以下の表を得る.'%( self.array.size, (name if name else ''), self.tex()))
        data = {'%s'%name:self.array}
        df = pd.DataFrame(data, index=['']*len(self.array))
        return df.T
    def latex_mean(self, max=10, cp=True, nb=True):
        denom =  ''
        N=self.array.size
        for i in range(N):
            if i != 0 :denom=denom+'+'
            if i >=max:denom=denom+'..';break
            denom += r'%s \mathrm{%s}' %(to_sf(self.array[i],self.dig), self.rm)
        display( frac(denom,str(N),np.mean(self.array),self.tex(),self.rm,cp=True,nb=True))
    def latex_err(self, cp=True, nb=True):
        N=self.array.size ;m=to_sf(np.mean(self.array), self.dig);
        s = r'\sqrt{\frac{1}{%s\cdot%s}\sum_{i=1}^%s(%s_i-%s)^2}'%(N, N-1, N, self.tex(), m)
        display( to_latex(s, uncrt(self.array), self.d_tex(), self.rm, self.dig, cp=True,nb=True) )
    def latex(self, max=10, cp=True, nb=True):
        if self.err:
            self.latex_mean(max, cp, nb)
            self.latex_err(cp, nb)
            rslt_ans_align( self.val, self.err, self.tex_name(rm=False), self.rm, self.dig )
''' Eq object ------------------------------------------------------------------
  * This object responsible for processing
-----------------------------------------------------------------------------'''
class Eq:
    def __init__(self, leq, req, ans_sym=None, label='', **kwargs):
        ### 設定
        self.label      = label              ### to_latex用
        self.func    , self.todiff  , self.diffed   = [None]*3### diff: functionとsyn
        self.subs_str, self.subs_val, self.subs_ans = [None]*3###
        self.func_val, self.func_ans, self.func_rslt= [None]*3### Latex用
        self.syn_val , self.syn_ans , self.syn_rslt = [None]*3### syn : 合成不確かさ用
        self.eq         = sym.Eq(leq, req)   ### 方程式
        self.vars       = {}                 ### 方程式を構成する変数の辞書.
        self.ans        = None               ### ans tyoe is Var obj
        self.ans_val    = 0
        self.err_val    = 0
        if ans_sym: self.set_func(self.vars[ans_sym].var)### ans = Var();self.ans.set_var(leq)
        elif leq in self.vars: self.set_func(self.vars[leq].var)
    ### latex process ----------------------------------------------------------
    def latex(self, cp=True, nb=True, rqs=[1]*5):
        self.set_tex()
        eqs = [self.ans.var, self.func, self.func_val, self.func_ans, self.func_rslt]
        latex_text = align_asta_latex([e for r,e in zip(rqs, eqs) if r], cp, nb)
        if nb: display(latex_text)
        else    : return latex_text
    ### error mainprocess ----------------------------------------------------------
    def syn(self, cp=True, nb=True, sub_val=True):
        self.set_syn()
        eqs = [self.ans.d_tex(),sym.latex(self.todiff),
                                sym.latex(self.diffed),
                               (self.syn_val if sub_val else None),
                                self.syn_ans,
                                self.syn_rslt,]
        latex_text = align_asta_latex(eqs,cp, nb)
        if nb: display( latex_text )
        else    : return latex_text
    ### init setting -----------------------------------------------------------
    def set_var  (self, obj)      : self.vars[obj.var]   = obj### 辞書varsに追加
    def set_err(self, var, err) : self.vars[var].err = err
    def set_func (self, ans_sym=None) :
        if ans_sym : self.ans = self.vars[ans_sym]                    ### 入力があったらself.ansの変更
        if self.ans: self.func = sym.solve( self.eq, self.ans.var )[0]### 方程式から関数へ変形
        else       : print("please set ans_var_object as 'eq_obj.set_ans( var_obj )'")
    def set_ans  (self, obj)      : self.set_func(obj.var); self.ans= obj       ### 非推奨.未使用
    def set_eq   (self, leq, req) : self.eq=sym.Eq(leq, req);self.set_func()    ### 非推奨.未使用
    def set_obj (self, var=None, val=None, rm='', dig= 3, ans=False):
        obj = Var()
        obj.set_var(var, val, rm, dig)
        self.set_var(obj)
        if (val is None) or ans: self.set_func(obj.var)### set_ansだとfuncがNoneのままなので注意
    def set_err(self, var, err):self.vars[var].err = err       ### 非推奨
    ### manage process ---------------------------------------------------------
    def not_setting_obj(self):    ### set_objされていない変数をreturn
        return [v for v in self.eq.atoms(sym.Symbol)if not v in self.vars]
    def status(self): ### eqの代入状態を返す
        for v in self.not_setting_obj(): print('{0} is not setting. please run "f.set_obj({0})"'.format(v))
        display(pd.DataFrame({' $%s$ '%sym.latex(var):[ obj.val, r'$\mathrm{%s}$'%obj.rm, obj.dig, var==self.ans.var] for var, obj in self.vars.items() },
                            index=['val', 'rm'  , 'dig'  , 'is ans']).T)
    ### latex sub process ------------------------------------------------------
    ### subs 代入処理
    def set_tex(self, err=False):       ###Sym.subs_str:  vars -> vars or str
        if self.ans is None:_=[self.set_obj(var, None) for var in self.not_setting_obj()]
        self.subs_str = self.func ### 初期化  ### subs str
        for var, obj in self.vars.items():self.subs_str = obj.subs_str(self.subs_str)
        self.subs_ans = self.func ### 初期化 ### subs val and ans(subs_valは使われていない...)
        for var, obj in self.vars.items():self.subs_ans = obj.subs_ans(self.subs_ans);
        self.ans_val  = float(self.subs_ans)
        self.func_val = sym.latex(self.subs_str)  ### self.func_valの初期化
        self.func_val = mark_number(self.func_val)### 数字をマーキング
        for var, obj in self.vars.items():        ### 変数マーキング+数値代入
            txt = r'{# %s\mathrm{%s} #}'%(to_sf(float(obj.val), int(obj.dig)), obj.rm)
            self.func_val = self.func_val.replace( '%s'%obj.tex(), txt)
            #print("\t1", to_sf(float(obj.val), int(obj.dig))  , '\t\t', txt )
            #print("\t2",'{#%s#}'%obj.tex(),"\t\t",'{#%s#}'%txt, '\t\t', self.func_val)
        self.func_val = self.func_val.replace(' ','').replace('#}{#', r'\times').replace('{#','').replace('#}','')
        self.func_ans = r'%s\mathrm{%s}'%(to_sf(self.ans_val, self.ans.dig*2),self.ans.rm)
        self.func_rslt= r'%s\mathrm{%s}'%(to_sf(self.ans_val, 1 if err else self.ans.dig,up=True),self.ans.rm)
    def set_syn(self):pass

    def ans_align(self):
        rslt_ans_align(self.ans_val, self.err_val, self.ans.tex_name(rm= False), self.ans.rm, self.ans.dig)

    """TODO
    def set_syn(self)
        for i, [var, obj] in enumerate(self.vars.items()):
            obj.set_diff(self.ans, self.func) ### Var()によるtodiffとdiffedのリセット
            diff_new = [Delta_(var)**2*obj.todiff, Delta_(var)**2*obj.diffed]
            if var is self.ans.var  :pass
            elif float(obj.err)<=0:pass
            elif self.todiff is None or self.diffed is None: self.todiff, self.diffed= diff_new
            else     : self.todiff, self.diffed= [self.todiff+diff_new[0], self.diffed+diff_new[1]]
        self.todiff = self.ans.var*sqrt(self.todiff)
        self.diffed = self.ans.var*sqrt(self.diffed)
        ### saved past value-------------------------
        past_eq   = self.eq
        past_func = self.func.copy()
        past_vars = self.vars.copy()
        past_ans  = self.ans;### print(past_ans.var)
        past_rslt = self.ans_val
        ### set err ---------------------------------
        self.set_eq ( Delta_(past_ans.var), self.diffed)### print(sym.sympify(self.diffed).atoms(sym.Symbol))
        self.set_obj( Delta_(past_ans.var), None, past_ans.rm, past_ans.dig, ans=1)
        for var, obj in past_vars.items():
            obj.set_diff(self.ans, self.func) ### Var()によるtodiffとdiffedのリセット
            self.set_obj( Delta_(var), obj.err, obj.rm, obj.dig)
        self.set_obj(past_ans.var , past_rslt, past_ans.rm, past_ans.dig, ans=0)
        self.set_tex(err=True);
        self.syn_val =self.func_val
        self.syn_ans =self.func_ans
        self.syn_rslt=self.func_rslt
        self.err_val =self.ans_val ### register the new value
        ### reset value -----------------------------------
        self.eq   = past_eq
        self.func = past_func
        self.vars = past_vars
        self.ans  = past_ans
        self.ans_val = past_rslt"""
