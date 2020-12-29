from masterpiece.models.DbConn import DbConn

class ColorPallate():
    """
    ColorPallate table
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
        select * from color_pallate {limit_sql}
        """
        
        return self.db.select(sql)

    def emotion_filter(self, color_type = None, season_type = None, cw_type = None, cp_type = None, value_type = None, limit_start = 0, limit_end = 100):
        sql = "select * from color_pallate"
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