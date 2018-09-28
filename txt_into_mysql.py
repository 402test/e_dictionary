from pymysql import connect
import time
conn = connect(host = '127.0.0.1' ,user = 'test' ,password = '123456' ,\
    database = 'all_dict',charset = 'utf8',port = 3306)

cur = conn.cursor()
my_insert = 'insert into mydict(word , word_value) values(%s,%s)'



with open('all_dict.txt') as f:
    i = 1
    while True:
        i += 1
        data = f.readline()
        if not data:
            break
        spece = data.find(' ')
        word = data[:spece]
        explains = str(data[spece:]).strip()
        explains=explains.replace("'",'')
        word=word.replace("'",'')
        print(word,':  ',explains)
        cur.execute(my_insert,(word,explains))
        conn.commit()
conn.close()
cur.close()
