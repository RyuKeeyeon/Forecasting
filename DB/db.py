import pandas as pd
import psycopg2
from sqlalchemy import create_engine, MetaData, Table, select, delete
from Crawl import cr as cr
from Crawl import extract_data as extract
#데이터베이스에 테이블만들기(sqlshell에서)
#CREATE TABLE energy_production (
#    id SERIAL PRIMARY KEY,
#    발전소명 VARCHAR(255),  -- 발전소명, 문자열 형식
#    시간 TIMESTAMP,         -- 시간, 타임스탬프 형식
#    생산량_kWh INTEGER,     -- 생산량(kWh), 정수 형식
#    PV_발전량 INTEGER,      -- PV 발전량, 정수 형식
#    ESS_충전량 INTEGER,     -- ESS 충전량, 정수 형식
#    ESS_방전량 INTEGER      -- ESS 방전량, 정수 형식
#);



# SQLAlchemy 엔진 생성: user:pw@host:port/dbname
db_url = 'postgresql://postgres:1234@localhost:5432/postgres'
engine = create_engine(db_url)

# SQLAlchemy MetaData 객체 생성 -> 테이블데이터 삭제,수정에 사용됨
metadata = MetaData()

# def excel_to_db (user_name,PW,host,db_name,port,table_name):
#     print('setting dbURL')
#     DB_URL = 'postgresql://'+user_name+':'+PW+'@'+host+':'+port+'/'+db_name
#     Engine = create_engine(DB_URL)
#     Table_name = table_name
#     print('read data')
#     crawled_Data = cr.gen(TargetDay,Farm)
#     # 데이터 db에 넣기
#     print('insert data')
#     crawled_Data.to_sql(Table_name, Engine, if_exists='replace', index=False)
#     engine.dispose()
#
#     return []



if __name__ == '__main__':
    # Start db_test.py
    TargetDay = '2023-03-03'
    Farm = 1
    table_name = 'energy_production_'+TargetDay

    Data = cr.gen(TargetDay, Farm)
    #Data = extract.extract_data_from_html(r'C:\Users\bosco\Documents\Forecasting\Crawl\Download\TimeData_2023-03-03.html')
    print("add data to table")

    Data.to_sql(table_name, engine, if_exists='replace', index=False)

    print('Data inserted')
    engine.dispose()
