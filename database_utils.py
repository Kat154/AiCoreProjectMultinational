import yaml
# import db_creds
from sqlalchemy import create_engine
import psycopg2
import pandas as pd


class DatabaseConnector:
	
	def read_db_creds(self):
		with open('db_creds.yaml','r') as yaml_file_object:
			db_credentials_from_file = yaml.safe_load(yaml_file_object)
			# breakpoint()
		return db_credentials_from_file


	def init_db_engine(self):
		db_credentials_from_file = self.read_db_creds()
		RDS_HOST = db_credentials_from_file['RDS_HOST']
		RDS_PASSWORD = db_credentials_from_file['RDS_PASSWORD']
		RDS_USER = db_credentials_from_file['RDS_USER']
		RDS_DATABASE = db_credentials_from_file['RDS_DATABASE']
		RDS_PORT = db_credentials_from_file['RDS_PORT']
		DBAPI = 'psycopg2'
		RDS_DATABASE_TYPE = 'postgresql'
		engine = create_engine(f"{RDS_DATABASE_TYPE}+{DBAPI}://{RDS_USER}:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/{RDS_DATABASE}")
		return engine

	


	def upload_to_db(self,data,table_name):
		HOST = 'localhost'
		PASSWORD = 'sonia'
		USER = 'postgres'
		DATABASE = 'sales_data'
		DBAPI = 'psycopg2'
		PORT= 5432
		DATABASE_TYPE = 'postgresql'	
		
		engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
		with engine.connect() as connection:
			data.to_sql(table_name,con = connection, if_exists = 'replace',index_label='id')
			result = pd.read_sql_query(f'select * from {table_name}', engine)
			print(result)





