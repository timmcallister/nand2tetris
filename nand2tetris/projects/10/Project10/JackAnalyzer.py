#!/usr/bin/python
import os
import sys
from tokenizer import JackTokenizer
from compengine import CompilationEngine

def main():
    arg_len = len(sys.argv)
    file_list = []
    output_file_list = []
    tokenizers = []
    compengines = []

    if arg_len == 1:
        dir_name = os.getcwd()
        for f in os.listdir(dir_name):
            if f.endswith(".jack"):
                file_list.append(f)
                output_file_list.append(os.path.splitext(f)[0] + ".xml")
        if not file_list:
            print("Error, no .jack files in current directory")
            return
    elif arg_len == 2:
        if os.path.isdir(sys.argv[1]):
            for f in os.listdir(sys.argv[1]):
                if f.endswith(".jack"):
                    file_list.append(f)
                    output_file_list.append(os.path.splitext(f)[0] + ".xml")
            if not file_list:
                print("Error, no .jack files in given directory")
                return
            file_list = [sys.argv[1] + "/" + f for f in file_list]
            output_file_list = [sys.argv[1] + "/" + f for f in output_file_list]
        else:
            if os.path.splitext(sys.argv[1])[1] != ".jack":
                print("Error, .jack file not specified")
                return
            else:
                file_list.append(sys.argv[1])
                output_file_list.append(os.path.splitext(sys.argv[1])[0] + ".xml")
    try:
        tokenizers = [JackTokenizer(f) for f in file_list]
        compengines = [CompilationEngine(f) for f in output_file_list]
    except IOError as e:
        print(e)
        return
    
    for t in tokenizers:
        t.has_more_tokens()
    
    for c in compengines:
        c.compile_class()
                

main()