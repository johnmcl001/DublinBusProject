import sqlalchemy as db
engine = db.create_engine('mysql+pymysql://niamh:comp47360jnnd@csi420-01-vm9.ucd.ie/website')
import pandas as pd
df=pd.read_csv('shapes.txt',delimiter=',', dtype=str)
try:
    df.to_sql('shapes', con=engine, index=False, if_exists='append')
except Exception as e:
    print(e)
