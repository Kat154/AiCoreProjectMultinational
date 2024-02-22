
import database_utils
import pandas as pd
import psycopg2
from sqlalchemy import create_engine,text
class DataExtractor:
	def read_rds_table(self,table_name):
		engine = self.init_db_engine()
		with engine.connect() as connection:
			user_data_df = pd.read_sql_table(table_name,engine)
			return user_data_df

	def list_db_tables(self):
		engine = self.init_db_engine()
		with engine.connect() as connection:
			list_of_tables = pd.read_sql_query('select * from information_schema.tables',engine)['table_name']
			return list_of_tables
	

	def upload_to_db(self,data,table_name):
		HOST = 'localhost'
		PASSWORD = 'sonia'
		USER = 'postgres'
		DATABASE = 'sales_data'
		DBAPI = 'psycopg2'
		PORT: 5432
		DATABASE_TYPE = 'postgresql'	
		
		engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
		with engine.connect() as connection:
			data.to_sql(table_name,con = connection, if_exists = 'replace')
			