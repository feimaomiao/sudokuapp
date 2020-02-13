"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""
from setuptools import setup

APP = ['sudoku.py']
DATA_FILES = ['exe', 'exe/sudoku.png']
OPTIONS = {
	'argv_emulation': True,
	'includes':['tkinter', 'os','copy','time','random','errno','signal','functools'],
	'packages': ['exe','PIL'],
	# 'excludes': ['PyQt5']
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
