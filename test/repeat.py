# Here is some code that redirects io.
_input_stream = open("in.txt")
_output_stream = open("out.txt", "w", buffering=1)

def input():
    return _input_stream.readline()[:-1]

def print(s):
    _output_stream.write(s+"\n")
# User Code Below