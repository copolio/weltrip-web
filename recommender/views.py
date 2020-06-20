import operator
from decimal import Decimal
from math import sqrt

import numpy as np
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
import recs.content_based_recommender

from actualPlanner.models import Rating
from recs.neighborhood_based_recommender import NeighborhoodBasedRecs


def pearson(users, this_user, that_user):
    if this_user in users and that_user in users:
        this_user_avg = sum(users[this_user].values()) / len(users[this_user].values())
        that_user_avg = sum(users[that_user].values()) / len(users[that_user].values())

        all_places = set(users[this_user].keys()) & set(users[that_user].keys())

        dividend = 0
        a_divisor = 0
        b_divisor = 0
        for place in all_places:

            if place in users[this_user].keys() and place in users[that_user].keys():
                a_nr = users[this_user][place] - this_user_avg
                b_nr = users[that_user][place] - that_user_avg
                dividend += a_nr * b_nr
                a_divisor += pow(a_nr, 2)
                b_divisor += pow(b_nr, 2)

        divisor = Decimal(sqrt(a_divisor) * sqrt(b_divisor))
        if divisor != 0:
            return Decimal(dividend) / Decimal(sqrt(a_divisor) * sqrt(b_divisor))

    return 0


def jaccard(users, this_user, that_user):
    if this_user in users and that_user in users:
        intersect = set(users[this_user].keys()) & set(users[that_user].keys())

        union = set(users[this_user].keys()) | set(users[that_user].keys())

        return len(intersect) / Decimal(len(union))
    else:
        return 0


def similar_users(request, user_id, sim_method = 'pearson'):
    min = request.GET.get('min', 1)

    ratings = Rating.objects.filter(userRated = user_id)
    sim_users = Rating.objects.filter(contentName__in=ratings.values('contentName')) \
        .values('userRated') \
        .annotate(intersect=Count('userRated')).filter(intersect__gt=min)

    dataset = Rating.objects.filter(userRated__in=sim_users.values('userRated'))

    users = {u['userRated']: {} for u in sim_users}

    for row in dataset:
        if row.userRated in users.keys():
            users[row.userRated][row.contentName] = row.grade

    similarity = dict()

    switcher = {
        'jaccard': jaccard,
        'pearson': pearson,
    }

    for user in sim_users:

        func = switcher.get(sim_method, lambda: "nothing")
        s = func(users, user_id, user['userRated'])

        if s > 0.2:
            similarity[user['userRated']] = round(s, 2)
    topn = sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)[:10]

    data = {
        'user_id': user_id,
        'num_places_rated': len(ratings),
        'type': sim_method,
        'topn': topn,
        'similarity': topn,
    }

    #return data 
    return JsonResponse(data, safe=False)
    #http://127.0.0.1:8000/recommender/sim/user/'user_id'/pearson/

def recs_cf(request, user_id, num=6):
    min_sim = request.GET.get('min_sim', 0.1)
    sorted_items = NeighborhoodBasedRecs(min_sim=min_sim).recommend_items('user_id', num)

    print(f"cf sorted_items is: {sorted_items}")
    data = {
        'user_id': user_id,
        'data': sorted_items
    }

    return JsonResponse(data, safe=False)
