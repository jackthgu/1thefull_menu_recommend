import datetime
import mysql.connector
from mysql.connector import errorcode
import pdb


def init_session() :
    try:
        our_db = mysql.connector.connect(
                host ="35.243.97.54",
                user="root",
                password="asdf;lkj",
                database="food"
                )

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print ("Somthing is wrong with your ser name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else :
            print(err)
    else:
        our_db.close()


def single_select(cnx,sel,frm):
    cursor = cnx.cursor()
    query = "SELECT {0} FROM {1} ".format(sel,frm)
    print(query)


def get_db_all(cnx):
    cursor = cnx.cursor()
    query = "SELECT * FROM fooddata"
    iterator = cursor.execute(query, params=None, multi=True)
    pdb.set_trace()

    
aa = init_session()
get_db_all(aa)
