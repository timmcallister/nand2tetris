@SP     // gt
AM=M-1
D=M
A=A-1
D=M-D
@TRUE
D;JGT
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
