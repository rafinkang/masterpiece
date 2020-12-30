from django.db import connection


class DbConn:
    def select(self, sql, args=None):
        """
        단일 행 select 실행 
        ex) data = (1, 'test') 
        execute(sql, data)
        """

        try:
            curs = connection.cursor()
            if args == None:
                result = curs.execute(sql)
            else:
                result = curs.execute(sql, args)
                
            if result:
                return self.dictfetchall(curs) # dictionary로 return
            
        except Exception as e:
            return e    
        
        finally:
            connection.commit()
            connection.close()
            
    def execute(self, sql, args=None):
        """
        단일 행 실행 
        ex) data = (1, 'test') 
        execute(sql, data)
        """
        try:
            curs = connection.cursor()
            if args == None:
                result = curs.execute(sql)
            else:
                result = curs.execute(sql, args)
                
            return result
            
        except Exception as e:
            return e    
        
        finally:
            connection.commit()
            connection.close()
            
    def executemany(self, sql, args=None):
        """
        다중 행 실행 
        ex) data = [[1, 'test'],[2, 'test2'],[3, 'test3'],[4, 'test4']]
        executemany(sql, data)
        """

        try:
            curs = connection.cursor()
            if args == None:
                result = curs.executemany(sql)
            else:
                result = curs.executemany(sql, args)
                
            return result
            
        except Exception as e:
            return e
            
        finally:
            connection.commit()
            connection.close()

    def dictfetchall(self, cursor):
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
