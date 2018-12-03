
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
        def select_market_product(self,market_name):
            try:
                with self.connection.cursor() as cursor:
                    sql = "SELECT * FROM recipe_proto.online_market_recipe WHERE online_market_name = '%s';" % market_name
                    print(sql)
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    self.get_column_name()
                #for obj in results:
                #    market_data.append(obj.get('MARKET_COINID'))
                return results

            finally:
                print("end query")


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

        



    def delete_data(self):
        try:
            with self.get_connection.connection.cursor() as cursor:
                sql="DELETE from recipe_proto.online_market_recipe WHERE %s;" % market_name
                cursor.execute(sql)

        finally:
            print("end query")
