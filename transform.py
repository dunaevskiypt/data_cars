import pandas as pd

import json


with open('car_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

df = pd.DataFrame(data)
