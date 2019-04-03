class CodeWriter:

    label_number = 0

    def __init__(self, output_file_name):
        self.command_list = []
        self.output_file = open(output_file_name + ".asm", 'w')

    def write_arithmetic(self, operation):
        pass

    def write_push_pop(self):
        pass

    def close(self, file_name):
        self.output_file.writelines(self.command_list)
        self.output_file.close()

    @classmethod
    def increment_label(cls):
        cls.label_number += 1
