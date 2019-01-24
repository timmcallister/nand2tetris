#!/usr/bin/python
import sys, os
from parser import Parser
from code import Code
from symboltable import SymbolTable

# import pdb

def main():

    if len(sys.argv) == 2:
        fileName = os.path.splitext(sys.argv[1])[0]
        fileExt = os.path.splitext(sys.argv[1])[1]

    if len(sys.argv) != 2 or fileExt != ".asm":
        print("Usage: assembler.py <inputFile>.asm")
        return

    try:
        p = Parser(fileName)
    except IOError as e:
        print(e)
        return
    else:
        c = Code()
        s = SymbolTable()
        outputList = []
        p.stripComments()

        #first pass
        labelAddress = 0
        while p.hasMoreCommands():
            p.advance()
            if p.currentCommand != '':
                if p.commandType() == "L_COMMAND":
                    labelSymbol = p.symbol()
                    s.addEntry(labelSymbol, labelAddress)
                else:
                    labelAddress += 1

        #second pass
        n = 16
        p.commandAddr = -1
        p.currentCommand = None
        # pdb.set_trace()
        while p.hasMoreCommands():
            outputLine = ""
            p.advance()
            if p.currentCommand != '':
                if p.commandType() == "A_COMMAND":
                    symbol = p.symbol()
                    if symbol.isdigit():
                        outputLine = "0" + "{0:015b}".format(int(symbol))
                    else:
                        if s.contains(symbol):
                            value = s.getAddress(symbol)
                            outputLine = "0" + "{0:015b}".format(int(value))
                        else:
                            s.addEntry(symbol, n)
                            outputLine = "0" + "{0:015b}".format(n)
                            n += 1
                elif p.commandType() == "C_COMMAND":
                    outputLine = "111" + c.getComp(p.comp()) + \
                    c.getDest(p.dest()) + c.getJump(p.jump())
                if p.commandType() != "L_COMMAND":
                    outputLine = outputLine + "\n"
                    outputList.append(outputLine)

    with open(fileName + ".hack", "w") as writeOut:
        writeOut.writelines(outputList)

main()
