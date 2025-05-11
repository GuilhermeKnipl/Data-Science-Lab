import numpy as np
import pandas as pd


def relu(y: pd.Series) -> pd.Series:
    return y.clip(lower=0)