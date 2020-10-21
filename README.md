
# ExPy


The sophisticated tool needed for scientific computing.

- **Documentation:** https://tsei.jp/expy
- **Source code:** https://github.com/tseijp/expy
- **Contributing:** https://github.com/tseijp/expy/pulls
- **Bug reports:** https://github.com/tseijp/expy/issues
- **Website:** ~https://tsei.jp/expy~
- **Contact** ~contact@tsei.jp~

It provides:

 - useful rendering formula, Formula deformation.
 - simply converting Jupyter notebook to PDF.

To get the latest version :

- from https://pypi.python.org/project/expy-python/
- `$ pip install expy-python`

To get the latest version do:

- `$ git clone git://github.com/YouseiTakei/expy.git`
- `$ cd expy`
- `$ python setup.py install`

From this directory, start Jupyter notebook and:
```python
>>> from expy  import F, x_, y_,
>>> f = F(y_, x_**x_)
>>> f.set(x_, 0)
>>> f()
```

Convert your Jupyter notebook. start cmd line and:
```cmd
$ expy -a -p -t
```

Usage Example:

|Usage|Detail|  
|`expy -h`| check args help|  
|`expy -i test.ipynb`| convert to pdf|  
|`expy -a test_dir  `| convert all file in your directory|  
|`expy -r test.pdf  `| remove converted pdf file or all files in directory|  
|`expy -i test.ipynb -o html`| convert to html|  
|`expy -a test_dir   -o html`| convert all files to html|  
|`expy -r test_dir   -o html`| remove all html files in directory|  
|`expy -i test.ipynb -p result\today\    `| use output path|  
|`expy -i test.ipynb -t data\article.tplx`| use your template|  

Other Usage Hints:
- If you want to change template file, you can edit file in `~/.expy/latex/article.tplx`
- If you don't have auth and can't install this, you can use `$pip install expy-python --user`
- If you can't convret pd.DataFrame, you should run 'expy.init_ep()'
