import pandas as pd
from sqlalchemy import create_engine


engine = create_engine('mysql://root:root@localhost/tat')

#conn = MySQLdb.connect(host="localhot",user="root",passwd="root",db="tat",charset="utf8")

# read
sql = "select * from tat"
#df = pd.read_sql(sql,conn,columns=['las_inlab','TAT'])
df = pd.read_sql_query(r'select * from tat',con=engine)
print df.describe()


# write
'''
cur = conn.cursor()
cur.execute("drop table if exists user")
cur.execute('create table user(id int,name varchar(20))' )
pd.io.sql.write_frame(df,"user",conn)
'''