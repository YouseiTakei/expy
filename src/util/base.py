""" here is a basic process that is also used many times,
    such as conversion of numerical values ​​and character.

    - expy-python ver.1.2.2 ©tseijp
"""
import math
import numpy as np
import sympy as sym
import pandas as pd
# import matplotlib.pyplot as plt
# from sympy import sqrt, sin, cos, tan, exp, log, diff
# from IPython.display import Markdown, Latex, Math
from pyperclip import copy
# from pyperclip import paste

# the process for digit -----------------------------------------------
# 丸め
def roundup(x, dig=2):
    def roundup_unit(x):
        return (math.ceil(x*(10**dig))) / (10**dig)
    return to_multi_d(roundup_unit, x, 0)


def rounder(x, dig=2):
    def rounder_unit(x):
        return round(x, dig)
    return to_multi_d(rounder_unit, x, 0)


# 桁数
def num_dig(x):
    y = abs(x)+abs(x)*0.0000000000001
    if y >= 1:
        return np.floor(np.log10(float(y)))
    if 1 > y > 0:
        return -np.floor(np.log10(float(1/y))+1)
    if y == 0:
        return 0


# 有効数字何桁か
# e.g. 0.03412/100000 -> 4
def eff_dig(num):
    num_str = str(num * (10 ** -num_dig(num)))
    num_i, num_d = num_str.split('.') if '.' in num_str else (num_str, '0')
    if '0000'in num_d:
        num_d = num_d.split('0000')[0]
    elif '9999'in num_d:
        num_d = num_d.split('9999')[0]
    return len(num_d)+1


# 有効n桁 (return float)
# this is used in tex.py
def sgnf(n_in, num_sgnf=3):
    dig = num_dig(n_in)
    n_rslt = n_in * (10**(-dig))
    n_rslt = np.round(float(n_rslt), int(num_sgnf-1))
    n_rslt = n_rslt * (10**(dig))
    return n_rslt


# 多次元化 for df_to_sf
def to_list(data):
    if type(data) is type(pd.Series([])):
        return data.values.tolist()
    if type(data) is type(pd.DataFrame([])):
        return data.values.tolist()
    if type(data) is type(np.array([])):
        return data.tolist()
    else:
        return data


# 有効数字化
def to_sf(n_in, sf_in=None, up=False):
    dig = num_dig(n_in)
    sf = sf_in if sf_in is not None else eff_dig(n_in)
    n_rslt = n_in * (10**(-dig))
    if up:
        n_rslt = roundup(float(n_rslt), int(sf-1))
    else:
        n_rslt = np.round(float(n_rslt), int(sf-1))

    if dig == 0:
        return '%s' % roundup(n_in, sf-1) if up else np.round(n_in, sf-1)
    if dig == 1:
        return r'%s\times 10' % (n_rslt)
    return r'%s\times 10^{%s}' % (n_rslt, int(dig))


# latex ----------------------------------------------------------------------
def align_asta_latex(unit=[], cp=False, nb=True):
    tex = ""
    for i in range(len(unit)):
        if unit[i]:
            if i != 0:
                tex += '\n\t&='
            tex += sym.latex(unit[i])
            if i != 0:
                tex += r'\\'

    tex = r'\begin{align*}'+'\n\t'+tex+'\n\t'+r'\end{align*}'

    if cp:
        copy(tex)
    if nb:
        return Latex(tex)
    else:
        return tex


def to_latex(s='x^2+y^2', ans=0, x='z', rm='', dig=3, cp=False, nb=True, label=''):
    return align_asta_latex([
        '%s' % x, '%s' % s, r'%s\mathrm{%s}' % (to_sf(ans, dig*2), rm),
        r'%s\mathrm{%s}' % (to_sf(ans, dig), rm)
    ], cp, nb)


def frac(denom, numer, ans=0, x='z', rm='', dig=3, cp=True, nb=True, label=''):
    return to_latex(r'{\tiny \frac{%s}{%s}}' % (denom, numer), ans, x, rm, dig, cp, nb, label)


def mean_disp(data, x='%%', rm='%%', cp=True, nb=True, label=''):
    denom = ''
    for i in range(len(data)):
        if i != 0:
            denom = denom + '+'
        denom += str(data[i])+rm
    return frac(denom, str(len(data)), np.mean(data), x, rm, cp, label)


def uncrt_disp(data, x='%%', rm='%%', cp=True, nb=True, label=''):
    N = len(data)
    m = np.mean(data)
    u = uncrt(data)
    s = '\\sqrt{\\frac{1}{' + str(N) + '\\cdot' + str(N-1) + '}\\sum_{i=1}^' + str(N) + '(' + x + '_i-' + str(m) + ')^2}'
    return to_latex(s, uncrt(data), r'\Delta' + x, rm, p, label)


def weighted(mean_all, uncrt_all, x='z', rm='', dig=3, cp=True, nb=True, label=''):
    display(tex_weighted_mean (mean_all, uncrt_all, x, rm, cp, nb, label))
    display(tex_weighted_uncrt(mean_all, uncrt_all, r'\Delta '+x, rm, cp, nb, label))

    def tex_weighted_mean(mean_all, uncrt_all, x='z', rm='', cp=True, nb=True, label=''):
        denom = ''
        numer = ''
        for i in range(len(mean_all)):
            denom += '\\frac{%s}{(%s)^2}' % (to_sf(mean_all[i], dig), to_sf(uncrt_all[i], dig))
            numer += '\\frac{1}{(%s)^2}' % to_sf(uncrt_all[i], dig)
            if i != len(mean_all)-1:
                denom += '+'
                numer += '+'
        return frac(denom, numer, weighted_mean(mean_all, uncrt_all)[0], x, rm, dig)

    def tex_weighted_uncrt(mean_all, uncrt_all, x='z', rm='', cp=True, nb=True, label=''):
        numer = '\\sqrt{'
        for i in range(len(mean_all)):
            numer += '\\frac{1}{(%s)^2}' % to_sf(uncrt_all[i], dig)
            if i != len(mean_all) - 1:
                numer += '+'
            if i == len(mean_all) - 1:
                numer += '}'
        return frac('1', numer, weighted_mean(mean_all, uncrt_all)[1], x, rm, dig)
