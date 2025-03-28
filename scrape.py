import pandas as pd 
import random 
from datetime import datetime


items = ["A", "B", "C"]
prices = [random.randint(1, 10) for item in items]
df = pd.DataFrame({"Items": items, "Prices": prices})
# path = f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.csv'
path = "prices.csv"
df.to_csv(path, index=False)