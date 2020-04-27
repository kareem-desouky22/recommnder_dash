

import numpy as np
import pandas as pd
import os
from surprise import Dataset, KNNWithMeans, Reader


anime_info_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'anime_info.dat')
anime_ratings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'anime_ratings.dat')

anime_info = pd.read_csv(anime_info_path, sep="\t")
# print(anime_info.head())
anime_ratings = pd.read_csv(anime_ratings_path, sep='\t')

reader = Reader(rating_scale=(1, 10))

data = Dataset.load_from_df(anime_ratings[['User_ID', "Anime_ID", "Feedback"]], reader)

# To use item-based cosine similarity
sim_options = {
    "name": "cosine",
    "user_based": False,  # Compute  similarities between items
}

model = KNNWithMeans(sim_options=sim_options)

trainingSet = data.build_full_trainset()

model.fit(trainingSet)

# print ("ok")

def top_5():

    top_movies = anime_info.sort_values(
        by='rating', ascending=False)

    return top_movies[:5]

def top_5_recommendations(uid):
    
    movies_rated_by_user = anime_ratings.loc[anime_ratings['User_ID']==uid, "Anime_ID"].values
    
    other_movies = anime_info.loc[~anime_info['anime_ids'].isin(movies_rated_by_user)].sort_values(
        by='rating', ascending=False)
        

    other_movies['user_rate'] = other_movies['anime_ids'].apply(lambda x: model.predict(uid, x).est)
    
    return print(str(other_movies.sort_values(by='user_rate', ascending=False)[:5]))




