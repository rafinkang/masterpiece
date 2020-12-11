'''
비비드, 파스텔, 웜톤, 쿨톤 make and load model

비비드 : contrasting
파스텔 : pastel
웜톤 : cool
쿨톤 : warm

'''

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pandas as pd
import joblib

from  classes.DbConn import DbConn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
 
if __name__ == '__main__':

    db = DbConn()
    sql_value = 'select h1, s1, v1, h2, s2, v2, h3, s3, v3, h4, s4, v4, status from crawl_value'
    value_list = list(db.select(sql_value))

    value_dp = pd.DataFrame(list(value_list), columns=['h1','s1','v1','h2','s2','v2','h3','s3','v3','h4','s4','v4','status'])


    value_x = value_dp[['h1','s1','v1','h2','s2','v2','h3','s3','v3','h4','s4','v4']]
    value_y = value_dp['status'] 

   
    value_X_train, value_X_test, value_y_train, value_y_test = train_test_split(value_x, value_y, test_size=0.3, random_state=999)


    # 학습 진행
    value_forest = RandomForestClassifier(n_estimators=100)

    value_forest.fit(value_X_train, value_y_train)

    # 예측
    value_y_pred = value_forest.predict(value_X_test)
    # print(value_y_pred)
 
    # 정확도 확인
    print('value(high,low) 정확도 :', metrics.accuracy_score(value_y_test, value_y_pred))


    # 모델 저장
    joblib.dump(value_forest, "test/modelling/model/value_forest.joblib")


    # 모델 로드
    loaded_value_rf = joblib.load("test/modelling/model/value_forest.joblib")


    load_value_pred = loaded_value_rf.predict(value_X_test)

    print('LOAD value(high, low) 정확도 :', metrics.accuracy_score(value_y_test, load_value_pred))

