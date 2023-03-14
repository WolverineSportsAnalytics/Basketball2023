import pandas as pd

# read in
combined = pd.read_csv("C:/Users/lavh/Documents/WSA/MMModel/Data/2023 KP.csv")
results = pd.read_csv("C:/Users/lavh/Documents/WSA/MMModel/Data/2023 MM Stats.csv")

# use merge
full_year = pd.merge(combined, results,
                     on="Team",
                     how='outer')

full_year.to_csv("C:/Users/lavh/Documents/WSA/MMModel/Data/2023_full.csv")