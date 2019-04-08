class CodeWriter:

    def __init__(self, output_file_name):
        self.command_list = []
        self.file = output_file_name.split("/")[-1]
        self.output_file = open(output_file_name + ".asm", 'w')
        self.label_number = 0

        self.pushd = [
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]

        self.popd = [
            "@SP",
            "AM=M-1",
            "A=M",
            "A=A+D",
            "D=A-D",
            "A=A-D",
            "M=D"
        ]

        self.binary_op = {
            "add": "M=D+M",
            "sub": "M=M-D",
            "and": "M=D&M",
            "or":  "M=D|M"
        }

        self.jump_op = {
            "eq":  "D;JEQ",
            "lt":  "D;JLT",
            "gt":  "D;JGT"
        }

        self.unary_op = {
            "neg": "M=-M",
            "not": "M=!M"
        }

        self.latt = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT"
        }

    def set_segment(self, cmd_type, segment, index):
        line = []

        if segment in self.latt:
            segment = self.latt[segment]

        if segment == "temp":
            line = [
                "@" + str(5 + int(index))
            ]
        elif segment == "constant":
            line = [
                "@" + index,
                "D=A"
            ]
        elif segment == "static":
            line = [
                "@" + self.file + "." + index
            ]
        elif segment == "pointer":
            if index == "0":
                line = [
                    "@THIS"
                ]
            else:
                line = [
                    "@THAT"
                ]
        else:
            line = [
                "@" + index,
                "D=A",
                "@" + segment,
                "A=D+M"
            ]
        if cmd_type == "C_PUSH" and segment != "constant":
            line.append("D=M")
        elif cmd_type == "C_POP":
            line.append("D=A")

        return line

    def write_arithmetic(self, command):
        if command in self.unary_op:
            lines = [
                "@SP",
                "AM=M-1",
                self.unary_op[command],
                "@SP",
                "M=M+1"
            ]
        elif command in self.binary_op:
            lines = [
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                self.binary_op[command]
            ]
        else:
            lines = [
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                "D=M-D",
                "@TRUE" + str(self.label_number),
                self.jump_op[command],
                "@SP",
                "A=M-1",
                "M=0",
                "@DONE" + str(self.label_number),
                "0;JMP",
                "(TRUE" + str(self.label_number) + ")",
                "@SP",
                "A=M-1",
                "M=-1",
                "(DONE" + str(self.label_number) + ")"
            ]
        self.command_list.extend(lines)
        self.label_number += 1

    def write_push_pop(self, command, segment, index):
        lines = self.set_segment(command, segment, index)
        if command == "C_POP":
            lines.extend(self.popd)
        else:
            lines.extend(self.pushd)
        self.command_list.extend(lines)

    def close(self):
        for line in self.command_list:
            self.output_file.write("%s\n" % line)
        self.output_file.close()
