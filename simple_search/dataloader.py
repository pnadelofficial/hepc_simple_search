import pandas as pd
from whoosh.index import open_dir

class DataLoader:
    def __init__(self) -> None:
        self.choice_path = "./indices/press_review_index/indices/press_review_index" # './indices/press_review_index'
        self.data_path = "./data/chunked_press_review.csv"
    
    def load(self):
        data = pd.read_csv(self.data_path)
        return data, open_dir(self.choice_path)

