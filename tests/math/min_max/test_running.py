from nibbler.math import find_max_from_gradients, find_min_from_gradients 
import pathlib as pt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

    cwd = pt.Path(__file__).parent

    csv_files = cwd/"../../../resources/csv"
    
    assert csv_files.exists()

    csv_file =csv_files/"BitcoinBinance1hr.csv"

    data = pd.read_csv(csv_file)

    close = data["Close"].values

    gradients = np.gradient(close)

    max_locations = find_max_from_gradients(gradients)
    min_locations = find_min_from_gradients(gradients)

    plt.plot(close)

    plt.plot(max_locations, close[max_locations], "o")

    plt.plot(min_locations, close[min_locations], "o")

    plt.show()