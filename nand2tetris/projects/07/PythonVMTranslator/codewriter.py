class CodeWriter:

    self.label_number = 0

    def __init__(self, output_file_name):
        self.command_list = []
        self.output_file = open(output_file_name + ".asm", 'w')

    def write_arithmetic(self, command):
        self.label_number += 1

    def write_push_pop(self, command, segment, index):
        self.label_number += 1

    def close(self, file_name):
        self.output_file.writelines(self.command_list)
        self.output_file.close()

    # @classmethod
    # def increment_label(cls):
    #     cls.label_number += 1
