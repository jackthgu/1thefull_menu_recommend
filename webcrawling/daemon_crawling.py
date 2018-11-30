#!/usr/bin/env python
 
import sys, time
from daemon import Daemon
import datetime
import pymysql.cursors
import base64
import random
import datetime
import pdb
from market_fooding import fooding 
 
class MyDaemon(Daemon):
    def run(self):
        while True:
            time.sleep(1)
            
            

class db_manager():
    
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

    def 
    
 
if __name__ == "__main__":
    fooding = market_fooding()
    fooding.get_date()
    
    # daemon = MyDaemon('/tmp/daemon-example.pid')
    # if len(sys.argv) == 2:
    #     if 'start' == sys.argv[1]:
    #         daemon.start()
    #     elif 'stop' == sys.argv[1]:
    #         daemon.stop()
    #     elif 'restart' == sys.argv[1]:
    #         daemon.restart()
    #     else:
    #         print "Unknown command"
    #         sys.exit(2)
    #         sys.exit(0)
    # else:
    #     print "usage: %s start|stop|restart" % sys.argv[0]
    #     sys.exit(2)
