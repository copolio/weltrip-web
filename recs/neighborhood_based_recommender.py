#from recs.base_recommender import base_recommender

from django.db.models import Q
import time
from decimal import Decimal

from recommender.models import Similarity
from actualPlanner.models import Rating
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recs.item_similarity_calculator  import ItemSimilarityMatrixBuilder

class NeighborhoodBasedRecs():

    def __init__(self, neighborhood_size=15, min_sim=0.0):
        self.neighborhood_size = neighborhood_size
        self.min_sim = min_sim
        self.max_candidates = 100

    def recommend_items(self, user_id, num=6):

        active_user_items = Rating.objects.filter(userRated=user_id).order_by('-grade')[:100]
        # 사용자가 높은 점수를 준 items

        return self.recommend_items_by_ratings(user_id, active_user_items.values())

    def recommend_items_by_ratings(self, user_id, active_user_items, num=6):

        if len(active_user_items) == 0:
            return {}
        active_user_items = active_user_items.values()
        start = time.time()
        content_names = {content['contentName']: content['grade'] for content in active_user_items}
        total = 0
        for i in content_names.values():
            total +=i
        user_mean = i / len(content_names)

        ItemSimilarityMatrixBuilder(0, min_sim=0).build(active_user_items, save=True)

        candidate_items = Similarity.objects.filter(Q(source__in=content_names.keys())
                                                    & ~Q(target__in=content_names.keys())
                                                    & Q(similarity__gt=self.min_sim)
                                                    )
        candidate_items = candidate_items.order_by('-similarity')[:self.max_candidates]

        
        recs = dict()
        rated_items = []
        for candidate in candidate_items:
            target = candidate.target

            pre = 0
            sim_sum = 0

            
            for i in candidate_items :
                if i.target == target:
                    rated_items.append(i)

            if len(rated_items) > 1:
                for sim_item in rated_items:
                    r = Decimal(content_names[sim_item.source] - user_mean)
                    pre += sim_item.similarity * r
                    sim_sum += sim_item.similarity
                if sim_sum > 0:
                    recs[target] = {'prediction': Decimal(user_mean) + pre / sim_sum,
                                    'sim_items': [r.source for r in rated_items]}

        sorted_items = sorted(recs.items(), key=lambda item: -float(item[1]['prediction']))[:num]
        return sorted_items

    def predict_score(self, user_id, item_id):

        user_items = Rating.objects.filter(user_id=user_id)
        user_items = user_items.exclude(cotentName=item_id).order_by('-rating')[:100]
        content_names = {place.contentName: place.rating for place in user_items}

        return self.predict_score_by_ratings(item_id, content_names)

    def predict_score_by_ratings(self, item_id, content_names):
        top = Decimal(0.0)
        bottom = Decimal(0.0)
        ids = content_names.keys()
        mc = self.max_candidates
        candidate_items = (Similarity.objects.filter(source__in= ids)
                                             .exclude(source=item_id)
                                             .filter(target=item_id))
        candidate_items = candidate_items.distinct().order_by('-similarity')[:mc]

        if len(candidate_items) == 0:
            return 0

        for sim_item in candidate_items:
            r = content_names[sim_item.source]
            top += sim_item.similarity * r
            bottom += sim_item.similarity

        return Decimal(top/bottom)
