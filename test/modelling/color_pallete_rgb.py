import os, sys

from colorutils.convert import hsv_to_hex, hsv_to_rgb, hsv_to_web
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from colorutils import Color

from classes.DbConn import DbConn


if __name__ == '__main__':

    db = DbConn()
    sql = 'select * from color_pallete limit 10'
    color_list = list(db.select(sql))
    # print(color_list)
    for color in color_list:
        # print(color)
        # c = Color(hsv=(color[1]/360,color[2]/100,color[3]/100))
        # print(c)
        # print(c.hex, c.rgb)
        print(hsv_to_hex((color[1]/360,color[2]/100,color[3]/100)))
        print(hsv_to_web((color[1]/360,color[2]/100,color[3]/100)))
        print(hsv_to_rgb((color[1]/360,color[2]/100,color[3]/100)))