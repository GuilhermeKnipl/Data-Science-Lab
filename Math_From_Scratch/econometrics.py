import pandas as pd
import numpy as np
import os
import sys
from Math_From_Scratch import regression

def ar_linear_regression(y:pd.Series, n_window: int) -> tuple[float,float]:
    # Returns the AR (coef,intercept)
    y_lagged = y.shift(n_window)
    df = pd.DataFrame({'y': y})

    df['y_lag'] = y_lagged

    df = df.dropna()

    coef = regression.coefficient(df['y_lag'], df['y'])
    intercept = regression.intercept(df['y_lag'], df['y'], coef)

    return [coef,intercept]

def AR(X, y:pd.DataFrame, n_window:int):
    
    y = y.copy()

    y_pred = regression.multiple_regression(X,y, return_params=False) 
    
    y[f'ar_pred_lag{n_window}'] = np.nan
    y['pred'] = y_pred
    y['pred_error'] = y.iloc[:,0] - y['pred']

    ar_params= ar_linear_regression(y.iloc[:,0] , n_window)
    coef = ar_params[0]
    intercept = ar_params[1]


    for actual_idx in range(len(y)):
        sum_iter_lags = np.array([])

        if actual_idx >= n_window:
            for idx in range(1,n_window + 1):
                lag_iter_val = (y.iloc[actual_idx-idx,0] * coef) #+ y['pred_error'].loc[actual_idx]
                #print(lag_iter_val)
                sum_iter_lags = np.append(sum_iter_lags, lag_iter_val)

            #print("\n-------",intercept + sum_iter_lags.sum(), sum_iter_lags.sum())
            y.loc[actual_idx, f'ar_pred_lag{n_window}'] = intercept + sum_iter_lags.sum()


def MA(X, y:pd.DataFrame, n_window:int):
    
    y = y.copy()

    y_pred = regression.multiple_regression(X,y, return_params=False) 

    y['pred'] = y_pred
    y['pred_error'] = y.iloc[:,0] - y['pred']

    ar_params= ar_linear_regression(y.iloc[:,0] , n_window)
    coef = ar_params[0]
    intercept = ar_params[1]


    for actual_idx in range(len(y)):
        sum_iter_lags = np.array([])

        if actual_idx >= n_window:
            for idx in range(1,n_window + 1):
                lag_iter_val = y['pred_error'].loc[actual_idx - idx] * coef 
                sum_iter_lags = np.append(sum_iter_lags, lag_iter_val)

            y.loc[actual_idx, f'ma_pred_lag{n_window}'] = intercept + sum_iter_lags.sum()
    return y


def ARMA(X, y:pd.DataFrame, n_window:int):
    
    y = y.copy()

    y_pred = regression.multiple_regression(X,y, return_params=False) 
    
    y['pred'] = y_pred
    y['pred_error'] = y.iloc[:,0] - y['pred']

    ar_coefs, ar_intercept = ar_linear_regression(y.iloc[:,0], n_window)
    ma_coefs, _ = ar_linear_regression(y['pred_error'], n_window)


    for actual_idx in range(len(y)):
        sum_iter_lags = np.array([])
        sum_err_iter_lags  = np.array([])
        if actual_idx >= n_window:
            for idx in range(1,n_window + 1):
                lag_err_iter_val = y['pred_error'].loc[actual_idx - idx] * ar_coefs 
                lag_iter_val = y.iloc[actual_idx-idx,0] * ma_coefs

                sum_iter_lags = np.append(sum_iter_lags, lag_iter_val)
                sum_err_iter_lags = np.append(sum_err_iter_lags, lag_err_iter_val)


            y.loc[actual_idx, f'arma_pred_lag{n_window}'] = ar_intercept + sum_iter_lags.sum() + sum_err_iter_lags.sum()
    return y

def exp_moving_average(df: pd.DataFrame, column: str ,n_window:int) -> pd.DataFrame|ValueError:

    smoothing_factor = (2/(n_window + 1))

    if n_window == 0 or n_window > len(df):
        print("INVALID WINDOW RANGE")
        return ValueError
    else:

        metric_name = column
        col_name = f'ema_{metric_name}_{n_window}'
        
        df[col_name] = np.nan


        for n in range(len(df)):

            if n == 0:
                df.loc[n, col_name] = df.loc[n, column]

            else:
                last_ema = df.loc[n-1, col_name]
                actual_y = df.loc[n, column]

                df.loc[n, col_name] = actual_y * smoothing_factor + (1 - smoothing_factor) * last_ema



        return df

def SMA(df: pd.DataFrame, column: str ,n_window:int, method:str = 'mean') -> pd.DataFrame|None:
    # Simple Moving Average
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