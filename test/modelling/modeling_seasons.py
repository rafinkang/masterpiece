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
    sql_seasons = 'select h1, s1, v1, h2, s2, v2, h3, s3, v3, h4, s4, v4, status from crawl_seasons'
    seasons_list = list(db.select(sql_seasons))
    
    seasons_dp = pd.DataFrame(list(seasons_list), columns=['h1','s1','v1','h2','s2','v2','h3','s3','v3','h4','s4','v4','status'])

    seasons_x = seasons_dp[['h1','s1','v1','h2','s2','v2','h3','s3','v3','h4','s4','v4']]
    seasons_y = seasons_dp['status']

    seasons_X_train, seasons_X_test, seasons_y_train, seasons_y_test = train_test_split(seasons_x, seasons_y, test_size=0.3)

    # 학습 진행
    seasons_forest = RandomForestClassifier(n_estimators=100)

    seasons_forest.fit(seasons_X_train, seasons_y_train)

    # 예측
    seasons_y_pred = seasons_forest.predict(seasons_X_test)

    # 정확도 확인
    print('Seasons 정확도 :', metrics.accuracy_score(seasons_y_test, seasons_y_pred))

    # 모델 저장
    joblib.dump(seasons_forest, "test/modelling/model/seasons_forest.joblib")

    # 모델 로드
    loaded_seasons_rf = joblib.load("test/modelling/model/seasons_forest.joblib")

    load_seasons_pred = loaded_seasons_rf.predict(seasons_X_test)
    print('LOAD seasons 정확도 :', metrics.accuracy_score(seasons_y_test, load_seasons_pred))

    from sklearn.metrics import confusion_matrix
    conMat = pd.DataFrame(confusion_matrix(seasons_y_test,seasons_y_pred),
                        index=['True[autumn]', 'True[spring]', 'True[summer]', 'True[winter]'],
                        columns=['Pred[autumn]', 'Pred[spring]', 'Pred[summer]', 'Pred[winter]'])
    print(conMat)

    # print(seasons_X_test, seasons_y_test, seasons_y_pred)
    seasons_y_pred = pd.DataFrame(seasons_y_pred)
    
    #df.to_csv('daum_real_time_keyword.csv', index=False)
    # seasons_X_test.to_csv('seasons_X_test.csv', index=True, encoding='cp949') #encoding 옵션: csv 파일에서 한글 (컬럼 혹은 내용) 읽어올 때 encoding='cp949' (혹은 encoding='euc-kr') 옵션 사용, 엑셀의 csv 파일 utf-8 인코딩 (유니코드) 인식 버그
    # seasons_y_test.to_csv('seasons_y_test.csv', index=True, encoding='cp949') #encoding 옵션: csv 파일에서 한글 (컬럼 혹은 내용) 읽어올 때 encoding='cp949' (혹은 encoding='euc-kr') 옵션 사용, 엑셀의 csv 파일 utf-8 인코딩 (유니코드) 인식 버그
    # seasons_y_pred.to_csv('seasons_y_pred.csv', index=False, encoding='cp949') #encoding 옵션: csv 파일에서 한글 (컬럼 혹은 내용) 읽어올 때 encoding='cp949' (혹은 encoding='euc-kr') 옵션 사용, 엑셀의 csv 파일 utf-8 인코딩 (유니코드) 인식 버그
    # seasons_dp2.to_csv('seasons_dp2.csv', index=True, encoding='cp949') #encoding 옵션: csv 파일에서 한글 (컬럼 혹은 내용) 읽어올 때 encoding='cp949' (혹은 encoding='euc-kr') 옵션 사용, 엑셀의 csv 파일 utf-8 인코딩 (유니코드) 인식 버그
    