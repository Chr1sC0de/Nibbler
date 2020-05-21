from nibbler.math import find_max_from_gradients, find_min_from_gradients, find_max_from_gradients_jit, find_min_from_gradients_jit
import pathlib as pt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import time

if __name__ == "__main__":

    cwd = pt.Path(__file__).parent

    csv_files = cwd/"../../../resources/csv"
    
    assert csv_files.exists()

    csv_file =csv_files/"BitcoinBinance1hr.csv"

    data = pd.read_csv(csv_file)

    close = data["Close"].values

    gradients = np.gradient(close)

    N = 10000

    start = time()

    for i in range(N):
        max_locations = find_max_from_gradients(gradients)
    
    end = time()

    print(end-start)

    start = time()

    for i in range(N):
        min_locations = find_min_from_gradients(gradients)

    end = time()

    print(end-start)

    start = time()

    for i in range(N):
        max_locations = find_max_from_gradients_jit(gradients)
    
    end = time()

    print(end-start)

    start = time()

    for i in range(N):
        min_locations = find_min_from_gradients_jit(gradients)

    end = time()

    print(end-start)