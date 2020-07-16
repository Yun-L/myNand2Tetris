# test seek, read and tell methods

with open("./seektellread.txt", "r") as infile:
    infile.read(8)
    res = infile.readline()
    print(res)
    pos = infile.tell()
    infile.seek(pos)
    res = infile.read(1)
    print(f"[{res}]")
    # tell() returns where the next char is
    # readline includes the newline
    # readline only reads remainder of line

with open("./seektellread.txt", "r") as infile:
    infile.read(8)
    pos = infile.tell()
    infile.seek(pos)
    c = infile.read(1)
    print(c)
    # prints o

with open("./seektellread.txt", "r") as infile:
    infile.readline()
    res = infile.read(17)
    print(res)
    res = infile.read(1)
    if not res:
        print("returns false")
    print(f"[{res}]")
