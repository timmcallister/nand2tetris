class CodeWriter:

    def __init__(self, output_file_name):
        self.command_list = []
        self.file = output_file_name.split("/")[-1]
        self.output_file = open(output_file_name, 'w')
        self.rel_label_num = 0
        self.label_prefix = ''

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

    def push_str(self, push_string):
        lines = [
            "@" + push_string,
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
        self.command_list.extend(lines)

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
                "@TRUE" + str(self.rel_label_num),
                self.jump_op[command],
                "@SP",
                "A=M-1",
                "M=0",
                "@DONE" + str(self.rel_label_num),
                "0;JMP",
                "(TRUE" + str(self.rel_label_num) + ")",
                "@SP",
                "A=M-1",
                "M=-1",
                "(DONE" + str(self.rel_label_num) + ")"
            ]
        self.command_list.extend(lines)
        self.rel_label_num += 1

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

    def set_file_name(self, file_name):
        self.file_name = file_name.split("/")[-1]

    def write_init(self):
        lines = [
            "@256",
            "D=A",
            "@0",
            "M=D"
        ]
        self.command_list.extend(lines)
        self.write_call("Sys.init", 0)

    def write_label(self, label):
        self.command_list.append("(" + self.label_prefix + "$" + label + ")")

    def write_goto(self, label):
        lines = [
            "@" + self.label_prefix + "$" + label,
            "0;JMP"
        ]
        self.command_list.extend(lines)

    def write_if(self, label):
         lines = [
             "@SP",
             "AM=M-1",
             "D=M",
             "@" + self.label_prefix + "$" + label,
             "D;JNE"
         ]
         self.command_list.extend(lines)

    def write_function(self, function_name, n_vars):
        self.command_list.append("(" + function_name + ")")
        self.label_prefix = function_name
        for _ in range(n_vars):
            self.write_push_pop("C_PUSH", "constant", '0')

    def write_call(self, function_name, n_args):
        return_addr = "$return" + str(self.rel_label_num)
        self.command_list.extend([
            "@" + return_addr,
            "D=A"
        ])
        self.command_list.extend(self.pushd)
        self.push_str("LCL")
        self.push_str("ARG")
        self.push_str("THIS")
        self.push_str("THAT")
        lines = [
            "@SP",
            "D=M",
            "@" + str(n_args),
            "D=D-A",
            "@5",
            "D=D-A",
            "@ARG",
            "M=D",
            "@SP",
            "D=M",
            "@LCL",
            "M=D",
            "@" + function_name,
            "0;JMP"
        ]
        self.command_list.extend(lines)
        self.command_list.append("($return" + str(self.rel_label_num) + ")")
        self.rel_label_num += 1
    
    def write_return(self):
        FRAME = "R13"
        RET = "R14"

        lines =[
            "@LCL",
            "D=M",
            "@" + FRAME,
            "M=D",
            "@5",                       
            "A=D-A",
            "D=M",
            "@" + RET,
            "M=D",
            "@SP",
            "AM=M-1",
            "D=M",
            "@ARG",
            "A=M",
            "M=D",
            "@ARG",
            "D=M+1",
            "@SP",
            "M=D",
            "@" + FRAME,
            "AM=M-1",
            "D=M",
            "@THAT",
            "M=D",
            "@" + FRAME,
            "AM=M-1",
            "D=M",
            "@THIS",
            "M=D",
            "@" + FRAME,
            "AM=M-1",
            "D=M",
            "@ARG",
            "M=D",
            "@" + FRAME,
            "AM=M-1",
            "D=M",
            "@LCL",
            "M=D",
            "@" + RET,
            "A=M",
            "0;JMP"
        ]

        self.command_list.extend(lines)
