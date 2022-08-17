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
    page = 1
    if request.method == 'GET':
        poisk = request.args.get('poisk',"")
        if poisk is None:
            poisk = ""
            
        page = request.args.get('page')
        if page is None:
            page = 1
        else:
            page = int(page)
    
    return render_template('index.html',poisk=poisk,page=page)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)