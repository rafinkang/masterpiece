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
        VALUES ('{user_id}', '{password}', '{user_name}', {sex}, STR_TO_DATE('{birth}', '%Y-%m-%d'), '{job}', '{company}')
        """
        return self.db.execute(sql)
    
    def idcheck(self, user_id):
        sql = f"select * from user where user_id = '{user_id}'"
        return self.db.select(sql)


    def login_go(self,user_id,password):
        sql = f"select user_idx,user_id,user_name,sex,birth,job,company from user where user_id ='{user_id}' and password='{password}'"
        return self.db.select(sql)

    # def logout(self,sessionid):
    #     sql =f"delet from django_session where session_key='{sessionid}'"
    #     return self.db.execute(sql)


    def findpw(self,user_id,user_name):
        sql = f"select * from user where user_id = '{user_id}' and user_name='{user_name}'"   
        return self.db.select(sql)

    def modifypw_go(self,password,user_id,user_name):
        sql =f"update user set password = '{password}' where user_id='{user_id}' and user_name='{user_name}'"
        # print(sql)
        return self.db.execute(sql)