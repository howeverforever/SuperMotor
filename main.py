import sys, serial
from collections import deque

from lib import *

POOL_SIZE = 10

# class that holds analog data for N samples
class AnalogData:
    # constr
    def __init__(self, maxLen):
        self.ax = deque([0.0]*maxLen)
        self.ay = deque([0.0]*maxLen)
        self.az = deque([0.0]*maxLen)
        self.maxLen = maxLen

    # ring buffer
    def addToBuf(self, buf, val):
        if len(buf) < self.maxLen:
            buf.append(val)
        else:
            buf.pop()
            buf.appendleft(val)

    # add data
    def add(self, data):
        assert(len(data) == 3)
        self.addToBuf(self.ax, data[0])
        self.addToBuf(self.ay, data[1])
        self.addToBuf(self.az, data[2])
    def mergeToList(self):
        tmps=[[], [], []]
        tmps[0]=list(self.ax)
        tmps[1]=list(self.ay)
        tmps[2]=list(self.az)
        return tmps

TRAINING_MODEL_FILE = 'motorcycle.txt'
TARGET_FILE = 'prediction.txt'

def ReadModel():
    fp = open(TRAINING_MODEL_FILE, 'r')
    X = []
    for toekn in fp.readline().split('^'):
        X.append(toekn.split(','))
    
    y = fp.readline().split(',')
    
    clf = SVC(kernel = 'linear', gamma = 4)
    clf.fit(X, y)
    
    return clf

def AddToPool(pool, val):
    if len(pool) == POOL_SIZE:
        pool.pop()
    pool.appendleft(val)
    
def TakeResult(pool):
    counts = np.bincount(pool)
    return np.argmax(counts)
    
# main() function
def main():
    # open feature data AND parse them
    SVM = ReadModel()
              
    # plot parameters
    analogData = AnalogData(PAGESIZE)
    dataList = []
    print('start to receive data...')
    
    # open serial port
    ser = serial.Serial("COM4", 9600)
    for _ in range(20):
        ser.readline()
        
    pool = deque([-1] * POOL_SIZE)
    
    while True:
        try:
            line = ser.readline()
            try:
                data = [float(val) for val in line.decode().split(',')]
                if(len(data) == 3):
                    analogData.add(data)
                    dataList = analogData.mergeToList()
                    
                    a = []
                    for k in range(len(dataList[0])):
                        a.append([dataList[0][k], dataList[1][k], dataList[2][k]])
                    realData = Parse(a)
                    
                    
                    prediction = Predict(realData, SVM)
                    AddToPool(pool, prediction)
                    
                    fp = open(TARGET_FILE, 'w')
                    fp.write(str(TakePool(pool)))
                    fp.close()
                   
            except:
                pass
        except KeyboardInterrupt:
            print('exiting')
            break
    # close serial
    ser.flush()
    ser.close()
    
    # reset file
    fp = open(TARGET_FILE, 'w')
    fp.write('-1')
    fp.close()    

# call main
if __name__ == '__main__':
    main()