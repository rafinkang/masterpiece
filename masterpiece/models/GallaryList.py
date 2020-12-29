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
        sql = f"insert into gallary_list(user_idx, image_name, origin_url, masterpiece_url, artist) values({user_idx}, '{image_name}', '{origin_url}', '{masterpiece_url}', '{artist}')"
        return self.db.execute(sql)
    
    def emotion_filter(self, artist_type, style_type):
        sql = "select * from color_pallate"
        where = ""
        if artist_type or style_type:
            where += " where "
            where_value = ""
            
            if artist_type: 
                if len(where_value) > 0 : where_value += " and "
                where_value += "color in ("
                for index, val in enumerate(artist_type.split(',')):
                    if index == 0:
                        where_value += "'"+val+"'"
                    else:
                        where_value += ", '"+val+"'"
                where_value += ")"
                
            if style_type: 
                if len(where_value) > 0 : where_value += " and "
                where_value += "season in ("
                for index, val in enumerate(style_type.split(',')):
                    if index == 0:
                        where_value += "'"+val+"'"
                    else:
                        where_value += ", '"+val+"'"
                where_value += ")"
                
                
            where = where + where_value
            
        sql = sql + where + " limit 100;"
        print(sql)
        return self.db.select(sql)
