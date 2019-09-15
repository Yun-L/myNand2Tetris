// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@1          // Set A to value 1
D=A         // D = 1
@i          // Set A to i address
M=D         // i = 1

(LOOP)

@i          // Set A to i address
D=M         // D = i
@R1         // Set A to R1 address
D=D-M       // D = D - R1
@END        // Set A to END address
D;JGT       // Jump to END if D is greater than 0
@R0         // Set A to R0 address
D=M         // D = R0
@product    // Set A to product address
M=D+M       // product = product + R0
@i          // Set A to i address
M=M+1       // i = i + 1
@LOOP       // Set A to LOOP address
0;JMP       // Jump to start of LOOP

(END)
@product    // Set A to product address
D=M         // D = product
@R2         // Set A to R2 address
M=D         // R2 = product

@0          // Set A to 0
D=A         // D = 0
@product    // set Memory[product] and Memory[i] back to 0
M=D
@i
M=D
