from masterpiece.models.DbConn import DbConn

class GallaryList():
    """
    GallaryList table
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
        select * from gallary_list {limit_sql}
        """
        
        return self.db.select(sql)

    def insert_mp_info(self, user_idx, image_name, origin_url, masterpiece_url, artist):
        sql = f"insert into gallary_list(user_idx, image_name, origin_url, masterpiece_url, artist) values({user_idx}, '{image_name}', '{origin_url}', '{masterpiece_url}', '{artist}');"
        return self.db.execute(sql)

    def insert_mp_info2(self, user_idx, image_name, origin_url, masterpiece_url, hex1,hex2,hex3,hex4):
        sql = f"insert into gallary_list(user_idx, image_name, origin_url, masterpiece_url, hex1,hex2,hex3,hex4, artist) values({user_idx}, '{image_name}', '{origin_url}', '{masterpiece_url}', '{hex1}', '{hex2}', '{hex3}', '{hex4}', 'color');"
        # 아티스트 부분은 color 로 입력
        return self.db.execute(sql)
    
    def image_filter(self, opt_type, user_idx):
        sql = '''select 
                    a.*, 
                    (select 
                        count(*) like_btn 
                    from 
                        like_btn 
                    where 
                        gl_idx = a.gl_idx) as cnt'''

        if user_idx != None: 
            sql += f''', if(
                        (select count(*) from like_btn where user_idx = {user_idx} AND gl_idx = a.gl_idx) > 0, 
                        'T', 
                        'F') as mylike, 
                        (SELECT user_name FROM user WHERE user_idx = a.user_idx) AS user_name'''

        sql += ''' from 
            gallary_list as a'''

        where = ""
        if opt_type :
            where += " where "
            where_value = ""

            if len(where_value) > 0 : where_value += " and "
            where_value += "artist in ("
            for index, val in enumerate(opt_type.split(',')):
                if index == 0:
                    if val == "cd": where_value += "'color'"
                    else: where_value += "'"+val+"'"
                else:
                    if val == "cd": where_value += ", 'color'"
                    else: where_value += ", '"+val+"'"
            where_value += ")"
                
            where = where + where_value
            
        sql = sql + where + " order by create_date desc limit 100;"
        
        return self.db.select(sql)

    def get_user_like(self, gl_idx, user_idx):
        return self.db.select(f"select * from like_btn where gl_idx = {gl_idx} and user_idx = {user_idx};")

    def set_like(self, gl_idx, user_idx):
        return self.db.execute(f"insert into like_btn(gl_idx, user_idx) values({gl_idx}, {user_idx});")

    def drop_like(self, gl_idx, user_idx):
        return self.db.execute(f"delete from like_btn where gl_idx = {gl_idx} and user_idx = {user_idx};")
