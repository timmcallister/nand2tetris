#!/usr/bin/python
import os
import sys
from parser import Parser
from codewriter import CodeWriter


def main():

    if len(sys.argv) == 2:
        file_name = str(os.path.splitext(sys.argv[1])[0])
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
        while parser.hasMoreCommands():
            parser.advance()
            cmd = parser.command_type()
            if cmd != "C_RETURN":
                argument1 = parser.arg1()
            if cmd in ["C_POP", "C_PUSH", "C_FUNCTION",
                       "C_CALL"]:
                argument2 = parser.arg2()
            if cmd == "C_ARITHMETIC":
                writer.write_arithmetic(argument1)
            elif cmd in ["C_POP", "C_PUSH"]:
                writer.write_push_pop(cmd, argument1,
                                      argument2)
            elif cmd == "C_LABEL":
                writer.write_label(argument1)
            elif cmd == "C_GOTO":
                writer.write_goto(argument1)
            elif cmd == "C_IF":
                writer.write_if(argument1)
        writer.close()


main()
