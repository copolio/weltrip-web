import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from ast import literal_eval
# from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv('C:/projects/weltrip_web/recs/areaBasedList.csv')
data['category'] = data['cat1']+" "+data['cat2']+" "+data['cat3']
data.category = data.category.fillna(" ")
data.category.isnull().sum()
count_vector = CountVectorizer(ngram_range=(1, 3))
c_vector_category = count_vector.fit_transform(data['category'])
cat_c_sim = cosine_similarity(c_vector_category, c_vector_category).argsort()[:, ::-1]


def get_recommend_place_list_content(df, contentid, top=30):
    # 특정 장소와 비슷한 장소를 추천해야 하기 때문에 '특정 장소' 정보를 뽑아낸다.
    target_place_index = df[df['contentid'] == contentid].index.values

    # 코사인 유사도 중 비슷한 코사인 유사도를 가진 정보를 뽑아낸다.
    sim_index = cat_c_sim[target_place_index, :top].reshape(-1)
    # 본인을 제외
    sim_index = sim_index[sim_index != target_place_index]

    # data frame으로 만들고 readcount순으로 정렬한 뒤 return
    result = df.iloc[sim_index].sort_values('readcount', ascending=False)[:10]
    return result