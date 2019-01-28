import sys, os
from parser import Parser
from codewriter import CodeWriter

def main():
    if len(sys.argv) == 2:
        file_name = os.path.splitext(sys.argv[1])[0]
        file_ext = os.path.splitext(sys.argv[1])[1]

    if len(sys.argv) != 2 or file_ext != ".vm":
        print("Usage: translator.py <inputFile>.vm")
        return

    try:
        parser = Parser(file_name, file_ext)
        writer = CodeWriter(file_name)
    except IOError as e:
        print(e)
        return
    else:
        pass


main()
