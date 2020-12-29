from masterpiece.models.DbConn import DbConn
import json

class ColorList():
    """
    ColorList table
    """
    def __init__(self):
        self.db = DbConn()
        
    def select(self, sql, args=None):
        return self.db.select(sql, args)
    
    def execute(self, sql, args=None):
        return self.db.execute(sql, args)
    
    def executemany(self, sql, args=None):
        return self.db.executemany(sql, args)
    
    def select_all(self, start = None, end = None):
        limit_sql = ""
        if start is not None:
            limit_sql = "limit " + str(start)
        if end is not None:
            limit_sql = limit_sql + ', '+ str(end)
        
        sql = f"""
        select * from color_list {limit_sql}
        """
        
        return self.db.select(sql)

    def insert_color(self, user_idx, path, color_pick):
        color_pick = json.loads(color_pick)
        sql = f"""
        insert into color_list(user_idx, h1,s1,v1,h2,s2,v2,h3,s3,v3,h4,s4,v4, color, cp, cw, season, value, hex1, hex2, hex3, hex4, origin_url) 
        values ({user_idx},
            '{color_pick['h1']}', '{color_pick['s1']}', '{color_pick['v1']}',
            '{color_pick['h2']}', '{color_pick['s2']}', '{color_pick['v2']}', 
            '{color_pick['h3']}', '{color_pick['s3']}', '{color_pick['v3']}', 
            '{color_pick['h4']}', '{color_pick['s4']}', '{color_pick['v4']}', 
            '{color_pick['color']}', '{color_pick['cp']}', '{color_pick['cw']}', '{color_pick['season']}', '{color_pick['value']}', 
            '{color_pick['hex1']}', '{color_pick['hex2']}', '{color_pick['hex3']}', '{color_pick['hex4']}', '{path}'
        )
        """
        return self.db.execute(sql)
        