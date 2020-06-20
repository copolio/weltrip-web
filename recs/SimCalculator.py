"""
from recs.base_recommender import base_recommender

from django.db.models import Q
import time
from decimal import Decimal
"""

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

def SimCalculator ():
    # Create connection.
    cnx = sqlite3.connect('weltip-web\db.sqlite3')
    data = pd.read_sql_query("SELECT * FROM actualPlanner_rating", cnx)
    UserItemM = data.pivot_table('grade', index = 'userRated', columns = 'contentName').fillna(0)
    ItemUserM = UserItemM.transpose()
    place_sim = cosine_similarity(ItemUserM, ItemUserM)
    item_based_collabor = pd.DataFrame(data = place_sim, index = ItemUserM.index, columns = ItemUserM.index)

    item_based_collabor.to_sql('Recommender_similarity', cnx)

