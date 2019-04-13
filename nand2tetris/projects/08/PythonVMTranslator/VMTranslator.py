#!/usr/bin/python
import os
import sys
from parser import Parser
from codewriter import CodeWriter


def main():
    arg_len = len(sys.argv)
    file_list = []

    if arg_len == 1:
        file_name = os.getcwd()
    elif arg_len == 2:
        is_dir = os.path.isdir(sys.argv[1])
        file_name = os.path.splitext(sys.argv[1])[0]
        file_ext = os.path.splitext(sys.argv[1])[1]
        if is_dir:
            for f in os.listdir(file_name):
                if f.endswith(".vm"):
                    file_list.append(f)
                    file_name = file_name + os.path.basename(os.path.dirname(file_name)) 
        else:
            file_list.append(sys.argv[1])
    if arg_len == 1 and not file_list:
        print("Current directory contains no .vm files")
        return
    elif arg_len == 2 and file_ext != ".vm" and not is_dir:
        print("Usage: translator.py <inputFile>.vm")
        return
    elif arg_len == 2 and is_dir and not file_list:
        print("Directory contains no .vm files")
        return
    try:
        writer = CodeWriter(file_name)
    except IOError as e:
        print("In codewriter: ")
        print(e)
        return
    else:
        try:
            file_list = [sys.argv[1] + f for f in file_list]
            parsers = [Parser(f) for f in file_list]
        except IOError as e:
            print("In parsers: ")
            print(e)
            return
        else:
            writer.write_init()
            for p in parsers:
                writer.set_file_name(file_name)
                while p.hasMoreCommands():
                    p.advance()
                    cmd = p.command_type()
                    if cmd != "C_RETURN":
                        argument1 = p.arg1()
                    if cmd in ["C_POP", "C_PUSH", "C_FUNCTION",
                            "C_CALL"]:
                        argument2 = p.arg2()
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
                    elif cmd == "C_FUNCTION":
                        writer.write_function(argument1, int(argument2))
                    elif cmd == "C_CALL":
                        writer.write_call(argument1, argument2)
                    elif cmd == "C_RETURN":
                        writer.write_return()
        writer.close()


main()
