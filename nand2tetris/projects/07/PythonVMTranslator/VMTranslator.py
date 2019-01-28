import sys, os
from parser import Parser
from codewriter import CodeWriter

def main():
    if len(sys.argv) == 2:
        fileName = os.path.splitext(sys.argv[1])[0]
        fileExt = os.path.splitext(sys.argv[1])[1]

    if len(sys.argv) != 2 or fileExt != ".vm":
        print("Usage: translator.py <inputFile>.vm")
        return

main()
