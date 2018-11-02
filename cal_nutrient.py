import os
import re
import pandas as pd

filename = 'data/foodnutrienttable.csv'
filepath = os.path.join(os.path.dirname(__file__), filename)
fooddata = pd.read_csv(filepath, engine='python')



