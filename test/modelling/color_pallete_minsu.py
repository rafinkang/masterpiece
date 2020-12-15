import os, sys
from colorutils.convert import hsv_to_hex
from colorutils.convert import hex_to_hsv
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pandas as pd
import joblib

from  classes.DbConn import DbConn

import csv
color_list =[]
cnt =0

def csv_to_testdb():
    global cnt
    f = open('./test/modelling/color_minsu.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        cnt += 1

        db = DbConn()
        
        sql = """
                insert into color_pallete_minsu (hex1,hex2,hex3,hex4,made)
                VALUES
                (
                    '{}','{}','{}','{}','{}'
                )
                """.format(
                    line[0], line[1], line[2],  line[3]   , 'minsu'                        
                    )
        print(sql)
        result = db.execute(sql)
        if result:
            print( cnt, '번째 이미지 insert')
        else:
            print( cnt, '번째 이미지 Error발생 ㅜㅜ@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

    f.close() 


def csv_to_db():
    global cnt
    f = open('./test/modelling/color_minsu.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        cnt += 1

        
        hex1,hex2,hex3,hex4 = line
        # print(hex1,hex2,hex3,hex4)
        h1,s1,v1 = hex_to_hsv(hex1)
        h2,s2,v2 = hex_to_hsv(hex2)
        h3,s3,v3 = hex_to_hsv(hex3)
        h4,s4,v4 = hex_to_hsv(hex4)
        s1 = s1*100
        s2 = s2*100
        s3 = s3*100
        s4 = s4*100
        v1 = v1*100
        v2 = v2*100
        v3 = v3*100
        v4 = v4*100
        # print(h1,s1,v1,h2,s2,v2,h3,s3,v3,h4,s4,v4)
        hsv = (h1,s1,v1,h2,s2,v2,h3,s3,v3,h4,s4,v4)
        templist =[]
        templist.append(hsv)
        # print(templist)
        
        pallate_dp = pd.DataFrame(templist, columns=['h1','s1','v1','h2','s2','v2','h3','s3','v3','h4','s4','v4'])
        # print(pallate_dp)
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
        print(color_pred, cp_pred, cw_pred, season_pred, value_pred)

        db = DbConn()
        
        sql = """
            INSERT INTO color_pallete(h1,s1,v1,h2,s2,v2,h3,s3,v3,h4,s4,v4,color,cp,cw,season,value,hex1,hex2,hex3,hex4,made)
            VALUES
            (
                {},{},{},
                {},{},{},
                {},{},{},
                {},{},{},
                '{}','{}','{}','{}','{}',
                '{}','{}','{}','{}','{}'
            )
            """.format(
                int(h1),int(s1),int(v1),
                int(h2),int(s2),int(v2),
                int(h3),int(s3),int(v3),
                int(h4),int(s4),int(v4),
                color_pred[0], cp_pred[0], cw_pred[0], season_pred[0], value_pred[0],
                hex1,hex2,hex3,hex4, 'minsu'
            )
        print(sql)
        result = db.execute(sql)
        if result:
            print( cnt, '번째 이미지 insert')
        else:
            print( cnt, '번째 이미지 Error발생 ㅜㅜ@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

    f.close() 

csv_to_db()
