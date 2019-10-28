
Prerequisites
=============

Before reading this tutorial you should know a bit of Python.
If you would like to refresh your memory, take a look at the Python tutorial.

If you wish to work the examples in this tutorial,
you must also have some software installed on your computer.
Please see https://scipy.org/install.html for instructions.


The Basics
==========
```python
>>> from expy import F, x_, y_
>>> f = F(y_, x_**2)
>>> f.set(x_, 3)
>>> f.tex()
```


An example
==========
```python
>>> from expy    import F, x_, y_
>>> from expy.12 import mkdf, mkdf2, al34
>>> data = [1, 2, 2, 1, 4, 1, 2, 1, 2, 3]
>>> al34(data)
```
