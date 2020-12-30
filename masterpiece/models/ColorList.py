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
        
        
    def list_filter(self, color_type = None, season_type = None, cw_type = None, cp_type = None, value_type = None, limit_start = 0, limit_end = 100, user_idx = None):
        # sql = "select * from color_list"        
        sql = '''
        select a.*, (
                select count(*) like_btn 
                from like_btn 
                where cl_idx = a.cl_idx
            ) as cnt, (
                select user_name from user where user_idx = a.user_idx
            ) as user_name
        '''

        if user_idx != None: 
            sql += f'''
            , if(
            (select count(*) from like_btn where user_idx = {user_idx} AND cl_idx = a.cl_idx) > 0, 
            'T', 'F') as mylike
            '''

        sql += ''' from 
            color_list as a'''
        
        
        where = ""
        if color_type or season_type or cw_type or cp_type or value_type:
            where += " where "
            where_value = ""
            
            if color_type: 
                if len(where_value) > 0 : where_value += " and "
                where_value += "color in ("
                for index, val in enumerate(color_type.split(',')):
                    if index == 0:
                        where_value += "'"+val+"'"
                    else:
                        where_value += ", '"+val+"'"
                where_value += ")"
                
            if season_type: 
                if len(where_value) > 0 : where_value += " and "
                where_value += "season in ("
                for index, val in enumerate(season_type.split(',')):
                    if index == 0:
                        where_value += "'"+val+"'"
                    else:
                        where_value += ", '"+val+"'"
                where_value += ")"
                
            if cw_type: 
                if len(where_value) > 0 : where_value += " and "
                where_value += "cw in ("
                for index, val in enumerate(cw_type.split(',')):
                    if index == 0:
                        where_value += "'"+val+"'"
                    else:
                        where_value += ", '"+val+"'"
                where_value += ")"
                
            if cp_type: 
                if len(where_value) > 0 : where_value += " and "
                where_value += "cp in ("
                for index, val in enumerate(cp_type.split(',')):
                    if index == 0:
                        where_value += "'"+val+"'"
                    else:
                        where_value += ", '"+val+"'"
                where_value += ")"
                
            if value_type: 
                if len(where_value) > 0 : where_value += " and "
                where_value += "value in ("
                for index, val in enumerate(value_type.split(',')):
                    if index == 0:
                        where_value += "'"+val+"'"
                    else:
                        where_value += ", '"+val+"'"
                where_value += ")"
                
                
            where = where + where_value
            
        sql = sql + where + f" limit {limit_start}, {limit_end};"
        
        return self.db.select(sql)
    
    
    def get_user_like(self, cl_idx, user_idx):
        return self.db.select(f"select * from like_btn where cl_idx = {cl_idx} and user_idx = {user_idx};")

    def set_like(self, cl_idx, user_idx):
        return self.db.execute(f"insert into like_btn(cl_idx, user_idx) values({cl_idx}, {user_idx});")

    def drop_like(self, cl_idx, user_idx):
        return self.db.execute(f"delete from like_btn where cl_idx = {cl_idx} and user_idx = {user_idx};")
