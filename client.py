from flask import Flask, render_template, request, redirect, url_for
# import threading
# from PyQt5.QtCore import QUrl
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtWebEngineWidgets import QWebEngineView
import sqlite3
import os, time
import xlwt, zipfile, xlrd

abs_path = os.getcwd()
app = Flask(__name__)
URL, PORT = '0.0.0.0',6005
if not os.path.exists(os.path.join(os.getcwd(),'static','download_all')):
    os.mkdir(os.path.join(os.getcwd(),'static','download_all'))
if not os.path.exists(os.path.join(os.getcwd(),'static','download_cur')):
    os.mkdir(os.path.join(os.getcwd(),'static','download_cur'))
COLS = """name,date,companyname,username,userphone,userepl,companylocation,latlng,huanping,reportbook,reporttable,dengjitable,xianchangxiangfu,xianchangxiangfu_desc,yanshou,yanshou_desc,shengchangongyi,yuanliang,chengping,weixianping,wuranqingkuang,huanjingjijinyuyan,qingjiebianhao,wushuiqingkuang,dunwei,wushuichuligongyi,feiqiqingkuang,fengliang,feiqichuligongyi,wuni,youqi,jinshu,fenchen,feiqiwutianxiemingcheng,qitashuoming,zaoyinqingkuang,pianjian,PAC,PAM,tansuangai,chulinji,nalixianggaizao,zhushi,pic"""
table_cols = """name,date,companyname,username,userphone,userepl,companylocation,latlng,huanping,reportbook,reporttable,dengjitable,xianchangxiangfu,yanshou,weixianping,wuranqingkuang,huanjingjijinyuyan,qingjiebianhao,wushuiqingkuang,dunwei,wushuichuligongyi,feiqiqingkuang,fengliang,feiqichuligongyi,wuni,youqi,jinshu,fenchen,feiqiwutianxiemingcheng,zaoyinqingkuang,pianjian,PAC,PAM,tansuangai,chulinji"""
cols_table = """业务人员,日期,企业名称,业主姓名,业主电话,业主职务,企业地址,经纬度,环评情况,报告书,报告表,登记表,现场相符,验收情况,危险品,重点污染,环境应急预案,清洁生产,污水,吨位,污水处理,废气,风量,废气处理,污泥,油漆,金属,粉尘,废弃物,噪音,片碱,PAC,PAM,碳酸钙,除磷剂"""
all_cols_table = """业务人员,日期,企业名称,业主姓名,业主电话,业主职务,企业地址,经纬度,环评情况,报告书,报告表,登记表,现场相符,不否说明,验收情况,为什么没验收,生产工艺,原辅料,成品,危险品,重点污染,环境应急预案,清洁生产,污水,吨位,污水处理,废气,风量,废气处理,污泥,油漆,金属,粉尘,废弃物,其他物质说明,噪音,片碱,PAC,PAM,碳酸钙,除磷剂,哪里需要改造,注"""
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


def get_sel(cols, db):
    sel = [[i] for i in cols]
    for index in range(len(cols)):
        col = col_dict[cols[index]]
        db.curse.execute("""select %s from mds_env_survey group by %s""" % (col, col))
        dt = db.curse.fetchall()
        sel[index].append([i[0] for i in dt])
    return sel


def download_all():
    global all_cols_table
    download(all_cols_table, '*', '', 'download_all')


def download(all_cols_table, needed, where, dirname):
    db = DB_Connector()
    sql = "select %s from mds_env_survey " % needed + where
    print(sql)
    db.curse.execute(sql)
    data = db.curse.fetchall()
    dt = [i[1:-1] for i in data]
    pics = {i[-1]: i[3] for i in data if i[-1] and i[3]}
    cols = all_cols_table.split(',')
    dt = [cols] + dt
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    for i in range(len(dt)):
        for j in range(len(dt[i])):
            sheet.write(i, j, dt[i][j])
    wbk.save(os.path.join(os.getcwd(), 'static', dirname, 'all.xls'))
    print('saved successful!', os.path.join(os.getcwd(), 'static', dirname, 'all.xls'))
    for k, v in pics.items():
        if not os.path.exists(os.path.join(os.getcwd(), 'static', dirname, v)):
            os.mkdir(os.path.join(os.getcwd(), 'static', dirname, v))
        for pic in k.split(','):
            os.system("cp static/pics/%s static/%s/%s/%s" % (pic, dirname, v, pic))
    startdir = os.path.join(os.getcwd(), 'static', dirname)
    file_news = os.path.join(os.getcwd(), 'static', dirname) + '.zip'
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
    z.close()
    os.system("rm -rf static/%s/*" % dirname)


