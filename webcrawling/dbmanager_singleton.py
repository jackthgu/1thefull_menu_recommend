
import datetime
import pymysql.cursors

class db_manager():
    column_type =[]
    column_name=[]
    def __init__(self):
        self.connect_db()

    def __del__(self):
        self.connection.close()

    def connect_db(self):
        self.connection = pymysql.connect(host='104.155.225.112',
                                          user='root',
                                          password='0412',
                                          db='recipe_proto',
                                          cursorclass=pymysql.cursors.DictCursor)

    def select_market_product(self,market_name):
        try:
            with self.connection.cursor() as cursor:
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
            with self.connection.cursor() as cursor:
                for desc in cursor.description:
                    self.colname.append(desc[0])
                    self.coltype.append(desc[1])
        finally:
            return self.colname

    def delete_data(self):
        try:
            with self.connection.cursor() as cursor:
                sql="DELETE from recipe_proto.online_market_recipe WHERE %s;" % market_name
                cursor.execute(sql)

        finally:
            print("end query")
