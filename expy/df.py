import math
import numpy  as np
import pandas as pd
#import sympy  as sym
import matplotlib.pyplot as plt
from pyperclip import copy
from pyperclip import paste
from IPython.display import display, Latex
### my created
from .util.disp import df_to_sf

class Md():
    def __init__(self,s):
        self.s = s
    def _repr_html_(self):
        return '%s' % self.s
    def _repr_latex_(self):
        return '\n %s \n' % self.s

class Caption():
    def __init__(self,s= ''):
        self.s = s
    def _repr_html_(self):
        return '<center> %s </center>' % self.s
    def _repr_latex_(self):
        return '\\begin{center}\n %s \n\\end{center}' % self.s

class Df():
    def __init__(self, data=None, dig=None, sheet='Sheet1', col=None, cap=None):
        self.dig     = dig
        self.data    = None ### 元データの保管用
        self.df      = None ### 処理を加える
        self.columns = None
        self.caption = None
        self.set(data, sheet, dig, col, cap)
    ### core -------------------------------------------------------------------
    def __call__(self):
        if self.caption:display(Caption(self.caption))
        if self.dig:display(df_to_sf(self.get(), dig=self.dig))
        else:display(self.get())
    ### get --------------------------------------------------------------------
    def get(self):
        if self.columns: self.df = self.get_drop()
        if self.columns: self.df = self.get_rename()
        return self.df.rename(index={i:"" for i in list(self.df.index)},inplace=False)
    ### sub process
    def get_drop(self)  : return self.df.drop  (columns=[i   for i,v in self.columns.items() if v==None], inplace=False)
    def get_rename(self): return self.df.rename(columns={i:v for i,v in self.columns.items() if v!=None}, inplace=False)
    ### set --------------------------------------------------------------------
    def set(self, data=None, sheet='Sheet1', dig=None, col=None, cap=None):
        if data is not None: self.set_data(data, sheet)
        if dig: self.dig = dig
        if col: self.set_col(col)
        if cap: self.set_cap(cap)
    ### sub process
    def set_data(self, data, sheet='Sheet1'):    ### データの読み取りとバックアップ
        if type(data) is pd.core.frame.DataFrame: self.data=data.copy()
        if type(data) is str :self.data = pd.read_excel(data, index=1, sheet_name=sheet)
        if type(data) is dict:self.data = pd.DataFrame(data)
        if type(self.data) is pd.core.frame.DataFrame:self.df = self.data.copy()
    def set_col(self, name, rename=None):
        if type(name)==dict: self.columns      = name
        if type(name)==str : self.columns[name]=rename
    def set_cap(self, caption):self.caption = caption
    ### ------------------------------------------------------------------------
