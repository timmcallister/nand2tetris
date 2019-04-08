@2		// index
D=A
@10		// segment
D=D+A		// segment is init
@SP
AM=M-1
A=M
A=A+D		// swap a and d
D=A-D
A=A-D
M=D


