from jack_tokenizer import JackTokenizer
from compilation_engine import CompilationEngine
import shutil
import sys
import os
import glob

os_dir = os.path.split(os.path.realpath(__file__))[0] + "/OS"

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <directory | .jack file>")

    files = []
    if sys.argv[1].endswith(".jack"):
        files.append(sys.argv[1])
    elif os.path.isdir(sys.argv[1]):
        files.extend(glob.glob(f"{sys.argv[1]}*.jack"))
        if not files:
            raise Exception(f"No .jack files found in directory {sys.argv[1]}")
    else:
        raise Exception("Error: target must be a .jack file or a directory")

    print("Copying OS files...")
    os_files = []
    os_files.extend(glob.glob(f"{os_dir}/*.vm"))

    for f in os_files:
        if os.path.isdir(sys.argv[1]):
            shutil.copy(f, sys.argv[1])
        else:
            shutil.copy(f, os.path.split(sys.argv[1])[0] + "/")

    print("Compiling...")
    for f in files:
        print(f"compiling '{f}'")
        with open(f.strip("/.jack") + ".vm", "w") as outfile:
            with open(f, "r") as infile:
                t = JackTokenizer(infile)
                c = CompilationEngine(t, outfile)
                c.compile_class()
                print(f"'{f}' successful.")
    print("Success.")
