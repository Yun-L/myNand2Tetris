@256
D=A
@SP
M=D
@None:return.0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@LCL
M=D
@5
D=D-A
@ARG
M=D
@Sys.init
0;JMP
(None:return.0)
(Sys.init)
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1
@R3
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1
@R4
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@Sys.init:return.1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@LCL
M=D
@5
D=D-A
@ARG
M=D
@Sys.main
0;JMP
(Sys.init:return.1)
@R6
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
(Sys.init:LOOP)
@Sys.init:LOOP
0;JMP
(Sys.main)
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
@R3
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1
@R4
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@LCL
A=M
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@LCL
A=M
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
@3
D=A
@LCL
A=M
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
@Sys.main:return.2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@LCL
M=D
@6
D=D-A
@ARG
M=D
@Sys.add12
0;JMP
(Sys.main:return.2)
@R5
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@0
D=A
@LCL
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@LCL
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@LCL
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@3
D=A
@LCL
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@4
D=A
@LCL
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1
@LCL
D=M
@FRAME
M=D
@5
A=D-A
D=M
@R14
M=D
@0
D=A
@ARG
A=M
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@ARG
D=M+1
@SP
M=D
@FRAME
M=M-1
A=M
D=M
@THAT
M=D
@FRAME
M=M-1
A=M
D=M
@THIS
M=D
@FRAME
M=M-1
A=M
D=M
@ARG
M=D
@FRAME
M=M-1
A=M
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Sys.add12)
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
@R3
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1
@R4
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@0
D=A
@ARG
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@12
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1
@LCL
D=M
@FRAME
M=D
@5
A=D-A
D=M
@R14
M=D
@0
D=A
@ARG
A=M
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@ARG
D=M+1
@SP
M=D
@FRAME
M=M-1
A=M
D=M
@THAT
M=D
@FRAME
M=M-1
A=M
D=M
@THIS
M=D
@FRAME
M=M-1
A=M
D=M
@ARG
M=D
@FRAME
M=M-1
A=M
D=M
@LCL
M=D
@R14
A=M
0;JMP
