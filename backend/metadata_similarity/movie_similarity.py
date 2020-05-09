import pandas as pd


class MovieSimilarity:
    def __init__(self):
        self.data = pd.read_csv('metadata_similarity/top_10_list.csv').reset_index(drop=True).set_index(['id'])

    def getmovies(self, id):
        try:
            return self.data.loc[id].tolist()
        except Exception as e:
            print('Error in get similar movie', e)
            return []


# if __name__ == '__main__':
#     m = MovieSimilarity()
#     m.getmovies(91548)
