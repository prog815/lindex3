from flask import Flask, render_template, request
import sqlite3
import math

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/',methods=["GET"])
@app.route('/index',methods=["GET"])
def index():
    uslovie = ""
    page = 1
    if request.method == 'GET':
        poisk = request.args.get('poisk',"")
        if poisk is None:
            poisk = ""
        
        for u in poisk.split():
            uslovie += " AND ROWID IN (SELECT file_rowid FROM `index` WHERE word_rowid IN (SELECT ROWID FROM words WHERE word LIKE '" + u.lower() + "%'))"
        
        page = request.args.get('page')
        if page is None:
            page = 1
        else:
            page = int(page)
    
    print(uslovie)
    
    conn = get_db_connection()
    rows_cnt = conn.execute('SELECT count(*) rows_cnt FROM files WHERE 1' + uslovie).fetchone()
    conn.close()
    if rows_cnt is None:
        rows_cnt = 0
    else:
        rows_cnt = rows_cnt['rows_cnt']
    
    conn = get_db_connection()
    rows = conn.execute('SELECT file_path FROM files WHERE 1 ' + uslovie + ' ORDER BY file_ok_time DESC LIMIT ' + str((page-1)*10) + ',10').fetchall()
    conn.close()
    
    pages = [p for p in range(1,math.ceil(rows_cnt/10)+1)]  
    for p in pages:
        if abs(p-1) > 3 and  abs(p-page) > 3 and abs(p-pages[-1]) > 3 :
            pages[p-1] = None
            if abs(p-1) == 4 or  abs(p-page) == 4 or abs(p-pages[-1]) == 4:
                pages[p-1] = '.' 
    pages = list(filter(lambda x: not (x is None),pages))
    if len(pages) == 1:
        pages = []
    
    
    
    return render_template('index.html',rows=rows,poisk=poisk,page=page,pages=pages)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)