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
    sql_cp = 'select h1, s1, v1, h2, s2, v2, h3, s3, v3, h4, s4, v4, status from croll_cp'
    cp_list = list(db.select(sql_cp))
    sql_cw = 'select h1, s1, v1, h2, s2, v2, h3, s3, v3, h4, s4, v4, status from croll_cw'
    cw_list = list(db.select(sql_cw))

    cp_dp = pd.DataFrame(list(cp_list), columns=['h1','s1','v1','h2','s2','v2','h3','s3','v3','h4','s4','v4','status'])
    cw_dp = pd.DataFrame(list(cw_list), columns=['h1','s1','v1','h2','s2','v2','h3','s3','v3','h4','s4','v4','status'])

    cp_x = cp_dp[['h1','s1','v1','h2','s2','v2','h3','s3','v3','h4','s4','v4']]
    cp_y = cp_dp['status']

    cw_x = cw_dp[['h1','s1','v1','h2','s2','v2','h3','s3','v3','h4','s4','v4']]
    cw_y = cw_dp['status']

    cp_X_train, cp_X_test, cp_y_train, cp_y_test = train_test_split(cp_x, cp_y, test_size=0.3, random_state=999)
    cw_X_train, cw_X_test, cw_y_train, cw_y_test = train_test_split(cw_x, cw_y, test_size=0.3, random_state=999)

    # 학습 진행
    cp_forest = RandomForestClassifier(n_estimators=100)
    cw_forest = RandomForestClassifier(n_estimators=100)

    cp_forest.fit(cp_X_train, cp_y_train)
    cw_forest.fit(cw_X_train, cw_y_train)
 
    # 예측
    cp_y_pred = cp_forest.predict(cp_X_test)
    cw_y_pred = cw_forest.predict(cw_X_test)
 
    # 정확도 확인
    print('CP(contrasting, pastel) 정확도 :', metrics.accuracy_score(cp_y_test, cp_y_pred))
    print('CW(cool, warm) 정확도 :', metrics.accuracy_score(cw_y_test, cw_y_pred))

    # 모델 저장
    joblib.dump(cp_forest, "test/modelling/model/cp_forest.joblib")
    joblib.dump(cw_forest, "test/modelling/model/cw_forest.joblib")

    # 모델 로드
    loaded_cp_rf = joblib.load("test/modelling/model/cp_forest.joblib")
    loaded_cw_rf = joblib.load("test/modelling/model/cw_forest.joblib")

    load_cp_pred = loaded_cp_rf.predict(cp_X_test)
    load_cw_pred = loaded_cw_rf.predict(cw_X_test)
    print('LOAD CP(contrasting, pastel) 정확도 :', metrics.accuracy_score(cp_y_test, load_cp_pred))
    print('LOAD CW(cool, warm) 정확도 :', metrics.accuracy_score(cw_y_test, load_cw_pred))
