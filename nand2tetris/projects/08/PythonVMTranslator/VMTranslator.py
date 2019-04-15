#!/usr/bin/python
import os
import sys
from parser import Parser
from codewriter import CodeWriter


def main():
    arg_len = len(sys.argv)
    file_list = []
    output_file = ""
    parsers = []

    if arg_len == 1:
        dir_name = os.getcwd()
        output_file = dir_name + '/' + dir_name.split('/')[-1] + ".asm"
        for f in os.listdir(dir_name):
            if f.endswith(".vm"):
                file_list.append(f)
        if not file_list:
            print("Error, no .vm files in current directory")
            return
    elif arg_len == 2:
        if os.path.isdir(sys.argv[1]):
            output_file = sys.argv[1] + sys.argv[1].split('/')[-2] + ".asm"
            for f in os.listdir(sys.argv[1]):
                if f.endswith(".vm"):
                    file_list.append(f)
            if not file_list:
                print("Error, no .vm files in given directory")
                return
            file_list = [sys.argv[1] + "/" + f for f in file_list]
        else:
            if os.path.splitext(sys.argv[1])[1] != ".vm":
                print("Error, .vm file not specified")
                return
            else:
                file_list.append(sys.argv[1])
                output_file = os.path.splitext(sys.argv[1])[0] + ".asm"
    try:
        writer = CodeWriter(output_file)
    except IOError as e:
        print("In codewriter: ")
        print(e)
        return
    else:
        try:
            parsers = [Parser(f) for f in file_list]
        except IOError as e:
            print("In parsers: ")
            print(e)
            return
        else:
            writer.write_init()
            for p in parsers:
                writer.set_file_name("TODO")
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
