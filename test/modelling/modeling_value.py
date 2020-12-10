import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pandas as pd
import numpy as np 
from  classes.DbConn import DbConn

import matplotlib.pyplot as plt 

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler #거리계산을 위한 표준화 작업
from sklearn.metrics import confusion_matrix #모델 평가 
from sklearn.metrics import classification_report


db = DbConn()
sql_value = 'select h1, s1, v1, h2, s2, v2, h3, s3, v3, h4, s4, v4, status from croll_value'
value_list = list(db.select(sql_value))

value_dp = pd.DataFrame(list(value_list), columns=['h1','s1','v1','h2','s2','v2','h3','s3','v3','h4','s4','v4','status'])

value_x = value_dp[['h1','s1','v1','h2','s2','v2','h3','s3','v3','h4','s4','v4']]
value_y = value_dp['status']

value_X_train, value_X_test, value_y_train, value_y_test = train_test_split(value_x, value_y, test_size=0.3, random_state=999)
# 거리 계산을 위한 표준화 작업 Z-score 

scaler = StandardScaler() # Scaler 객체 생성 
scaler.fit(value_X_train) # 표준화를 위한 평균과 표준편차 계산 

value_X_train = scaler.transform(value_X_train) #표준화 수행 

value_X_test = scaler.transform(value_X_test)

# z-score 표준화 수행 결과 확인
# for col in range(4):
#     print(f'평균 = {value_X_train[:, col].mean()}, 표준편차= {value_X_train[:, col].std()}')

# for col in range(4):
#     print(f'평균 = {value_X_test[:, col].mean()}, 표준편차= {value_X_test[:, col].std()}')


# 학습 진행
value_knn = KNeighborsClassifier(n_neighbors = 10)
value_knn.fit(value_X_train,value_y_train)

# 예측
value_y_pred = value_knn.predict(value_X_test)
# print(value_y_pred)

# 정확도 확인
conf_matrix = confusion_matrix(value_y_test,value_y_pred)
print(conf_matrix)

report= classification_report(value_y_test,value_y_pred)
print(report)


#모델 개선 
# errors = []
# for i in range(1, 31):
#     value_knn = KNeighborsClassifier(n_neighbors = i)
#     value_knn.fit(value_X_train,value_y_train)
#     pred_i = value_knn.predict(value_X_test)
#     errors.append(np.mean(pred_i != value_y_test))
# print(errors)


# plt.plot(range(1,31),errors,marker ='o')
# plt.title('Mean error with K-Value')
# plt.xlabel('k-value')
# plt.ylabel('mean error')
# plt.show()