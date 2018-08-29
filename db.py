import sqlite3
import os

abs_path = os.getcwd()


class DB_Connector():
    def __init__(self):
        self.con = sqlite3.connect(os.path.join(abs_path, 'db', 'mds_env.db'))
        self.curse = self.con.cursor()
    def init(self):
        self.curse.execute("""
        create table if not exists mds_env_survey (
        id INT auto_increment PRIMARY KEY NOT NULL ,
        name CHAR(50),
        date CHAR(50),
        username CHAR(50),
        userphone CHAR(50),)
        """)


    def close(self):
        self.curse.close()
        self.con.close()
