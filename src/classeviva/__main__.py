import os
import sys
import webbrowser


if __name__ == "__main__":
    if (len(sys.argv) > 1):
        if (sys.argv[1] in {"--help", "--version"}):
            os.system("python -m pip show classeviva.py")
    else:
        webbrowser.open("https://pypi.org/project/classeviva.py/")