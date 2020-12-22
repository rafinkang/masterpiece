from masterpiece.models.DbConn import DbConn

class User():
    """
    User table
    """
    def __init__(self):
        self.db = DbConn()
        
    def select(self, sql, args=None):
        return self.db.select(sql, args)
    
    def execute(self, sql, args=None):
        return self.db.execute(sql, args)
    
    def executemany(self, sql, args=None):
        return self.db.executemany(sql, args)
    
    def insert_user(self, user_id, password, user_name, sex, birth, job, company):
        sql = f"""
        INSERT INTO user (user_id, password, user_name, sex, birth, job, company) 
        VALUES ('{user_id}', md5('{password}'), '{user_name}', {sex}, STR_TO_DATE('{birth}', '%Y-%m-%d'), '{job}', '{company}')
        """
        return self.db.execute(sql)
    
    def idcheck(self, user_id):
        sql = f"select * from user where user_id = '{user_id}'"
        return self.db.select(sql)
    
