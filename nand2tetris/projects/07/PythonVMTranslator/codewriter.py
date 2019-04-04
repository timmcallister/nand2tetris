class CodeWriter:

    self.add_helper = {
        "add": "M=D+M\n",
        "sub": "M=D-M\n",
        "and": "M=D&M\n",
        "or":  "M=D|M\n"
    }

    self.eq_helper = {
        "eq":  "D;JEQ\n",
        "lt":  "D;JLT\n",
        "gt":  "D;JGT\n"
    }

    self.not_helper = {
        "neg": "M=-M\n",
        "not": "M=!M\n"
    }

    self.label_number = 0

    def __init__(self, output_file_name):
        self.command_list = []
        self.output_file = open(output_file_name + ".asm", 'w')

    def write_arithmetic(self, command):
        self.command_list.append("@SP\nAM=M-1\n")
        if command in ["add", "subtract", "and", "or"]:
            self.command_list.append("D=M\nA=A-1\n")
            self.command_list.append(self.add_helper[command] + "\n")
        elif command in ["eq", "gt", "lt"]:
            self.command_list.append("D=M\nA=A-1\nD=M-D\n@TRUE" +
                                     self.label_number + "\n")
            self.command_list.append(self.eq_helper[command] + "\n")
            self.command_list.append("@SP\nA=M-1\nM=0\n@DONE" +
                                     self.label_number + "\n")
            self.command_list.append("0;JMP\n(TRUE" +
                                     self.label_number + ")\n")
            self.command_list.append("@SP\nA=M-1\nM=-1")
            self.command_list.append("(DONE" + self.label_number + ")\n")
        elif command in ["neg", "not"]:
            self.command_list.append(self.not_helper[command] + "\n")

        self.label_number += 1

    def write_push_pop(self, command, segment, index):
        self.command_list.append("@" + index + "\n")
        self.command_list.append("D=A\n@" + segment + "\n")
        if command == "C_PUSH":
            self.command_list.append("A=D+A\nD=M\n@SP\nA=M\nM=D\n@SP/nM=M+1")
        elif command == "C_POP":
            self.command_list("A=D+A\nD=M\n@SP\nM=M-1\n@SP\nA=M\nM=D")

        self.label_number += 1

    def close(self, file_name):
        self.output_file.writelines(self.command_list)
        self.output_file.close()

    # @classmethod
    # def increment_label(cls):
    #     cls.label_number += 1
