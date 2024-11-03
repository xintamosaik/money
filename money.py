# grab a file named money.csv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read the file
df = pd.read_csv('money.csv')

# print the first 5 rows
print(df.head())

# print the last 5 rows
print(df.tail())