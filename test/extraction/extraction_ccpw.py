'''
비비드, 파스텔, 웜톤, 쿨톤 DB insert

H : 360 (도)
S : 0 ~ 100 (%)
V : 0 ~ 100 (%)

Spuit.get_hsv360 사용
'''
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from  classes.DbConn import DbConn
from  classes.Spuit import Spuit

dir_names = ['contrasting', 'pastel', 'cool', 'warm']
db = DbConn()

hsv_list = []

for dir_name in dir_names:
    path = "test/crawling/images/" + dir_name
    file_list = os.listdir(path)
    cnt = 0

    print('----------------------------------------------------')
    print('------------------' + dir_name + '------------------')
    print('----------------------------------------------------')

    for img_name in file_list:
        img_path = path + "/" + img_name
        sp = Spuit(img_path)
        hsv = sp.get_hsv360()
        img_info_list = []
        cnt = cnt + 1

        for i in hsv:
            img_info_list.append(i[0])
            img_info_list.append(i[1])
            img_info_list.append(i[2])
        
        img_info_list.append(dir_name)
        img_info_list.append(img_name)

        del sp
    
        hsv_list.append(img_info_list)

        print(str(cnt) + " : " + img_path)
        print(' hsv : ', hsv)
        print(' img_info_list : ', img_info_list)
        print(' hsv_list len : ', len(hsv_list))
        print('')
    
    print(dir_name + ' len : ' + str(len(file_list)))
    print('db insert len : ' + str(len(img_info_list)))

    if dir_name in ('contrasting', 'pastel') :
        sql = "insert into crawl_cp(h1,s1,v1,h2,s2,v2,h3,s3,v3,h4,s4,v4,status,filename) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        db.executemany(sql, hsv_list)
    else:
        sql = "insert into crawl_cw(h1,s1,v1,h2,s2,v2,h3,s3,v3,h4,s4,v4,status,filename) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        db.executemany(sql, hsv_list)

    hsv_list = []
    
    print('----------------------------------------------------')
    print('----------------------------------------------------')
    print('----------------------------------------------------')


