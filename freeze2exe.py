# encoding = utf-8
__author__ = 'Cyan'

application_title = "TGParser" #what you want to application to be called
main_python_file = "sudoku_gui.py" #the name of the python file you use to run the program

import sys

from cx_Freeze import setup, Executable



includes = [ 'pygame', 'pygame.display','pygame.locals']
packages = []

setup(
        name = application_title,
        version = "0.1",
        description = "Timing Gen Parser",
        options = {"build_exe" : {"includes" : includes}}, #, 'packages':packages }},
        executables = [Executable(main_python_file)])
