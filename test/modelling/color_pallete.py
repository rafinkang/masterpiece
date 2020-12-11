import os, sys
from colorutils.convert import hsv_to_hex
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pandas as pd
import joblib

from  classes.DbConn import DbConn

if __name__ == '__main__':

    db = DbConn()
    # sql = 'select h1, s1, v1, h2, s2, v2, h3, s3, v3, h4, s4, v4 from stack_img limit 119, 5783'
    sql = 'select h1, s1, v1, h2, s2, v2, h3, s3, v3, h4, s4, v4 from stack_img'
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
        hex1 = hsv_to_hex((pallate[0],pallate[1]/100,pallate[2]/100))
        hex2 = hsv_to_hex((pallate[3],pallate[4]/100,pallate[5]/100))
        hex3 = hsv_to_hex((pallate[6],pallate[7]/100,pallate[8]/100))
        hex4 = hsv_to_hex((pallate[9],pallate[10]/100,pallate[11]/100))
        
        try:
            sql = """
            INSERT INTO color_pallete(h1,s1,v1,h2,s2,v2,h3,s3,v3,h4,s4,v4,color,cp,cw,season,value,hex1,hex2,hex3,hex4)
            VALUES
            (
                {},{},{},
                {},{},{},
                {},{},{},
                {},{},{},
                '{}','{}','{}','{}','{}',
                '{}','{}','{}','{}'
            )
            ON DUPLICATE KEY
            UPDATE color = '{}', cp = '{}', cw = '{}', season = '{}', value = '{}', hex1 = '{}', hex2 = '{}', hex3 = '{}', hex4 = '{}'
            """.format(
                pallate[0],pallate[1],pallate[2],
                pallate[3],pallate[4],pallate[5],
                pallate[6],pallate[7],pallate[8],
                pallate[9],pallate[10],pallate[11],
                color_pred[i],cp_pred[i],cw_pred[i],season_pred[i],value_pred[i],
                hex1, hex2, hex3, hex4,
                color_pred[i],cp_pred[i],cw_pred[i],season_pred[i],value_pred[i],
                hex1, hex2, hex3, hex4                
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