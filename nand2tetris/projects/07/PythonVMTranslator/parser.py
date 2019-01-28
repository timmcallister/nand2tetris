class Parser:
    def __init__(self, file_name, file_ext):
        with open(file_name + file_ext, 'r') as input_file:
            self.commandList = input_file.readlines()

    def hasMoreCommands(self):
        pass

    def advance(self):
        pass

    def command_type(self):
        pass

    def arg1(self):
        pass
    
    def arg2(self):
        pass

    