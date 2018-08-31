// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here
@R2         // clear R2
M=0

@R0         // if either term is 0, skip to end
D=M
@END
D;JEQ
@R1
D=M
@END
D;JEQ


(LOOP)
@R0
D=M
@R2
M=M+D
@R1
M=M-1
D=M
@END
D;JEQ
@LOOP
0;JMP

(END)
0;JMP


//@R0
//D=M
//@sum
//M=D
//@R2
//M=0
//(LOOP)
//@R1
//D=M-1
//M=D
//@DONE
//D;JEQ
//@R0
//AD=M
//D=D+A
//@sum
//M=D
//@LOOP
//0;JMP
//(DONE)
//@sum
//D=M
//@R2
//M=D
//(END)
//@END
//0;JMP



