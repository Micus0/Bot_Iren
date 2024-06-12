import pandas as pd


class DataManager:
    def __init__(self, data: list):
        self.df = pd.DataFrame(data)

    def create_csv(self):
        self.df.to_csv("lavoro.csv", header=False, index=False)
