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

// Put your code here.


(PRELOOP)

@R1         // Use R1 as the address offset for the screen and set to 0
M=0

(LOOP)

@R1         // Check if offset is larger than screen range
D=M         
@8192       
D=A-D
@PRELOOP
D;JLE       // Jump to PRELOOP if offset is larger than 8192

@SCREEN     // Start Address of the screen
D=A
@R1
D=D+M
@pix_addr   // keep pixel address
M=D         

@KBD        // Check keyboard input
D=M         
@BLACK
D;JNE       // Jump to BLACK if any key in pressed

(WHITE)

@pix_addr  // Make screen white at pix_addr
A=M
M=0
@INC
0;JMP

(BLACK)     // Make screen black at pix_addr

@pix_addr
A=M
M=-1
@INC
0;JMP

(INC)

@1         // Increment offset by 16
D=A
@R1
M=D+M
@LOOP
0;JMP