import os
import pandas as pd
import psycopg2
import sqlite3
import logging
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import coo_matrix
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weltrip_web.settings")

import django

django.setup()

from recommender.models import Similarity
from actualPlanner.models import Rating
from weltrip_web import settings

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
logger = logging.getLogger('Item simialarity calculator')


class ItemSimilarityMatrixBuilder(object):

    def __init__(self, min_overlap=15, min_sim=0.2):
        self.min_overlap = min_overlap
        self.min_sim = min_sim
        self.db = settings.DATABASES['default']['ENGINE']


    def build(self, rating, save=True):

        logger.debug("Calculating similarities ... using {} ratings".format(len(rating)))
        start_time = datetime.now()
        ratings = pd.DataFrame(rating)
        ratings.columns = ratings.keys()
        logger.debug("Creating ratings matrix")
        ratings['grade'] = ratings['grade'].astype(float)
        ratings['avg'] = ratings.groupby('userRated')['grade'].transform(lambda x: normalize(x))

        ratings['avg'] = ratings['avg'].astype(float)
        ratings['userRated'] = ratings['userRated'].astype('category')
        ratings['contentName'] = ratings['contentName'].astype('category')

        coo = coo_matrix((ratings['avg'].astype(float),
                          (ratings['contentName'].cat.codes.copy(),
                           ratings['userRated'].cat.codes.copy())))

        logger.debug("Calculating overlaps between the items")
        overlap_matrix = coo.astype(bool).astype(int).dot(coo.transpose().astype(bool).astype(int))

        number_of_overlaps = (overlap_matrix > self.min_overlap).count_nonzero()
        logger.debug("Overlap matrix leaves {} out of {} with {}".format(number_of_overlaps,
                                                                         overlap_matrix.count_nonzero(),
                                                                         self.min_overlap))

        logger.debug("Rating matrix (size {}x{}) finished, in {} seconds".format(coo.shape[0],
                                                                                 coo.shape[1],
                                                                                 datetime.now() - start_time))

        sparsity_level = 1 - (ratings.shape[0] / (coo.shape[0] * coo.shape[1]))
        logger.debug("Sparsity level is {}".format(sparsity_level))

        start_time = datetime.now()
        cor = cosine_similarity(coo, dense_output=False)
        # cor = rp.corr(method='pearson', min_periods=self.min_overlap)
        # cor = (cosine(rp.T))

        cor = cor.multiply(cor > self.min_sim)
        cor = cor.multiply(overlap_matrix > self.min_overlap)

        places = dict(enumerate(ratings['contentName'].cat.categories))
        logger.debug('Correlation is finished, done in {} seconds'.format(datetime.now() - start_time))
        if save:

            start_time = datetime.now()
            logger.debug('save starting')
            if self.db == 'django.db.backends.postgresql':
                self._save_similarities(cor, places)
            else:
                self._save_with_django(cor, places)

            logger.debug('save finished, done in {} seconds'.format(datetime.now() - start_time))

        return cor, places

    def _save_similarities(self, sm, index, created=datetime.now()):
        start_time = datetime.now()

        logger.debug('truncating table in {} seconds'.format(datetime.now() - start_time))
        sims = []
        no_saved = 0
        start_time = datetime.now()
        coo = coo_matrix(sm)
        csr = coo.tocsr()

        logger.debug('instantiation of coo_matrix in {} seconds'.format(datetime.now() - start_time))

        query = "insert into similarity (created, source, target, similarity) values %s;"

        conn = self._get_conn()
        cur = conn.cursor()

        cur.execute('truncate table similarity')

        logger.debug('{} similarities to save'.format(coo.count_nonzero()))
        xs, ys = coo.nonzero()
        for x, y in tqdm(zip(xs, ys), leave=True):

            if x == y:
                continue

            sim = csr[x, y]

            if sim < self.min_sim:
                continue

            if len(sims) == 500000:
                psycopg2.extras.execute_values(cur, query, sims)
                sims = []
                logger.debug("{} saved in {}".format(no_saved,
                                                     datetime.now() - start_time))

            new_similarity = (str(created), index[x], index[y], sim)
            no_saved += 1
            sims.append(new_similarity)

        psycopg2.extras.execute_values(cur, query, sims, template=None, page_size=1000)
        conn.commit()
        logger.debug('{} Similarity items saved, done in {} seconds'.format(no_saved, datetime.now() - start_time))

    @staticmethod
    def _get_conn():
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
            dbUsername = settings.DATABASES['default']['USER']
            dbPassword = settings.DATABASES['default']['PASSWORD']
            dbName = settings.DATABASES['default']['NAME']
            conn_str = "dbname={} user={} password={}".format(dbName,
                                                              dbUsername,
                                                              dbPassword)
            conn = psycopg2.connect(conn_str)
        elif settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
            dbName = settings.DATABASES['default']['NAME']
            conn = sqlite3.connect(dbName)

        return conn

    def _save_with_django(self, sm, index, created=datetime.now()): ##  cor, places
        start_time = datetime.now()
        Similarity.objects.all().delete()
        logger.info(f'truncating table in {datetime.now() - start_time} seconds')
        sims = []
        no_saved = 0
        start_time = datetime.now()
        coo = coo_matrix(sm)
        csr = coo.tocsr()

        logger.debug(f'instantiation of coo_matrix in {datetime.now() - start_time} seconds')
        logger.debug(f'{coo.count_nonzero()} similarities to save')
        xs, ys = coo.nonzero()
        for x, y in zip(xs, ys):

            if x == y:
                continue

            sim = csr[x, y]

            if sim < self.min_sim:
                continue

            if len(sims) == 500000:

                Similarity.objects.bulk_create(sims)
                sims = []
                logger.debug(f"{no_saved} saved in {datetime.now() - start_time}")

            new_similarity = Similarity(
                source=index[x],
                target=index[y],
                created=created,
                similarity=sim
            )
            no_saved += 1
            sims.append(new_similarity)

        Similarity.objects.bulk_create(sims)
        logger.info('{} Similarity items saved, done in {} seconds'.format(no_saved, datetime.now() - start_time))

def main():
    logger.info("Calculation of item similarity")

    all_ratings = load_all_ratings()
    ItemSimilarityMatrixBuilder(min_overlap=20, min_sim=0.0).build(all_ratings)

def normalize(x):
    x = x.astype(float)
    x_sum = x.sum()
    x_num = x.astype(bool).sum()
    x_mean = x_sum / x_num

    if x_num == 1 or x.std() == 0:
        return 0.0
    return (x - x_mean) / (x.max() - x.min())


def load_all_ratings(min_ratings=1):
    columns = ['userRated', 'contentName', 'grade'] #, 'type']

    ratings_data = Rating.objects.all().values(*columns)

    ratings = pd.DataFrame.from_records(ratings_data, columns=columns)
    user_count = ratings[['userRated', 'contentName']].groupby('userRated').count()
    user_count = user_count.reset_index()
    userRateds = user_count[user_count['contentName'] > min_ratings]['userRated']
    ratings = ratings[ratings['userRated'].isin(userRateds)]
    ratings['grade'] = ratings['grade'].astype(float)
    return ratings

if __name__ == '__main__':
    main()
