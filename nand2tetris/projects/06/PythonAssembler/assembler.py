#!/usr/bin/python
import sys, os
from parser import Parser
from code import Code


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
        outputList = []
        p.stripComments()

        
        while p.hasMoreCommands():
            outputLine = ""
            p.advance()
            if p.currentCommand != '':
                if p.commandType() == "A_COMMAND":
                    outputLine = "{0:016b}".format(int(p.symbol()))
                elif p.commandType() == "L_COMMAND":
                    pass
                elif p.commandType() == "C_COMMAND":
                    outputLine = "111" + c.getComp(p.comp()) + \
                    c.getDest(p.dest()) + c.getJump(p.jump())
                outputLine = outputLine + "\n"
                outputList.append(outputLine)


    with open(fileName + ".hack", "w") as writeOut:
        writeOut.writelines(outputList)

def firstPass():
    pass

def secondPass():
    pass

main()
