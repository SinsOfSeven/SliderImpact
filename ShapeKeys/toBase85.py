
import os
import base64

folder = os.getcwd().split("\\")[-1].replace(" ","_") + "_"

with open("output.txt","w+",encoding="utf-8") as writer:
    for filename in os.listdir():
        if filename.endswith(".dds"):
            with open(filename) as reader:
                x = base64.b85encode(reader.buffer.read())
                writer.write(f'{filename.split('.')[0]} = {str(x)}\n')

#base64.b64encode()