#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[93]:


import requests
import json
from DbConn import *
from datetime import datetime, timedelta

def week_dataframe(day):
    db = DbConn()
    
    select_query = """
    select moviecd, audicnt 
    from boxoffice2  
    where  opendt +:day = dailydate and dailydate < TO_DATE('19/01/01', 'YY/mm/dd') and dailydate > TO_DATE('03/01/01', 'YY/mm/dd')  
    order by moviecd
    """
    params = {"day":day}
    select_result = db.execute(select_query,params)

    print("첫주 작업 완료. -----")
    db.disconnect()
    return  select_result

day = 1

def movie2_dataframe():
    db = DbConn()
    
    select_query = """
    select moviecd,  max_audiacc, 
    prod_max, director_avg, 
    director_max,  actors1_max,
    actors2_max, actors3_max,
    actors4_max,
    director_100cnt, prod_avg
    
    from movie2
    where opendt < TO_DATE('19/01/01', 'YY/mm/dd') and opendt > TO_DATE('03/01/01', 'YY/mm/dd') and max_audiacc > 1000000
    order by moviecd
    """
    select_result = db.execute(select_query)

    print("누적 작업 완료. -----")
    db.disconnect()
    return  select_result


def screen_dataframe():
    db = DbConn()
    
    select_query = """
    select moviecd, scrncnt
    
    from boxoffice2
    where dailydate = opendt
    order by moviecd
    """
    select_result = db.execute(select_query)

    print("누적 작업 완료. -----")
    db.disconnect()
    return  select_result

# def max_dataframe():
#     db = DbConn()
    
#     select_query = """
#     select moviecd,  max(audiacc)
#     from boxoffice 
#     group by moviecd
#     order by moviecd
#     """
#     select_result = db.execute(select_query)

#     print("누적 작업 완료. -----")
#     db.disconnect()
#     return  select_result

# print(week_dataframe(13))

print(movie2_dataframe())


# In[94]:


import pandas as pd
df_week= []
for i in range(0,day):
    df_week_column_name = ['mnumber', 'dpeople+'+str(i)]
    df_week.append( pd.DataFrame(week_dataframe(i), columns=df_week_column_name) )



# In[95]:


movie2_dataframe
df_movie2_column_name = ['mnumber', 'sum_total_people','prod_max','director_avg','director_max',
                         'actors1_max', 'actors2_max', 'actors3_max', 'actors4_max',
                         'director_100cnt','prod_avg']
df_movie2 = pd.DataFrame(movie2_dataframe(), columns=df_movie2_column_name )
df_movie2.tail()


# In[96]:


screen_dataframe
df_screen_column_name = ['mnumber', 'screen']
df_screen = pd.DataFrame(screen_dataframe(), columns=df_screen_column_name )
df_screen.tail()


# In[97]:


df = df_movie2
df.tail()


# In[98]:


# df = pd.merge(df_week[0],df_movie2, on='mnumber')

# for i in range(1,day) :
#     df = pd.merge(df_week[i],df, on='mnumber', how='outer')

# df.tail()


# In[99]:


df = pd.merge(df,df_screen, on='mnumber')

df.tail()


# In[100]:


df_movie2_column_name = ['mnumber', 'sum_total_people','prod_max','director_avg','director_max',
                         'actors1_max', 'actors2_max', 'actors3_max', 'actors4_max',
                         'director_100cnt','prod_avg']
for i in df_movie2_column_name:
    df[i] = df[i].fillna(0)
    
df.tail()


# In[101]:


# for i in range(0,day) :
#     df['dpeople+'+str(i)] = df['dpeople+'+str(i)].fillna(0)

# df.tail()


# In[102]:


print(df['sum_total_people'].quantile(q=0.9, interpolation='nearest'),
      df['sum_total_people'].quantile(q=0.8, interpolation='nearest'),
      df['sum_total_people'].quantile(q=0.7, interpolation='nearest'),
      df['sum_total_people'].quantile(q=0.6, interpolation='nearest'),
      df['sum_total_people'].quantile(q=0.5, interpolation='nearest'),
      df['sum_total_people'].quantile(q=0.4, interpolation='nearest'),
      df['sum_total_people'].quantile(q=0.3, interpolation='nearest'),
      df['sum_total_people'].quantile(q=0.2, interpolation='nearest'),
      df['sum_total_people'].quantile(q=0.1, interpolation='nearest'),
      df['sum_total_people'].quantile(q=0, interpolation='nearest')
      
     )

a=df['sum_total_people'].quantile(q=0.9, interpolation='nearest')
b=df['sum_total_people'].quantile(q=0.8, interpolation='nearest')
c=df['sum_total_people'].quantile(q=0.7, interpolation='nearest')
d=df['sum_total_people'].quantile(q=0.6, interpolation='nearest')
e=df['sum_total_people'].quantile(q=0.5, interpolation='nearest')
f=df['sum_total_people'].quantile(q=0.4, interpolation='nearest')
g=df['sum_total_people'].quantile(q=0.3, interpolation='nearest')
h=df['sum_total_people'].quantile(q=0.2, interpolation='nearest')
i=df['sum_total_people'].quantile(q=0.1, interpolation='nearest')
j=df['sum_total_people'].quantile(q=0, interpolation='nearest')


