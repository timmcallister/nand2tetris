#! /usr/bin/python3

class Parser:
    def __init__(self, inputFile):
        with open(inputFile + ".asm", 'r') as inFile:
            self.commandList = inFile.readlines()
        self.commandAddr = -1
        self.currentCommand = None
        self.emptyLines = 0

    def stripComments(self):
        self.commandList = [ x[:x.index("//")] if "//" in x else x \
        for x in self.commandList]                                              # completely normal, self-documenting code
        self.commandList = ["".join(x.split()) for x in self.commandList]       # remove ALL white space

    def hasMoreCommands(self):
        try:
            nextCommand = self.commandList[self.commandAddr + 1]
        except IndexError:
            return False
        return True

    def advance(self):
        self.commandAddr += 1
        self.currentCommand = self.commandList[self.commandAddr]

    def commandType(self):
        if self.currentCommand.startswith("@"):
            return "A_COMMAND"
        if self.currentCommand.startswith("("):
            return "L_COMMAND"
        return "C_COMMAND"

    def symbol(self):
        x = self.currentCommand
        if x.startswith("@"):
            return x[1:]
        if x.startswith("("):
            return x[1:-1]

    def dest(self):
        x = self.currentCommand
        if "=" in x:
            return x[:x.index("=")]
        else:
            return ''

    def comp(self):
        x = self.currentCommand
        if "=" in x:
            x = x[x.index("=")+1:]
        if ";" in x:
            x = x[0:x.index(";")]
        return x

    def jump(self):
        x = self.currentCommand
        if ";" in x:
            return x[x.index(";")+1:]
        else:
            return ''
