"""Full Doku on: https://github.com/NapoII/OpenCounterAPI"from util.__my_path_funktion__ import *
my_file_path = my_file_path()
"""

import os, sys

class my_file_path:
    def __init__(self):

        self.main_py_path = os.path.abspath(sys.argv[0])

    class json:
        main_py_path = os.path.abspath(sys.argv[0])
        main_py_folder = os.path.dirname(main_py_path)

        # Falls das Skript aus "venv/bin/python" gestartet wird, springe zum Projektordner
        if "venv/bin" in main_py_folder:
            main_py_folder = os.path.abspath(os.path.join(main_py_folder, "../../"))

        data_dir = os.path.normpath(os.path.join(main_py_folder, "data"))


        config_dir = os.path.normpath(os.path.join(main_py_folder, "config"))
        json_dir = os.path.normpath(os.path.join(config_dir, "json"))



