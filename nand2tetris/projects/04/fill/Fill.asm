// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here
(GETKEY)
@8192           // set index or counter
D=A
@counter        // store the index in memory
M=D
@offset         // set memory address offset
M=0
@KBD            // get keyboard input
D=M
@NOTPRESS
D;JEQ
(PRESS)         // key pressed set 1's
@button
M=-1
@LOOP
0;JMP
(NOTPRESS)      // key not pressed set 0
@button
M=0
(LOOP)
@SCREEN         // load screen address in register
D=A
@offset         // load offset and add to screen address
A=D+M
D=A             // store address for use later
@address
M=D
@button         // get button press
D=M
@address
A=M
M=D
@offset         // load and increment offset
M=M+1
@counter        // load and decrement counter
M=M-1
D=M
@LOOP
D;JGT
@GETKEY
0;JMP





















