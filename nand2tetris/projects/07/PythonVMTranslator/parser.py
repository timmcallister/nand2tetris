class Parser:
    def __init__(self, file_name, file_ext):
        with open(file_name + file_ext, 'r') as input_file:
            self.commandList = input_file.readlines()

    def hasMoreCommands(self, cmd_list, index):
        try:
            cmd_list[index + 1]
        except IndexError:
            return False
        else:
            return True

    def advance(self, cmd_list, index):
        return cmd_list[index + 1]        

    def command_type(self, command_line):
        command = command_line.split(' ', 1)[0]
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

    def arg1(self, command) -> str:
        return command.split(' ')[1]

    def arg2(self, command) -> int:
        return command.split(' ')[2]
