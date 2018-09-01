import sqlite3
import os

abs_path = os.getcwd()


class DB_Connector():
    def __init__(self):
        self.con = sqlite3.connect(os.path.join(abs_path, 'db', 'mds_env.db'))
        self.curse = self.con.cursor()
    def init_envsurvey(self):
        self.curse.execute("""
        create table if not exists mds_env_survey (
        name CHAR(50),
        date date,
        companyname CHAR(50),
        username CHAR(50),
        userphone CHAR(50),
        userepl CHAR(50),
        companylocation CHAR(50),
        latlng CHAR(50),
        huanping CHAR(50),
        reportbook CHAR(50),
        reporttable CHAR(50),
        dengjitable CHAR(50),
        xianchangxiangfu CHAR(50),
        xianchangxiangfu_desc TEXT,
        yanshou CHAR(50),
        yanshou_desc TEXT,
        shengchangongyi TEXT,
        yuanliang TEXT,
        chengping TEXT,
        weixianping CHAR(50),
        wuranqingkuang CHAR(50),
        huanjingjijinyuyan CHAR(50),
        qingjiebianhao CHAR(50),
        wushuiqingkuang CHAR(50),
        dunwei FLOAT(50),
        wushuichuligongyi CHAR(50),
        feiqiqingkuang CHAR(50),
        fengliang FLOAT(50),
        feiqichuligongyi CHAR(50),
        wuni FLOAT(50),
        youqi FLOAT(50),
        jinshu FLOAT(50),
        fenchen FLOAT(50),
        feiqiwutianxiemingcheng FLOAT(50),
        qitashuoming TEXT,
        zaoyinqingkuang CHAR(50),
        pianjian FLOAT(50),
        PAC FLOAT(50),
        PAM FLOAT(50),
        tansuangai FLOAT(50),
        chulinji FLOAT(50),
        nalixianggaizao CHAR(50),
        zhushi TEXT,
        pic TEXT
        )
        """)
    def drop(self):
        self.curse.execute("drop table if exists mds_env_survey")
    def close(self):
        self.curse.close()
        self.con.close()

if __name__ == '__main__':
    db = DB_Connector()
    db.curse.execute("select name,date from mds_env_survey where name in ('老王')")
    print(db.curse.fetchall())
    # db.drop()
    # db.init_envsurvey()