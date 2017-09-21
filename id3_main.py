#import numpy as np
#import pandas as pd
import sys

if __name__== "__main__":
    cmdLine = sys.argv
    print(len(sys.argv))

    trainData = read_file(cmdLine[0])
    testData = read_file(cmdLine[1])
