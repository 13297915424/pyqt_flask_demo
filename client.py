from flask import Flask, render_template, request, redirect, url_for
import threading
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sqlite3
import os, time
import datetime
abs_path = os.getcwd()
app = Flask(__name__)
URL, PORT = 'localhost', 1518
cols = """name,date,companyname,username,userphone,userepl,companylocation,latlng,huanping,reportbook,reporttable,dengjitable,xianchangxiangfu,xianchangxiangfu_desc,yanshou,yanshou_desc,shengchangongyi,yuanliang,chengping,weixianping,wuranqingkuang,huanjingjijinyuyan,qingjiebianhao,wushuiqingkuang,dunwei,wushuichuligongyi,feiqiqingkuang,fengliang,feiqichuligongyi,wuni,youqi,jinshu,fenchen,feiqiwutianxiemingcheng,qitashuoming,zaoyinqingkuang,pianjian,PAC,PAM,tansuangai,chulinji,nalixianggaizao,zhushi,pic"""
table_cols = """name,date,companyname,username,userphone,userepl,companylocation,latlng,huanping,reportbook,reporttable,dengjitable,xianchangxiangfu,yanshou,weixianping,wuranqingkuang,huanjingjijinyuyan,qingjiebianhao,wushuiqingkuang,dunwei,wushuichuligongyi,feiqiqingkuang,fengliang,feiqichuligongyi,wuni,youqi,jinshu,fenchen,feiqiwutianxiemingcheng,zaoyinqingkuang,pianjian,PAC,PAM,tansuangai,chulinji"""
cols_table = """业务人员,日期,企业名称,业主姓名,业主电话,业主职务,企业地址,经纬度,环评情况,报告书,报告表,登记表,现场相符,验收情况,危险品,重点污染,环境应急预案,清洁生产,污水,吨位,污水处理,废气,风量,废气处理,污泥,油漆,金属,粉尘,废弃物,噪音,片碱,PAC,PAM,碳酸钙,除磷剂"""
all_cols_table = """业务人员,日期,企业名称,业主电话,业主姓名,业主职务,企业地址,经纬度,环评情况,报告书,报告表,登记表,现场相符,不否说明,验收情况,验收,生产工艺,原辅料,成品,危险品,重点污染,环境应急预案,清洁生产,污水,吨位,污水处理,废气,风量,废气处理,固废情况,污泥,油漆,金属,粉尘,废弃物,其他,噪音,片碱,PAC,PAM,碳酸钙,除磷剂,改造,注"""
cols_list = cols_table.split(',')
table_cols_list = table_cols.split(',')
col_dict = {cols_list[i]: table_cols_list[i] for i in range(len(table_cols_list))}
sel_cols = [['登记信息', '业务人员', '日期'],
            ['企业信息', '企业名称', '业主电话', '业主姓名', '业主职务', '企业地址', '经纬度'],
            ['环评情况', '环评情况', '报告书', '报告表', '登记表', '现场相符'],
            ['验收情况', '验收情况'],
            ['生产工艺', '危险品', '重点污染', '环境应急预案', '清洁生产'],
            ['污水情况', '污水', '吨位', '污水处理'],
            ['废气情况', '废气', '风量', '废气处理'],
            ['固废情况', '污泥', '油漆', '金属', '粉尘', '废弃物'],
            ['噪音情况', '噪音'],
            ['药剂使用情况', '片碱', 'PAC', 'PAM', '碳酸钙', '除磷剂']]


class DB_Connector():
    def __init__(self):
        self.con = sqlite3.connect(os.path.join(abs_path, 'db', 'mds_env.db'))
        self.curse = self.con.cursor()

    def init_envsurvey(self):
        self.curse.execute("""
        create table if not exists mds_env_survey (
        id INT auto_increment PRIMARY KEY NOT NULL ,
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
        zhushi TEXT
        )
        """)

    def close(self):
        self.curse.close()
        self.con.close()


@app.route('/')
def home():
    db = DB_Connector()
    db.curse.execute("select date,count(*) from mds_env_survey group by date")
    fet = db.curse.fetchall()
    db.close()
    date = [i[0].replace('-','/') for i in fet]
    data = [i[1] for i in fet]
    return render_template('home.html', data=data,date=date)

def get_sel(cols,db):
    sel = [[i] for i in cols]
    for  index in range(len(cols)):
        col = col_dict[cols[index]]
        db.curse.execute("""select %s from mds_env_survey group by %s""" % (col, col))
        dt = db.curse.fetchall()
        sel[index].append([i[0] for i in dt])
    return sel

@app.route('/tables-data', methods=['GET', 'POST'])
def tables_data():
    global sel_cols, cols_table, table_cols
    db = DB_Connector()
    cols = cols_table.split(',')

    if request.method == 'GET':
        sel = get_sel(cols[:5],db)
        db.curse.execute("""select %s from mds_env_survey""" % (','.join(table_cols.split(',')[:5])))
        lines = db.curse.fetchall()
        lines = [list(i) for i in lines]
        db.close()
        return render_template('tables-data.html', tb={'cols': cols[:5], 'lines': lines,'sel':sel}, sel_cols=sel_cols)
    elif request.method == "POST":
        # pass
        # return redirect(url_for('tables_data'))
        where = []
        for k,v in request.form.items():
            if k =="cols":
                post_cols = request.form.get("cols")
                post_cols = post_cols.split('-')
                if not post_cols:
                    return redirect(url_for('tables_data'))
            else:
                if v:
                    ll = '('+','.join(map(lambda x:'"'+x+'"',v.split('-')))+')'
                    where.append("%s in %s"%(col_dict[k],ll))
        sel = get_sel(post_cols, db)
        needed = [col_dict[i] for i in post_cols]
        db = DB_Connector()
        print("""select %s from mds_env_survey""" % (','.join(needed))+" where %s"%" and ".join(where))
        sql = """select %s from mds_env_survey""" % (','.join(needed))+" where %s"%" and ".join(where) if where else \
            """select %s from mds_env_survey""" % (','.join(needed))
        db.curse.execute(sql)
        lines_2 = db.curse.fetchall()
        lines_2 = [list(i) for i in lines_2]
        db.close()
        return render_template('tables-data.html', tb={'cols': post_cols, 'lines': lines_2,'sel':sel}, sel_cols=sel_cols)


