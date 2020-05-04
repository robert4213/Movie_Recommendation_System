import numpy as np
import pandas as pd
import sys
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
from pyspark import SparkConf,SparkContext

def train_ALS(rank,numItera):
    try:
        sc = SparkContext("local", "model training")
    except ERROR as e:
        sc.stop()
        sc = SparkContext("local", "model training")

    train  = sc.textFile('E:/CMPE255/train.csv')
    test  = sc.textFile('E:/CMPE255/test.csv')

    header = train.first()
    train = train.filter(lambda x: x != header)

    header = test.first()
    test = test.filter(lambda x: x != header)
    ratings = train.map(lambda l: l.split(',')).map(lambda l:Rating(int(l[0]),int(l[1]),float(l[2])))

    # rank_list = [2,4,6,8,10,15,20,30,40,50]
    # numItera_list = [5,10,20,30,40]

    valData = train.map(lambda l: l.split(',')).map(lambda l: (l[0],l[1]))
    testData = test.map(lambda l: l.split(',')).map(lambda l: (l[0],l[1]))

    # rmse_train = [[0]*len(numItera_list) for _ in range(len(rank_list))]
    # rmse_test = [[0]*len(numItera_list) for _ in range(len(rank_list))]
    try:
        model = ALS.train(ratings,rank,numItera)
        predictionVal = model.predictAll(valData).map(lambda l:((l[0],l[1]),l[2]))
        r_p = train.map(lambda l: l.split(',')).map(lambda l: ((int(l[0]),int(l[1])),float(l[2]))).join(predictionVal)
        MSE_train = r_p.map(lambda l:(l[1][0]-l[1][1])**2).mean()


        prediction = model.predictAll(testData).map(lambda l:((l[0],l[1]),l[2]))
        r_p = test.map(lambda l: l.split(',')).map(lambda l: ((int(l[0]),int(l[1])),float(l[2]))).join(prediction)
        MSE_test = r_p.map(lambda l:(l[1][0]-l[1][1])**2).mean()

        sc.stop()
    except ERROR as e:
        sc.stop()
        return ""

    return " ".join([rank,numItera,MSE_train,MSE_test])


if __name__ == "__main__":
    print("Start Training", sys.argv)
    f = open("E:/CMPE255/result.txt", "a")
    f.write(train_ALS(int(sys.argv[1]),int(sys.argv[2])))
    f.close()