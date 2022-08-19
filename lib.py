import hashlib
import time
import re

def split_text(text):
    return list(filter(lambda t: len(t)>0,list(set(re.split('[^\w\d\_]+',text.replace('_',' ').lower())))))

# -------------------------------------------------------------

def path_to_hash(path):
    '''
    преобразует путь в хеш по методу md5
    '''
    return hashlib.md5(path.encode('utf-8')).hexdigest()

# -------------------------------------------------------------

def time_now():
    '''
    текущее время в секундах
    '''
    return int(time.time())

# -------------------------------------------------------------

start_time = time_now()

def run_time():
    '''
    время в секундах от запуска программы
    '''
    return time_now() - start_time

# -------------------------------------------------------------