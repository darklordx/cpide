_input_stream = open("in.txt")
_output_stream = open("out.txt","w",buffering=1)
def input():
    return _input_stream.readline()[:-1]
def print(s):
    _output_stream.write(s+"\n")
    

for i in range(10):
    n = input()
    print(n)
