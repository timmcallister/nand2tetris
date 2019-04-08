class Write_Helper:
    def __init__(self):

        self.pushd = [
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]

        self.spmm = [
            "@SP",
            "M=M-1"
        ]

        self.popd = [
            "@SP",
            "M=M-1",
            "@SP",
            "A=M",
            "M=D"
        ]

        self.binary_op = {
            "add": "M=D+M",
            "sub": "M=D-M",
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

        
