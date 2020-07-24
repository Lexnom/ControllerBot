import mysql.connector
import config

from mysql.connector import Error


def insert_bd(id_client):
    try:
        con = mysql.connector.connect(host=config.ip_db,
                                      database=config.name_bd,
                                      user=config.user_db,
                                      password=config.pas_db)
        if con.is_connected():
            cursor = con.cursor()
            query = "INSERT INTO clients_telegram(id_client_telegram) VALUES (%s)" % id_client
            cursor.execute(query)
            con.commit()
    except Error as e:
        print(e)

def select_id_client(id):
    try:
        con = mysql.connector.connect(host=config.ip_db,
                                      database=config.name_bd,
                                      user=config.user_db,
                                      password=config.pas_db)
        if con.is_connected():
            cursor = con.cursor()
            query = "SELECT id_client_telegram FROM clients_telegram WHERE id_client_telegram=%s" % id
            cursor.execute(query)
            result = cursor.fetchone()
            return result
    except Error as e:
        print(e)

def insert_token_bot(id_client,token, first_name, user_name):
    try:
        con = mysql.connector.connect(host=config.ip_db,
                                      database=config.name_bd,
                                      user=config.user_db,
                                      password=config.pas_db)
        if con.is_connected():
            cursor = con.cursor()
            query = "INSERT INTO client_bot(id_client, token_bot, first_name, user_name) VALUES (%s,'%s','%s','%s')" % (id_client,token, first_name, user_name)
            cursor.execute(query)
            con.commit()
    except Error as e:
        print(e)

def select_token_client(id_client,token):
    try:
        con = mysql.connector.connect(host=config.ip_db,
                                      database=config.name_bd,
                                      user=config.user_db,
                                      password=config.pas_db)
        if con.is_connected():
            cursor = con.cursor()
            query = "SELECT cb.token_bot FROM client_bot cb WHERE cb.id_client=%s and cb.token_bot='%s'" % (id_client, token)
            cursor.execute(query)
            result = cursor.fetchone()
            return result
    except Error as e:
        print(e)


def select_token_client_all(id_client):
    try:
        con = mysql.connector.connect(host=config.ip_db,
                                      database=config.name_bd,
                                      user=config.user_db,
                                      password=config.pas_db)
        if con.is_connected():
            cursor = con.cursor()
            query = "SELECT * FROM client_bot cb WHERE cb.id_client=%s" % (id_client)
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except Error as e:
        print(e)


def select_user_name_bot(token):
    try:
        con = mysql.connector.connect(host=config.ip_db,
                                      database=config.name_bd,
                                      user=config.user_db,
                                      password=config.pas_db)
        if con.is_connected():
            cursor = con.cursor()
            query = "SELECT cb.user_name FROM client_bot cb WHERE cb.token_bot='%s'" % token
            cursor.execute(query)
            result = cursor.fetchone()
            return result
    except Error as e:
        print(e)