a = 10000000
b = 5000000
c = 2000000
d = 1000000



# 1% 1000만
# 4% 500만
# 24% 100만
# 65% 13만
# 100% 0


# In[103]:


score_list = []
for q in df['sum_total_people']:
    if q >= a:
        score_list.append('A')
    elif q >= b:
        score_list.append('B')
    elif q >= c:
        score_list.append('C')
    elif q >= d:
        score_list.append('D')
#     elif q >= e:
#         score_list.append('E')
#     elif q >= f:
#         score_list.append('F')
#     elif q >= g:
#         score_list.append('G')
#     elif q >= h:
#         score_list.append('H')
#     elif q >= i:
#         score_list.append('I')
#     else:
#         score_list.append('J')
   

df['score'] = score_list
df['score'].head()


# In[104]:


df.groupby('score')['score'].count()


# In[105]:


X = df.drop(['mnumber', 'sum_total_people','score'], axis=1)
X.tail()


# In[106]:


Y=df['score']


# In[107]:


import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_score

# train, test 7:3
X_train, X_test, y_train, y_test = train_test_split(X,Y,
                                                   test_size=0.3, random_state=999)


# In[108]:


from sklearn.ensemble import GradientBoostingClassifier
gbc = GradientBoostingClassifier(max_depth=4, learning_rate=0.3,  random_state=999)
gbc.fit(X_train,y_train)
gbc.score(X_train,y_train),gbc.score(X_test,y_test)



# In[109]:


from sklearn.model_selection import GridSearchCV

param = {
    'max_depth' : [3,4,5,6],
    'learning_rate' : [0.1,0.15, 0.2, 0.25, 0.3]
}

grid_cv_gbc = GridSearchCV(gbc, param_grid=param, cv=2, verbose=1, n_jobs=-1)
grid_cv_gbc.fit(X_train, y_train.values)
gbc_best = grid_cv_gbc.best_estimator_
print('최적 하이퍼 파라미터: \n', grid_cv_gbc.best_params_)
print('최고 예측 정확도: {0:.4f}'.format(grid_cv_gbc.best_score_))


# In[110]:


from sklearn.ensemble import AdaBoostClassifier
adb = AdaBoostClassifier(n_estimators=30, 
                        random_state=10, 
                        learning_rate=0.2)
adb.fit(X_train,y_train)
adb.score(X_train,y_train),adb.score(X_test,y_test)


# In[111]:


from sklearn.model_selection import GridSearchCV

param = {
    'n_estimators' : [10,20,30,40,50],
    'learning_rate' : [0.1,0.15, 0.2]
}

grid_cv_adb = GridSearchCV(adb, param_grid=param, cv=2, verbose=1, n_jobs=-1)
grid_cv_adb.fit(X_train, y_train.values)
adb_best = grid_cv_adb.best_estimator_
print('최적 하이퍼 파라미터: \n', grid_cv_adb.best_params_)
print('최고 예측 정확도: {0:.4f}'.format(grid_cv_adb.best_score_))


# In[112]:


rfc = RandomForestClassifier(n_estimators=70, random_state=999)
rfc.fit(X_train,y_train)
rfc.score(X_train,y_train), rfc.score(X_test,y_test)


# In[113]:


from sklearn.model_selection import GridSearchCV

param = {
    'n_estimators' : [10,20,30,40,50,60,70,80,90,100]
}

grid_cv_rfc = GridSearchCV(rfc, param_grid=param, cv=2, verbose=1, n_jobs=-1)
grid_cv_rfc.fit(X_train, y_train.values)
rfc_best = grid_cv_rfc.best_estimator_
print('최적 하이퍼 파라미터: \n', grid_cv_rfc.best_params_)
print('최고 예측 정확도: {0:.4f}'.format(grid_cv_rfc.best_score_))


# In[114]:


from sklearn.metrics import accuracy_score
# GridSearchCV를 이용해 최적으로 학습된 estimators로 예측 수행
gb_pred_gbc = grid_cv_gbc.best_estimator_.predict(X_test)
gb_accuracy_gbc = accuracy_score(y_test, gb_pred_gbc)
print('GBM 정확도: {0:.4f}'.format(gb_accuracy_gbc))

gb_pred_adb = grid_cv_adb.best_estimator_.predict(X_test)
gb_accuracy_adb = accuracy_score(y_test, gb_pred_adb)
print('GBM 정확도: {0:.4f}'.format(gb_accuracy_adb))

gb_pred_rfc = grid_cv_rfc.best_estimator_.predict(X_test)
gb_accuracy_rfc = accuracy_score(y_test, gb_pred_rfc)
print('GBM 정확도: {0:.4f}'.format(gb_accuracy_rfc))


# In[115]:


