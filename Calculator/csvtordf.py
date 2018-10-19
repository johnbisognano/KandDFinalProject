import numpy as npy
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
from pandas import Series,DataFrame

def main():
    df = pd.read_csv('19-10-2018_prix_europe.csv', delimiter=',',skipinitialspace=True)

    print(df)

if __name__ == '__main__':
    main()