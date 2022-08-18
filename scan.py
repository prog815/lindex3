import os
import sqlite3
import random
import re

import lib

# ------------------------------------------------------------------

conn = sqlite3.connect('database.db')

# ------------------------------------------------------------------

with conn:
    con = conn.cursor()
    
    # отбираем 1000 каталогов которые не сканировали последние сутки
    rows = con.execute('SELECT dir_path,dir_hash FROM dirs WHERE dir_scan_time < ? ORDER BY dir_scan_time DESC LIMIT 1000',(lib.time_now()-24*60*60,)).fetchall()
    
    # перемешиваем каталоги перед обработкой для исключения белых пятен
    random.shuffle(rows)
    
    # бежим по выборке из каталогов
    for path,hash in rows:
        # прерываем, если больше минуты работаем
        if lib.run_time() > 60:
            break
        
        try:
            # бежим по элементам текущего каталога
            with os.scandir('static/files/' + path) as it:
                
                # прерываем, если больше минуты скрипт работает
                if lib.run_time() > 60:
                    break
                
                for entry in it:
                    p = entry.path[13:].replace('\\','/')
                    h = lib.path_to_hash(p)
                    t = lib.time_now()
                    
                    if entry.is_dir():
                        try:
                            # добавляем новый каталог в базу
                            con.execute('INSERT INTO dirs (dir_path,dir_hash) VALUES (?,?)',(p,h))
                        except:
                            pass
                    elif entry.is_file():
                        
                        try:
                            # добавляем новый файл и берем его номер
                            file_rowid = con.execute('INSERT INTO files (file_path,file_hash,file_ok_time) VALUES (?,?,?)',(p,h,t)).lastrowid
                            
                            # бежим по словам из пути к файлу
                            for w in set(re.split('[^\w\d\_]+',p.replace('_',' ').lower())):
                                if len(w) > 0:
                                    try:
                                        # добавляем новое слово и берем его номер
                                        word_rowid = con.execute('INSERT INTO words (word) VALUES (?)',(w,)).lastrowid
                                    except:
                                        # слово уже есть. Берем его номер
                                        word_rowid = con.execute('SELECT ROWID FROM words WHERE word = ?',(w,)).fetchone()[0]
                                    
                                    try:
                                        # сохраняем в индексе пару файл-слово
                                        con.execute('INSERT INTO `index` (file_rowid,word_rowid) VALUES (?,?)',(file_rowid,word_rowid))
                                    except:
                                        pass
                        except:
                            # файл уже есть в базе. Обновляем его время доступности
                            con.execute('UPDATE files SET file_ok_time=? WHERE file_hash=?',(t,h))
            
            # удачно сканировали папку
            con.execute('UPDATE dirs SET dir_scan_time=?, dir_ok_time=? WHERE dir_hash=?',(lib.time_now(),lib.time_now(),hash))
            
        except:
            # неудачно сканировали папку
            con.execute('UPDATE dirs SET dir_scan_time=? WHERE dir_hash=?',(lib.time_now(),hash))
        