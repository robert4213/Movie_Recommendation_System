import pandas as pd
import numpy as np


if __name__ == '__main__':
    df = pd.read_csv('E:/CMPE255/rating_processed.csv')
    print(df.head())
    df = df.sample(frac=1).reset_index(drop=True)
    print(df.head())
    sp = df.count()[0]//10
    print(sp)
    dfs = np.split(df,[sp],axis = 0)
    # test = df.iloc[:,:sp]
    # train = df.iloc[:,sp:]
    print(df.count(),dfs[0].count(),dfs[1].count())
    dfs[0].to_csv('E:/CMPE255/test.csv',index=False)
    dfs[1].to_csv('E:/CMPE255/train.csv',index=False)
