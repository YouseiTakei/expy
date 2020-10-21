import os
import sys
import shutil
import subprocess as sub
def main():
    sub.run("pip uninstall expy".spit(), shell=True, cwd='.')
    sub.run([sys.executable, "setup.py" "check"], shell=True)
    sub.run([sys.executable, "setup.py" "sdist"], shell=True)
    sub.run([sys.executable, "setup.py" "install"], shell=True)

if __name__ == '__main__':
  main()
