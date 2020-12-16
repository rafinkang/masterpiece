import os, sys
from colorutils.convert import hsv_to_hex
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from  classes.Spuit import Spuit
import pandas as pd
import joblib

from  classes.DbConn import DbConn

if __name__ == '__main__':

    made_name = 'jiyeon'

    path = "test/crawling/images/color_combo" # color_combo1.png
    file_list = os.listdir(path)

    pallates = []
    color_x = []
    cnt = 0

    for img_name in file_list:
        img_path = path + "/" + img_name

        print(str(cnt) + " : " + img_path)

        sp = Spuit(img_path)
        hsv = sp.get_hsv360()
        img_info_list = []
        cnt = cnt + 1

        for i in hsv:
            if i[0] == 360 :
                img_info_list.append(0)
            else:
                img_info_list.append(i[0])
            img_info_list.append(i[1])
            img_info_list.append(i[2])

        del sp
    
        pallates.append(img_info_list)
        color_x.append([img_info_list[0]])

        print(' hsv : ', hsv)
        print(' img_info_list : ', img_info_list)
        print(' pallates len : ', len(pallates))
        print('')

    pallate_x = pd.DataFrame(pallates, columns=['h1', 's1', 'v1', 'h2', 's2', 'v2', 'h3', 's3', 'v3', 'h4', 's4', 'v4'])
    color_x = pallate_x[['h1']]


    db = DbConn()

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
    

    color_pred = color_model.predict(color_x)
    cp_pred = cp_model.predict(pallate_x)
    cw_pred = cw_model.predict(pallate_x)
    season_pred = season_model.predict(pallate_x)
    value_pred = value_model.predict(pallate_x)

    length = len(pallates)
    for i, pallate in enumerate(pallates):
        hex1 = hsv_to_hex((pallate[0],pallate[1]/100,pallate[2]/100))
        hex2 = hsv_to_hex((pallate[3],pallate[4]/100,pallate[5]/100))
        hex3 = hsv_to_hex((pallate[6],pallate[7]/100,pallate[8]/100))
        hex4 = hsv_to_hex((pallate[9],pallate[10]/100,pallate[11]/100))
        
        try:
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
            ON DUPLICATE KEY
            UPDATE color = '{}', cp = '{}', cw = '{}', season = '{}', value = '{}', hex1 = '{}', hex2 = '{}', hex3 = '{}', hex4 = '{}',made = '{}'
            """.format(
                pallate[0],pallate[1],pallate[2],
                pallate[3],pallate[4],pallate[5],
                pallate[6],pallate[7],pallate[8],
                pallate[9],pallate[10],pallate[11],
                color_pred[i],cp_pred[i],cw_pred[i],season_pred[i],value_pred[i],
                hex1, hex2, hex3, hex4, made_name,
                color_pred[i],cp_pred[i],cw_pred[i],season_pred[i],value_pred[i],
                hex1, hex2, hex3, hex4, made_name
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