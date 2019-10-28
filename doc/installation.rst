
Installation
============
ExPy is designed based on SymPy and Pandas, and does require other library to be installed first.
The recommended method of installation is through Anaconda, as well as several other useful libraries.

Anaconda
========

Anaconda is a free Python distribution that includes many more useful packages for scientific computing.
For example, without Matplotlib, only simple text-based plotting is enabled.
If you already have Anaconda and want to update ExPy to the latest version, use:
```
conda update expy
```


Git
===
If you wish to contribute to ExPy or like to get the latest updates, install ExPy from git.
To download the repository, execute the following from the command line:

```bash
git clone https://github.com/expy/expy.git
```

To update to the latest version, go into your repository and execute:

```bash
git pull origin master
```

Run ExPy
========
After installation, it is best to verify that your freshly-installed ExPy works.
To do this, start up Python and import the ExPy libraries:
```python
$ Python
>>> import expy as ep
```

From here, execute some simple ExPy statements like the ones below:

```python
>>> f = ep.F(ep.y_, ep.x_**2)
>>> f.set(ep.x_, 2)
>>> f.tex()
<IPython.core.display.Latex object>
```

XeTeX
=======
If you wish to convert jupyter notebook to pdf, install XeTeX and pass the path.
XeTeX is an extension of TeX that integrates TeX's typesetting capabilities.
The command 'nbconvert' in jupyter does require this library and os path into XeTeX.
If you already have Tex Live, XeTeX is installed at the same time.