from sklearn.ensemble import VotingClassifier
votigC = VotingClassifier(estimators=[
    ('gbc',gbc_best),('adb',adb_best),('rfc',rfc_best)], voting='hard', n_jobs=3 )
votigC = votigC.fit(X_train,y_train) 
#예측진행
prediction = votigC.predict(X_test)


# In[116]:


from sklearn.externals import joblib 
# 객체를 pickled binary file 형태로 저장한다 
file_name = '1000_500_200_100_voting_model.pkl' 
joblib.dump(votigC, file_name) 


# In[117]:


from sklearn.externals import joblib 
# pickled binary file 형태로 저장된 객체를 로딩한다 
file_name = '1000_500_200_100_voting_model.pkl' 
votigC = joblib.load(file_name) 


# In[118]:


# cunfuse matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 보팅한 컨퓨전매트릭스
conMat = pd.DataFrame(confusion_matrix(y_test,prediction),
#                          index=['True[A]', 'True[B]', 'True[C]', 'True[D]',  'True[E]','True[F]', 'True[G]', 'True[H]', 'True[J]',  'True[K]'],
#                          columns=['Pred[A]', 'Pred[B]', 'Pred[C]', 'Pred[D]',  'Pred[E]','Pred[F]', 'Pred[G]', 'Pred[H]', 'Pred[J]',  'Pred[K]'])
                         index=['True[A]', 'True[B]', 'True[C]', 'True[D]'],
                         columns=['Pred[A]', 'Pred[B]', 'Pred[C]', 'Pred[D]'])

gb_accuracy_voting = accuracy_score(y_test, prediction)
print('초대박 :',a,'명')
print('대박 :',b,'명')
print('중박 :',c,'명')
print('쪽박 :',d,'명')
print('GBM 정확도: {0:.4f}'.format(gb_accuracy_voting))
 # 정확도, precision, recall, f1
conMat


# In[119]:


gb_accuracy_voting = accuracy_score(y_test, prediction)
print('GBM 정확도: {0:.4f}'.format(gb_accuracy_voting))


# In[120]:


# cunfuse matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
rfc.fit(X_train, y_train) #랜덤포레스트의 컨퓨전 매트릭스

y_pred = rfc.predict(X_test)

conMat = pd.DataFrame(confusion_matrix(y_test,y_pred),
#                         index=['True[A]', 'True[B]', 'True[C]', 'True[D]',  'True[E]','True[F]', 'True[G]', 'True[H]', 'True[J]',  'True[K]'],
#                          columns=['Pred[A]', 'Pred[B]', 'Pred[C]', 'Pred[D]',  'Pred[E]','Pred[F]', 'Pred[G]', 'Pred[H]', 'Pred[J]',  'Pred[K]'])
                         index=['True[A]', 'True[B]', 'True[C]', 'True[D]'],
                         columns=['Pred[A]', 'Pred[B]', 'Pred[C]', 'Pred[D]'])
 # 정확도, precision, recall, f1
conMat


# In[121]:


gb_accuracy_rfc = accuracy_score(y_test, y_pred)
print('GBM 정확도: {0:.4f}'.format(gb_accuracy_rfc))


# In[122]:


feat_labels = X.columns
feat_labels


# In[123]:


import numpy as np

plt.style.use('fivethirtyeight')
fig = plt.figure(figsize=(20,15))
                 
importances = rfc.feature_importances_
indices = np.argsort(importances)[::-1]
for f in range(X_train.shape[1]):
    print("%2d) %-*s %f"%(f+1,30,feat_labels[indices[f]],
                         importances[indices[f]]))
plt.title('Feature importance')
plt.bar(range(X_train.shape[1]), importances[indices], align='center')
plt.xticks(range(X_train.shape[1]), feat_labels[indices], rotation=90,fontsize=30)
plt.tight_layout()
plt.savefig('randomforest.png')
plt.show()


# In[124]:


# 1~7 일 정도의 데이터가 제일 중요하고 이후날짜의 데이터는 크게 중요치 않음


# In[86]:


df.head()


# In[87]:


df.columns


# In[88]:


from patsy import dmatrices
from statsmodels.stats.outliers_influence import variance_inflation_factor

# y, X = dmatrices('sum_total_people ~ mnumber+ actors1_max+ actors2_max+actors3_max+ actors4_max+ actors1_avg+ actors2_avg+actors3_avg+ actors4_avg+ actors1_100cnt+ actors2_100cnt+actors3_100cnt+ actors4_100cnt+ prod_max+ prod_avg+prod_100cnt+ genre_max+ genre_avg+ genre_100cnt+ genresub_max+genresub_avg+ genresub_100cnt+ director_max+ director_avg+director_100cnt+ screen' , df, return_type = 'dataframe')
y, X = dmatrices('sum_total_people ~ mnumber+ actors1_max+ actors2_max+actors3_max+ actors4_max+  prod_max+ director_max+ screen' , df, return_type = 'dataframe')

vif = pd.DataFrame()
vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif["features"] = X.columns 
vif


# In[ ]:




