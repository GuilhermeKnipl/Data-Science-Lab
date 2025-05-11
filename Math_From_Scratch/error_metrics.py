import numpy as np
import pandas as pd

def MSE(y , y_pred) -> float:

    if len(y) == len(y_pred):
        err_summation = 0
        for idx in range(len(y)):
            err_summation += np.power(y[idx] - y_pred[idx],2)
        mse = (1 / len(y)) * err_summation
        return mse
        
    else: 
        print(f"Y has lenght {len(y)} x Y_Pred has lengh {len(y_pred)}")
        exit



def RMSE(y , y_pred) -> float:

    if len(y) == len(y_pred):
        err_summation = 0
        for idx in range(len(y)):
            err_summation += np.power(y[idx] - y_pred[idx],2)
        mse = (1 / len(y)) * err_summation
        return np.sqrt(mse)
        
    else: 
        print(f"Y has lenght {len(y)} x Y_Pred has lengh {len(y_pred)}")
        exit