import os, sys
from colorutils.convert import hex_to_hsv, hsv_to_hex
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pandas as pd
import joblib

from  classes.DbConn import DbConn

if __name__ == '__main__':

    db = DbConn()
    
    # ##################
    # sql = "select * from color_pallete_taeuk"
    # hex_list = db.selectdict(sql)
    # # print(hex_list)
    # # print(hex_to_hsv(hex_list[0]['hex1']))
    # for row in hex_list:
    #     idx = row['idx']
    #     h1, s1, v1 = hex_to_hsv(row['hex1'])
    #     h2, s2, v2 = hex_to_hsv(row['hex2'])
    #     h3, s3, v3 = hex_to_hsv(row['hex3'])
    #     h4, s4, v4 = hex_to_hsv(row['hex4'])
        
    #     h1, h2, h3, h4 = round(h1), round(h2), round(h3), round(h4)
        
    #     s1, v1 = round(s1*100), round(v1*100)
    #     s2, v2 = round(s2*100), round(v2*100)
    #     s3, v3 = round(s3*100), round(v3*100)
    #     s4, v4 = round(s4*100), round(v4*100)
        
    #     update_sql = f"""
    #     update color_pallete_taeuk 
    #     set h1={h1}, s1={s1}, v1={v1}, h2={h2}, s2={s2}, v2={v2}, h3={h3}, s3={s3}, v3={v3}, h4={h4}, s4={s4}, v4={v4}
    #     where idx = {idx}
    #     """
    #     print(db.execute(update_sql))
    #     ############################
    
    
    # sql = 'select h1, s1, v1, h2, s2, v2, h3, s3, v3, h4, s4, v4 from stack_img limit 119, 5783'
    sql = 'select h1, s1, v1, h2, s2, v2, h3, s3, v3, h4, s4, v4 from color_pallete_taeuk'
    pallate_list = list(db.select(sql))

    pallate_dp = pd.DataFrame(list(pallate_list), columns=['h1','s1','v1','h2','s2','v2','h3','s3','v3','h4','s4','v4'])

    pallate_x = pallate_dp[['h1','s1','v1','h2','s2','v2','h3','s3','v3','h4','s4','v4']]
    color_x = pallate_dp[['h1']]

    # 컬러 모델 로드
    color_model = joblib.load("test/modelling/model/color_forest.joblib")
    # 콘트라스트 파스텔 모델 로드
    cp_model = joblib.load("test/modelling/model/cp_forest.joblib")
    # 쿨웜 모델 로드
    cw_model = joblib.load("test/modelling/model/cw_forest.joblib")
    # 시즌 모델 로드
    season_model = joblib.load("test/modelling/model/seasons_forest.joblib")
    # 명암 모델 로드
    value_model = joblib.load("test/modelling/model/value_forest.joblib")

    # 모델 실행
    color_pred = color_model.predict(color_x)
    cp_pred = cp_model.predict(pallate_x)
    cw_pred = cw_model.predict(pallate_x)
    season_pred = season_model.predict(pallate_x)
    value_pred = value_model.predict(pallate_x)
    # print(color_pred, cp_pred, cw_pred, season_pred, value_pred)
    
    length = len(pallate_list)
    for i, pallate in enumerate(pallate_list):
        
        try:
            sql = """
            INSERT INTO color_pallete_taeuk(h1,s1,v1,h2,s2,v2,h3,s3,v3,h4,s4,v4,color,cp,cw,season,value)
            VALUES
            (
                {},{},{},
                {},{},{},
                {},{},{},
                {},{},{},
                '{}','{}','{}','{}','{}'
            )
            ON DUPLICATE KEY
            UPDATE color = '{}', cp = '{}', cw = '{}', season = '{}', value = '{}'
            """.format(
                pallate[0],pallate[1],pallate[2],
                pallate[3],pallate[4],pallate[5],
                pallate[6],pallate[7],pallate[8],
                pallate[9],pallate[10],pallate[11],
                color_pred[i],cp_pred[i],cw_pred[i],season_pred[i],value_pred[i],
                color_pred[i],cp_pred[i],cw_pred[i],season_pred[i],value_pred[i],
                )
            # print(sql)
            result = db.execute(sql)
            if result:
                print(length, '/', i, '번째 이미지 insert')
            else:
                print(length, '/', i, '번째 이미지 Error발생 ㅜㅜ@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        except :
            print(length, '/', i, '번째 이미지 TRYCATCH Error발생 ㅜㅜ@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            
            
    print("insert 완료 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")