@app.route('/')
def home():
    db = DB_Connector()
    db.curse.execute("select date,count(*) from mds_env_survey group by date")
    fet = db.curse.fetchall()
    db.close()
    date = [i[0].replace('-', '/') for i in fet]
    data = [i[1] for i in fet]
    return render_template('home.html', data=data, date=date)


@app.route('/tables-data', methods=['GET', 'POST'])
def tables_data():
    global sel_cols, cols_table, table_cols

    db = DB_Connector()
    cols = cols_table.split(',')
    if request.method == 'GET':
        msg = request.args.get('msg')
        warn = request.args.get('warn')
        sel = get_sel(cols[:5], db)
        db.curse.execute("""select %s from mds_env_survey""" % ("ID," + ','.join(table_cols.split(',')[:5])))
        lines = db.curse.fetchall()
        lines = [list(i) for i in lines]
        db.close()
        return render_template('tables-data.html', tb={'cols': cols[:5], 'lines': lines, 'sel': sel}, sel_cols=sel_cols,
                               message=msg, warn=warn)
    elif request.method == "POST":
        where = []
        for k, v in request.form.items():
            if k == "cols":
                post_cols = request.form.get("cols")
                post_cols = post_cols.split('-')
                if not post_cols:
                    return redirect(url_for('tables_data'))
            else:
                if v:
                    ll = '(' + ','.join(map(lambda x: '"' + x + '"', v.split('-'))) + ')'
                    where.append("%s in %s" % (col_dict[k], ll))
        while '' in post_cols:
            post_cols.remove('')
        if not post_cols:
            warn = "请选择需要查询的字段"
            return redirect(url_for('tables_data', warn=warn))
        sel = get_sel(post_cols, db)
        needed = [col_dict[i] for i in post_cols]
        db = DB_Connector()
        where = " where %s" % " and ".join(where) if where else ""
        sql = """select %s from mds_env_survey""" % ("ID," + ','.join(needed)) + where
        print(sql)
        db.curse.execute(sql)
        lines_2 = db.curse.fetchall()
        lines_2 = [list(i) for i in lines_2]
        db.close()
        download(','.join(post_cols), "ID," + ','.join(needed) + ",pic", where, "download_cur")
        return render_template('tables-data.html', tb={'cols': post_cols, 'lines': lines_2, 'sel': sel},
                               sel_cols=sel_cols)

