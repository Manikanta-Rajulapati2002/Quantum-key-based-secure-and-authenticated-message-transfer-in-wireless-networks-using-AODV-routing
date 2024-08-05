import numpy as np
def dec2bin(decimal_num,bits):
    decimal_num = int(decimal_num)
    binary_str = bin(decimal_num)[2:]
    return binary_str.zfill(bits)

def QHFM296(message):
    msgcodes = [ord(c) for c in message]
    binMsg = ''
    msgCharCnt = len(msgcodes)
    for j in range(msgCharCnt):
        binMsg+= bin(msgcodes[j])[2:]
    binMsgLen = len(binMsg)
    nodesCnt = 37
    hashBitsCntPerNode = 8
    probDigitsCntInUse = 8
    hash_code = ''
    amplArr = np.zeros((8, 37))
    coin1 = [9,18,27,36,45,54,63,72,81]
    coin2 = [81,72,63,54,45,36,27,18,9]
    for i in range(9):
        theta0 = coin1[i]
        theta1 = coin2[i]
        a0, b0, c0, d0 = np.cos(np.radians(theta0)), np.sin(np.radians(theta0)), np.sin(np.radians(theta0)), -np.cos(np.radians(theta0))
        a1, b1, c1, d1 = np.cos(np.radians(theta1)), np.sin(np.radians(theta1)), np.sin(np.radians(theta1)), -np.cos(np.radians(theta1))
        iniPos = 1
        amplArr[2, iniPos] = 1/np.sqrt(2)
        amplArr[3, iniPos] = 1/np.sqrt(2)
        for t in range(0,binMsgLen):
            tempAmpl = np.zeros((8, nodesCnt))
            if binMsg[t]=='1':
                for k in range(0,nodesCnt):
                    tempAmpl[0, (k-1)%nodesCnt]=a1*amplArr[2, k]+b1*amplArr[3, k]
                    tempAmpl[1, (k-1)%nodesCnt]=c1*amplArr[0, k]+d1*amplArr[1, k]
                    tempAmpl[2, (k-1)%nodesCnt]=a1*amplArr[6, k]+b1*amplArr[7, k]
                    tempAmpl[3, (k-1)%nodesCnt]=c1*amplArr[4, k]+d1*amplArr[5, k]
                    tempAmpl[4, (k+1)%nodesCnt]=a1*amplArr[0, k]+b1*amplArr[1, k]
                    tempAmpl[5, (k+1)%nodesCnt]=c1*amplArr[2, k]+d1*amplArr[3, k]          
                    tempAmpl[6, (k+1)%nodesCnt]=a1*amplArr[4, k]+b1*amplArr[5, k]
                    tempAmpl[7, (k+1)%nodesCnt]=c1*amplArr[6, k]+d1*amplArr[7, k]
            else:
                for k in range(0,nodesCnt):
                    tempAmpl[0, (k-1) % nodesCnt] = a0*amplArr[4, k] + b0*amplArr[5, k]
                    tempAmpl[1, (k-1) % nodesCnt] = c0*amplArr[0, k] + d0*amplArr[1, k]
                    tempAmpl[2, (k-1) % nodesCnt] = a0*amplArr[6, k] + b0*amplArr[7, k]
                    tempAmpl[3, (k-1) % nodesCnt] = c0*amplArr[2, k] + d0*amplArr[3, k]
                    tempAmpl[4, (k+1) % nodesCnt] = a0*amplArr[0, k] + b0*amplArr[1, k]
                    tempAmpl[5, (k+1) % nodesCnt] = c0*amplArr[4, k] + d0*amplArr[5, k]
                    tempAmpl[6, (k+1) % nodesCnt] = a0*amplArr[2, k] + b0*amplArr[3, k]
                    tempAmpl[7, (k+1) % nodesCnt] = c0*amplArr[6, k] + d0*amplArr[7, k]
            amplArr = tempAmpl
        distriArr = np.zeros(nodesCnt)
        for k in range(0,nodesCnt):
            distriArr[k] = np.dot(amplArr[:, k], amplArr[:, k])
        nodeHashArr = np.zeros(nodesCnt) 
        nodeHashMax = 2 ** hashBitsCntPerNode
        for k in range(0,nodesCnt):
            nodeHashArr[k] = round(distriArr[k] * 10**probDigitsCntInUse) % nodeHashMax
        hashbits = ''
        for l in nodeHashArr:
            hashbits+=dec2bin(l,8)
        hash_code = hex(int(hashbits, 2))
        binMsg = ''
        msgcodes = [ord(c) for c in hash_code]
        msgCharCnt = len(msgcodes)
        for j in range(msgCharCnt):
            binMsg+= bin(msgcodes[j])[2:]
    return hash_code[2:].upper()


