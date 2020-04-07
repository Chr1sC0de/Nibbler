import numpy as np

def splitList(inputList,nSplits):
    divisionSize = len(inputList)//nSplits
    chunks = []; chunkSetter = chunks.append
    for i in np.arange(nSplits):
        k = i*divisionSize

        if i < nSplits :
            chunkSetter(inputList[k:(k+divisionSize)])
        else:
            chunkSetter(inputList[k:])
    return chunks