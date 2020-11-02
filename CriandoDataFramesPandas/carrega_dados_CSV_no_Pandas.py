# The convention is to import Pandas with shortcut 'pd'
import pandas as pd
import  os

app_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(app_path, 'FAO+database.csv')

# Read the CSV into a pandas data frame (df) With a df you can do many things most important: visualize data with Seaborn
df = pd.read_csv(file_path, delimiter=',', encoding='latin-1')

print(df)

# Option 2:
# If the file is in the same directory that you are working in - you can load it with just the filename.
# Use os.getcwd() to 'get current working directory'
print("The directory we are working in is {}".format(os.getcwd()))
df = pd.read_csv("FAO+database.csv", delimiter=',', encoding='latin-1')

print(df)
