import sys
import webbrowser
import subprocess


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in {"--help", "--version"}:
            subprocess.run("python -m pip show classeviva.py")
    else:
        webbrowser.open("https://pypi.org/project/classeviva.py/")