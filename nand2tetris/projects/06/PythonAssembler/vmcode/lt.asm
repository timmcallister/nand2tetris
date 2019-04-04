@SP     // lt
AM=M-1
D=M     // d is second operand
A=A-1
D=M-D  // m is first operand
@TRUE
D;JLT
@SP
A=M-1
M=0
@DONE
0;JMP
(TRUE)
@SP
A=M-1
M=-1
(DONE)