def form_advanced_submit():
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
            f.save(os.path.join(abs_path, 'static', 'pics', fname))
            msg += "\n图片上传成功！%s" % f.filename
    pic = ','.join(pic)
    zhushi = request.form.get('zhushi')
    db = DB_Connector()
    global COLS
    insert_sql = "insert into mds_env_survey(%s) values(" % COLS + "'%s'," * 43 + "'%s')"
    args = tuple(i for i in
                 map(str, [name, date, companyname, userphone, username, userepl, companylocation, latlng, huanping,
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
    download_all()
    return render_template('forms-advanced.html', message=msg)

@app.route('/forms-advanced', methods=['GET', 'POST'])
def forms_advanced():
    if request.method == 'GET':
        return render_template('forms-advanced.html')
    elif request.method == 'POST':
        ID = request.form.get('id')
        if ID:
            db = DB_Connector()
            if request.form.get('op')=="0":
                # 查看详情
                db.curse.execute("select * from mds_env_survey where ID='%s'"%ID)
                data = list(db.curse.fetchone())
                mutisel = data[-3].split(',')
                pics = data[-1].split(',') if data[-1] else []
                gaizao = [1 if i in mutisel else 0 for i in ['环评', '预案', '清洁生产', '污水', '废气', '噪音']]
                return render_template("forms-basic.html",data=data,gaizao=gaizao,pics=pics)
            elif request.form.get('op')=="1":
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
                        f.save(os.path.join(abs_path, 'static', 'pics', fname))
                        msg += "\n图片上传成功！%s" % f.filename
                zhushi = request.form.get('zhushi')
                db = DB_Connector()
                db.curse.execute("select pic from mds_env_survey where ID='%s'"%ID)
                dt_pic = db.curse.fetchone()[0]
                cur_pic = dt_pic.split(',') if dt_pic else []
                print(cur_pic,request.form.get('del_pic').split('-'))
                for del_pic in request.form.get('del_pic').split('-'):
                    if del_pic in cur_pic:
                        cur_pic.remove(del_pic)
                pic = ','.join(pic+cur_pic)
                global COLS
                args = tuple(i for i in
                             map(str, [name, date, companyname, userphone, username, userepl, companylocation, latlng,
                                       huanping,
                                       reportbook, reporttable, dengjitable, xianchangxiangfu, xianchangxiangfu_desc,
                                       yanshou,
                                       yanshou_desc, shengchangongyi, yuanliang, chengping, weixianping, wuranqingkuang,
                                       huanjingjijinyuyan, qingjiebianhao, wushuiqingkuang, dunwei, wushuichuligongyi,
                                       feiqiqingkuang, fengliang, feiqichuligongyi, wuni, youqi, jinshu, fenchen,
                                       feiqiwutianxiemingcheng, qitashuoming, zaoyinqingkuang, pianjian, PAC, PAM,
                                       tansuangai,
                                       chulinji, nalixianggaizao, zhushi, pic]))
                COLS_list = COLS.split(',')
                update_sql = "update mds_env_survey set " +\
                             ','.join(["%s='%s'"%(COLS_list[i],args[i]) for i in range(len(COLS_list))]) +" where ID='%s'"%ID
                print(update_sql)
                db.curse.execute(update_sql)
                db.con.commit()
                db.close()
                msg += "\n表单提交成功！"
                download_all()
                return redirect(url_for('tables_data',msg=msg))
        else:
            return form_advanced_submit()


@app.route('/delete', methods=['post'])
def delete():
    ID = request.form.get('id')
    db = DB_Connector()
    db.curse.execute("delete from mds_env_survey where ID='%s'"%str(ID))
    db.con.commit()
    db.close()
    download_all()
    return "删除成功！"


@app.route('/upload', methods=['post'])
def upload():
    ff = request.form.get('file-input')
    if ff and (ff.endswith('xls') or ff.endswith('xlsx')):
        print('upload excel file')
        workbook = xlrd.open_workbook(ff)
        for sheetname in workbook.sheet_names():
            sheet = workbook.sheet_by_name(sheetname)
            col_names = [sheet.cell(0, col).value for col in range(sheet.ncols)]
            if col_names != all_cols_table.split(','):
                print('sheet format is wrong!')
                continue
            db = DB_Connector()
            for row in range(1, sheet.nrows):
                global COLS
                sql = """ insert into mds_env_survey(%s) values""" % ','.join(COLS.split(',')[:-1])
                values = tuple(i for i in map(str, [sheet.cell(row, col).value for col in range(sheet.ncols)]))
                sql += str(values)
                db.curse.execute(sql)
                db.con.commit()
            db.close()
        download_all()
        return redirect(url_for('tables_data', msg="表格数据上传成功"))
    elif ff and (ff.endswith('doc') or ff.endswith('docx')):
        return redirect(url_for('tables_data', warn="暂不支持word文档上传"))
    else:
        return wrong_tabledata()


def wrong_tabledata():
    warn = "文件格式错误或者未选择文件！"
    global sel_cols, cols_table, table_cols
    db = DB_Connector()
    cols = cols_table.split(',')
    sel = get_sel(cols[:5], db)
    db.curse.execute("""select %s from mds_env_survey""" % (','.join(table_cols.split(',')[:5])))
    lines = db.curse.fetchall()
    lines = [list(i) for i in lines]
    db.close()
    return render_template('tables-data.html', tb={'cols': cols[:5], 'lines': lines, 'sel': sel},
                           sel_cols=sel_cols, warn=warn)


if __name__ == '__main__':
    app.run(URL,PORT)
    # thread = threading.Thread(target=app.run, args=[URL, PORT])
    # thread.daemon = True
    # thread.start()
    # qt_app = QApplication([])
    # w = QWebEngineView()
    # w.setWindowTitle('My Browser')
    #
    # w.load(QUrl('http://%s:%s' % (URL, PORT)))
    # # w.load(QUrl('http://www.baidu.com'))
    # w.showMaximized()
    # w.show()
    # qt_app.exec_()
