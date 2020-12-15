import os, sys
from colorutils.convert import hsv_to_hex
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pandas as pd
import joblib

from  classes.DbConn import DbConn

import csv
color_list =[]
cnt =0

f = open('./test/modelling/color_minsu.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
for line in rdr:
    cnt += 1
    # print(line)
    # line.append("minsu")
    # color_list.append(line)

    db = DbConn()
    # sql = """
    #         insert into color_pallete_minsu (hex1,hex2,hex3,hex4,made)
    #         values
    #         (:hex1,:hex2,:hex3,:hex4, 'minsu')
    # """
    # params = {"hex1": line[0], "hex2": line[1], "hex3": line[2], "hex4": line[3]}
    # print(sql,params)
    # db.execute(sql,params)
    
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
# print(color_list)


