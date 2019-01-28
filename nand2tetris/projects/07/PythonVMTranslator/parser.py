class Parser:
    def __init__(self, file_name, file_ext):
        with open(file_name + file_ext, 'r') as input_file:
            self.commandList = input_file.readlines()
