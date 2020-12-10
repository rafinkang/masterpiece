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
    sql = 'select h1, status from croll_color'
    color_list = list(db.select(sql))

    color_dp = pd.DataFrame(list(color_list), columns=['h1','status'])

    color_x = color_dp[['h1']]
    color_y = color_dp['status']

    color_X_train, color_X_test, color_y_train, color_y_test = train_test_split(color_x, color_y, test_size=0.3, random_state=999)

    # 학습 진행
    color_forest = RandomForestClassifier(n_estimators=100)

    color_forest.fit(color_X_train, color_y_train)

    # 예측
    color_y_pred = color_forest.predict(color_X_test)

    # 정확도 확인
    print('color(contrasting, pastel) 정확도 :', metrics.accuracy_score(color_y_test, color_y_pred))

    # 모델 저장
    joblib.dump(color_forest, "test/modelling/model/color_forest.joblib")

    # 모델 로드
    loaded_color_rf = joblib.load("test/modelling/model/color_forest.joblib")

    load_color_pred = loaded_color_rf.predict(color_X_test)
    print('LOAD color(contrasting, pastel) 정확도 :', metrics.accuracy_score(color_y_test, load_color_pred))

"""
color 분류

UPDATE croll_color SET STATUS = 'red' WHERE h1 > 345 OR h1 <= 15;
UPDATE croll_color SET STATUS = 'orange' WHERE h1 > 15 and h1 <= 45;
UPDATE croll_color SET STATUS = 'yellow' WHERE h1 > 45 and h1 <= 75;
UPDATE croll_color SET STATUS = 'chartreuse green' WHERE h1 > 75 and h1 <= 105;
UPDATE croll_color SET STATUS = 'green' WHERE h1 > 105 and h1 <= 135;
UPDATE croll_color SET STATUS = 'spring green' WHERE h1 > 135 and h1 <= 165;
UPDATE croll_color SET STATUS = 'cyan' WHERE h1 > 165 and h1 <= 195;
UPDATE croll_color SET STATUS = 'azure' WHERE h1 > 195 and h1 <= 225;
UPDATE croll_color SET STATUS = 'blue' WHERE h1 > 225 and h1 <= 255;
UPDATE croll_color SET STATUS = 'violet' WHERE h1 > 255 and h1 <= 285;
UPDATE croll_color SET STATUS = 'magenta' WHERE h1 > 285 and h1 <= 315;
UPDATE croll_color SET STATUS = 'rose' WHERE h1 > 315 and h1 <= 345;
"""