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


def coefficient (x_data: pd.Series, y_data: pd.Series): 
    sum_top = 0
    sum_botton = 0

    for (x,y) in zip(x_data,y_data):
        sum_top += (x - x_data.mean()) * (y - y_data.mean())
        sum_botton += np.power((x - x_data.mean()),2)
    
    coef = sum_top / sum_botton

    return coef        

def intercept (x_data: pd.Series, y_data: pd.Series, coefficient):
    intercept = y_data.mean() - (coefficient * x_data.mean())

def multiple_regression(x_data: pd.Series ,y_data: pd.Series):
    
    x_stack = np.column_stack([np.ones(len(x_data)), x_data])
    x_stack_t = x_stack.T

    ols = np.linalg.inv(x_stack_t.dot(x_stack)).dot(x_stack_t).dot(y_data)

    intercept = ols[0]
    coefficients = ols[1:]
        
    y_pred = intercept + x_data.dot(coefficients)




def moving_average(df: pd.DataFrame, column: str ,n_window:int, method:str) -> pd.DataFrame|None:

    methods = ['mean','sum','std','median']


    if n_window == 0 or n_window > len(df):
        print("INVALID WINDOW RANGE")
    elif method not in methods:
        print(f"Invalid operation {method} \nAvailable Methods:{methods}")
    else:
        metric_name = column
        col_name = f'{metric_name}_{n_window}_{method}'
        df[col_name] = np.nan

        for n in range(len(df)):

            if n >= n_window-1 and n != 0:
                window_values = np.array([],dtype=float)

                for idx in range(n_window):
                    iter_val = df[column][np.abs(n-idx)]
                    window_values = np.append(window_values, iter_val)
                match method:
                    case 'mean':
                        df.loc[n, col_name] = np.mean(window_values)
                    case 'sum':
                        df.loc[n, col_name] = np.sum(window_values)  
                    case 'std':
                        df.loc[n, col_name] = np.std(window_values)    
                    case 'median':
                        df.loc[n, col_name] = np.median(window_values)    

        return df
