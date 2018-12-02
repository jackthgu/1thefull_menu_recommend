
import datetime
import pymysql.cursors

class db_manager(object):
    class __db_manager:
        def __init__(self):
            self.connection = pymysql.connect(host='104.155.225.112',
                                              user='root',
                                              password='0412',
                                              db='recipe_proto',
                                              cursorclass=pymysql.cursors.DictCursor)
        def __get_connection(self):
            return self.connection

    instance = None

    def __new__(cls):
        if not db_manager.instance:
            db_manager.instance = db_manager.__db_manager()
            return db_manager.instance
    def __getattr__(self,name):
        return getattr(self.instance,name)
    def __setattr__(self,name):
        return setattr(self.instance,name)

    def get_connection(self):
        return db_manager.instance.__get_connection()

        
    def select_market_product(self,market_name):
        try:
            with self.get_connection.connection.cursor() as cursor:
                sql = "SELECT * FROM recipe_proto.online_market_recipe WHERE %s;" % market_name
                cursor.execute(sql)
                results = cursor.fetchall()
                for obj in results:
                    self.market_ids.append(obj.get('MARKET_COINID'))
                print(self.market_ids)

        finally:
            print("end query")

    def get_column_name(self):
        try:
            with self.get_connection.connection.cursor() as cursor:
                for desc in cursor.description:
                    self.colname.append(desc[0])
                    self.coltype.append(desc[1])
        finally:
            return self.colname

    def delete_data(self):
        try:
            with self.get_connection.connection.cursor() as cursor:
                sql="DELETE from recipe_proto.online_market_recipe WHERE %s;" % market_name
                cursor.execute(sql)

        finally:
            print("end query")
