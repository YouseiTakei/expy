# import math
# import numpy as np
# import matplotlib.pyplot as plt
# from pyperclip import copy
# from pyperclip import paste
import pandas as pd
from IPython.display import display, Latex, Image
# my created
from .util.core import df_to_sf


class Md():
    def __init__(self, s):
        self.s = s

    def _repr_html_(self):
        return '%s' % self.s

    def _repr_latex_(self):
        return '\n %s \n' % self.s


class Caption():
    def __init__(self, s=''):
        self.s = s

    def _repr_html_(self):
        return '<center> %s </center>' % self.s

    def _repr_latex_(self):
        return '\\begin{center}\n %s \n\\end{center}' % self.s


class Df():
    def __init__(self, data=None, sheet='Sheet1', dig=None, col=None, cap=None):
        self.dig = dig
        self.data = None
        self.df = None
        self.columns = None
        self.caption = None
        self.set(data, sheet, dig, col, cap)

    # core -------------------------------------------------------------------
    def __call__(self, tiny=False):
        if tiny:
            display(Latex(r'\tiny'))
        if self.caption:
            display(Caption(self.caption))
        if self.dig:
            display(df_to_sf(self.get(), dig=self.dig))
        else:
            display(self.get())
        if tiny:
            display(Latex(r'\normalsize'))

    # get --------------------------------------------------------------------
    def get(self):
        df = self.df.copy()
        if self.columns:
            df = self.get_drop(df)
            df = self.get_rename(df)
        return df.rename(index={i: "" for i in list(df.index)}, inplace=False)

    # sub process --------------------
    def get_drop(self, df):
        return df.drop(columns=[i for i, v in self.columns.items() if v == None], inplace=False)

    def get_rename(self, df):
        return df.rename(columns={i: v for i, v in self.columns.items() if v != None}, inplace=False)

    # set --------------------------------------------------------------------
    def set(self, data=None, sheet='Sheet1', dig=None, col=None, cap=None):
        if data is not None:
            self.set_data(data, sheet)
        if dig:
            self.dig = dig
        if col:
            self.set_col(col)
        if cap:
            self.set_cap(cap)

    # sub process --------------------
    # データの読み取りとバックアップ
    def set_data(self, data, sheet='Sheet1'):
        if type(data) is pd.core.frame.DataFrame:
            self.data = data.copy()
        if type(data) is str:
            self.data = pd.read_excel(data, index=1, sheet_name=sheet)
        if type(data) is dict:
            self.data = pd.DataFrame(data)
        if type(self.data) is pd.core.frame.DataFrame:
            self.df = self.data.copy()

    def set_col(self, name, rename=None):
        if type(name) == dict:
            self.columns = name
        if type(name) == str:
            self.columns[name] = rename

    def set_cap(self, caption):
        self.caption = caption
    # ------------------------------------------------------------------------


class Fig():
    def __init__(self, data=None, sheet='Sheet1', dig=None, col=None, cap=None):
        self.df = None
        self.caption = None
        self.filepath = None
        self.set(data, sheet, dig, col, cap)

    def __call__(self, is_tiny=False):
        if self.filepath:
            display(Image(self.filepath))
        if self.caption:
            display(Caption(self.caption))

    # get --------------------------------------------------------------------
    def get(self):
        return self.df

    # sub process--------------------
    def get_plot(self):
        pass

    # set --------------------------------------------------------------------
    def set(self, data=None, sheet='Sheet1', dig=None, col=None, cap=None):
        if data is not None:
            self.set_data(data, sheet, dig, col, cap)
        if cap:
            self.set_cap(cap)

    # sub process --------------------
    # データの読み取りとバックアップ
    def set_data(self, data, sheet, dig, col, cap):
        if type(data) is pd.core.frame.DataFrame:
            self.df = Df(data, sheet, dig, col, cap)
        if type(data) is type(Df()):
            self.df = data
        if type(data) is str:
            self.filepath = data

    def set_cap(self, caption):
        self.caption = caption
