import sqlite3

import lib

conn = sqlite3.connect('database.db')

path = ''

with conn:
    con = conn.cursor()
    
    con.execute('DELETE FROM dirs')    
    con.execute('INSERT INTO dirs (dir_path,dir_hash) VALUES (?,?)',(path,lib.path_to_hash(path)))
    con.execute('DELETE FROM files')
    con.execute('DELETE FROM words')
    con.execute('DELETE FROM `index`')
    