@app.route('/forms-basic')
def forms_basic():
    return render_template('forms-basic.html')


@app.route('/forms-advanced', methods=['GET', 'POST'])
def forms_advanced():
    if request.method == 'GET':
        return render_template('forms-advanced.html')
    elif request.method == 'POST':
        msg = ''
        name = request.form.get('name')
        date = request.form.get('date')
        companyname = request.form.get('companyname')
        username = request.form.get('username')
        userphone = request.form.get('userphone')
        userepl = request.form.get('userepl')
        companylocation = request.form.get('companylocation')
        latlng = request.form.get('latlng')
        huanping = request.form.get('huanping')
        reportbook = request.form.get('reportbook')
        reporttable = request.form.get('reporttable')
        dengjitable = request.form.get('dengjitable')
        xianchangxiangfu = request.form.get('xianchangxiangfu')
        xianchangxiangfu_desc = request.form.get('xianchangxiangfu_desc')
        yanshou = request.form.get('yanshou')
        yanshou_desc = request.form.get('yanshou_desc')
        shengchangongyi = request.form.get('shengchangongyi')
        yuanliang = request.form.get('yuanliang')
        chengping = request.form.get('chengping')
        weixianping = request.form.get('weixianping')
        wuranqingkuang = request.form.get('wuranqingkuang')
        huanjingjijinyuyan = request.form.get('huanjingjijinyuyan')
        qingjiebianhao = request.form.get('qingjiebianhao')
        wushuiqingkuang = request.form.get('wushuiqingkuang')
        dunwei = request.form.get('dunwei')
        wushuichuligongyi = request.form.get('wushuichuligongyi')
        feiqiqingkuang = request.form.get('feiqiqingkuang')
        fengliang = request.form.get('fengliang')
        feiqichuligongyi = request.form.get('feiqichuligongyi')
        wuni = request.form.get('wuni')
        youqi = request.form.get('youqi')
        jinshu = request.form.get('jinshu')
        fenchen = request.form.get('fenchen')
        feiqiwutianxiemingcheng = request.form.get('feiqiwutianxiemingcheng')
        qitashuoming = request.form.get('qitashuoming')
        zaoyinqingkuang = request.form.get('zaoyinqingkuang')
        pianjian = request.form.get('pianjian')
        PAC = request.form.get('PAC')
        PAM = request.form.get('PAM')
        tansuangai = request.form.get('tansuangai')
        chulinji = request.form.get('chulinji')
        nalixianggaizao = [request.form.get('checkbox%s' % (str(i))) for i in range(1, 7)]
        while None in nalixianggaizao:
            nalixianggaizao.remove(None)
        nalixianggaizao = ','.join(nalixianggaizao)
        pic = []
        for f in request.files.getlist('file-multiple-input'):
            if f:
                fname = companyname + str(time.time()) + '.' + f.filename.split('.')[-1]
                pic.append(fname)
                f.save(os.path.join(abs_path, 'db', 'pics', fname))
                msg += "\n图片上传成功！%s" % f.filename
        pic = ','.join(pic)
        zhushi = request.form.get('zhushi')
        db = DB_Connector()
        insert_sql = "insert into mds_env_survey(%s) values(" % cols + "'%s'," * 43 + "'%s')"
        args = tuple(i for i in
                     map(str, [name, date, companyname, username, userphone, userepl, companylocation, latlng, huanping,
                               reportbook, reporttable, dengjitable, xianchangxiangfu, xianchangxiangfu_desc, yanshou,
                               yanshou_desc, shengchangongyi, yuanliang, chengping, weixianping, wuranqingkuang,
                               huanjingjijinyuyan, qingjiebianhao, wushuiqingkuang, dunwei, wushuichuligongyi,
                               feiqiqingkuang, fengliang, feiqichuligongyi, wuni, youqi, jinshu, fenchen,
                               feiqiwutianxiemingcheng, qitashuoming, zaoyinqingkuang, pianjian, PAC, PAM, tansuangai,
                               chulinji, nalixianggaizao, zhushi, pic]))
        db.curse.execute(insert_sql % args)
        db.con.commit()
        db.close()
        msg += "\n表单提交成功！"
        return render_template('forms-advanced.html', message=msg)


@app.route('/page-login')
def page_login():
    return render_template('page-login.html')


@app.route('/page-register')
def page_register():
    return render_template('page-register.html')


@app.route('/pages-forget.html')
def pages_forget():
    return render_template('pages-forget.html')


# {{ url_for('page_register') }}
if __name__ == '__main__':
    thread = threading.Thread(target=app.run, args=[URL, PORT])
    thread.daemon = True
    thread.start()
    qt_app = QApplication([])
    w = QWebEngineView()
    w.setWindowTitle('My Browser')

    w.load(QUrl('http://%s:%s' % (URL, PORT)))
    w.showMaximized()
    w.show()
    qt_app.exec_()
