class Parser:
    def __init__(self, file_name, file_ext):
        with open(file_name + file_ext, 'r') as input_file:
            self.current_command = -1
            self.command_list = input_file.readlines()
            self.command_list = [x[:x.index("//")] if "//" in x else x
                                 for x in self.command_list]
            self.command_list = ["".join(x.split()) for x in self.command_list]

    def hasMoreCommands(self):
        try:
            self.command_list[self.current_command + 1]
        except IndexError:
            return False
        else:
            return True

    def advance(self):
        self.current_command += 1
        # return self.command_list[self.current_command]

    def command_type(self):
        command = self.command_list[self.current_command].split(' ', 1)[0]
        _math_type_list = ["add", "sub", "neg", "eq",
                           "gt", "lt", "and", "or", "not"]

        if command in _math_type_list:
            return "C_ARITHMETIC"
        else:
            _cmd_type_list = {
                "pop": "C_POP",
                "push": "C_PUSH",
                "label": "C_LABEL",
                "goto": "C_GOTO",
                "if-goto": "C_IF",
                "function": "C_FUNCTION",
                "call": "C_CALL",
                "return": "C_RETURN"
            }

            return _cmd_type_list[command]

    def arg1(self) -> str:
        if self.command_type() == "C_ARITHMETIC":
            return self.command_list[self.current_command].split(' ')[0]
        else:
            return self.command_list[self.current_command].split(' ')[1]

    def arg2(self) -> int:
        return self.command_list[self.current_command].split(' ')[2]
