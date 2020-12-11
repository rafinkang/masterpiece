# 이곳은 컬러 값 hsv로 변환할 파일 입니다.
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from classes.Spuit import Spuit
from classes.DbConn import DbConn

db = DbConn()

images_dir = 'test\crawling\images\delete'
folder_list = os.listdir(images_dir)

for folder in folder_list:
    folder_dir = images_dir+'/'+folder
    file_list = os.listdir(folder_dir)
    length = len(file_list)
    
    result_list = []
    cnt = 0
    for filename in file_list:
        cnt += 1
        print(folder, cnt, '/', length, filename)

        sql = "delete from crawl_seasons where filename = '" + filename + "'"
        # print(filename)
        # break
        print(db.execute(sql)) 

        # try:
        #     file_dir = images_dir+'/'+folder+'/'+filename
        #     image = Spuit(file_dir)
        #     hsv = image.get_hsv360()
        #     hsv_list = []
            
        #     for i in hsv:
        #         hsv_list.append(i[0]) 
        #         hsv_list.append(i[1]) 
        #         hsv_list.append(i[2]) 
            
        #     hsv_list.append(folder)
        #     hsv_list.append(filename)
        #     result_list.append(hsv_list)
        #     del image
        # except:
        #     print("Error!!!!!!!!!!!!!!!!!!!!!!")

    # sql = "insert into crawl_seasons(h1,s1,v1,h2,s2,v2,h3,s3,v3,h4,s4,v4,status,filename) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    print(db.executemany(sql, result_list))
    print('============================================================')
    print(folder, ' 작업 완료==========================================')
    print('============================================================')


print('============================================================')
print('==========전체 작업 완료=====================================')
print('============================================================')
