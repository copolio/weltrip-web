from actualPlanner.models import Rating
from search.models import ClickDetail
import pandas as pd
import numpy as np




def basicTable():
    # 장소 열 값 생성
    all_data = Rating.objects.all().values()
    column_sites = []
    for items in all_data:
        tmp = str(items.get('contentId'))
        if tmp in column_sites:
            continue
        else: column_sites.append(tmp)


    # 유저이름 행 값 생성
    try:
        tmp_row_items = []
        for items in all_data:
            tmps = str(items.get('userRated'))
            if tmps in tmp_row_items:
                continue
            else: tmp_row_items.append(tmps)
        
        rows_and_values = {}
        for elm in tmp_row_items:
            d1 = {}
            filter_tmp = Rating.objects.filter(userRated=elm)
            
            for obj in filter_tmp:
                key = obj.contentId
                value = obj.grade
                d1[key] = value
            rows_and_values[elm] = d1
    except:
        pass
        # rows_and_values = {}

    
    # 데이터프레임 생성
    result = pd.DataFrame(columns = column_sites)

    for user, data in rows_and_values.items():
        df_tmp = pd.DataFrame.from_dict([data])
        df_tmp_rename = df_tmp.rename(index={0: user})
        # result = pd.merge(result, df_tmp_rename, how='outer')
        result = result.append(df_tmp_rename)

    # 평균값 행 추가
    df_avr = result.mean()
    df_avr_ = pd.DataFrame(df_avr).T
    df_avr_ = df_avr_.rename(index={0: '_average_'})
    

    # 평가자 수 행 추가
    df_count = result.count()
    df_count_ = pd.DataFrame(df_count).T
    df_count_ = df_count_.rename(index={0: '_count_'})
    result = result.append(df_count_)
    result = result.append(df_avr_)
    
    return result



def userHisTable(username):

    try:
        dataset = ClickDetail.objects.filter(userId=username)

        result = pd.DataFrame(columns = ['contentId', 'cat1', 'cat2', 'cat3', 'date'])
        
        for elm in dataset:
            cId = elm.contentId
            cat1 = elm.cat1
            cat2 = elm.cat2
            cat3 = elm.cat3
            date = elm.date
            s = pd.Series([cId, cat1, cat2, cat3, date], index = ['contentId', 'cat1', 'cat2', 'cat3', 'date'])
        
            result = result.append(s, ignore_index=True)
        
        return result


    except:
        # db 조회 실패시 리턴
        result = pd.DataFrame({'000000':np.nan,})
        return result
