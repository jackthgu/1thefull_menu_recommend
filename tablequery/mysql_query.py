import datetime
import mysql.connector
from mysql.connector import errorcode
import pdb

def print_cursor(cnx):
    cursor=cnx
    row = cursor.fetchone()
    while row is not None:
        print(row)
        row = cursor.fetchone()

def init_session() :
    try:
        our_db = mysql.connector.connect(
                host ="35.243.97.54",
                user="root",
                password="asdf;lkj",
                database="food"
                )
        return our_db

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
    cursor.execute(query)
    print_cursor(cursor)


def get_db_all(cnx):
    cursor = cnx.cursor()
    query = "SELECT * FROM fooddata"
    cursor.execute("SELECT * FROM fooddata")
    print_cursor(cursor)

def get_column_name(cnx,tablename):
    cursor = cnx.cursor()
    query = "SELECT `COLUMN_NAME`  FROM `INFORMATION_SCHEMA`.`COLUMNS`  WHERE `TABLE_SCHEMA`='food'      AND `TABLE_NAME`='{0}'".format(tablename)
    cursor.execute(query)
    print_cursor(cursor)

def get_column_type(cnx,tablename,column):
    cursor = cnx.cursor()
    query = "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS  WHERE table_name = '{0}' AND COLUMN_NAME = '{1}'".format(tablename,column)
    cursor.execute(query)
    print_cursor(cursor)
    
aa = init_session()
get_column_type(aa,"fooddata","year")


