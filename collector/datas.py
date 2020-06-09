from actualPlanner.models import Rating
import pandas as pd
import numpy as np



# 원하는 target row 값을 인자로 주면
# target행, 장소 열, 평가값 내용을 가지는 데이터프레임 반환
def basicTable():
    # 장소 열 값 생성
    all_data = Rating.objects.all().values()
    column_sites = []
    for items in all_data:
        tmp = str(items.get('contentId'))
        if tmp in column_sites:
            continue
        else: column_sites.append(tmp)


    # target row 생성
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

    print(result)
    
    return result


