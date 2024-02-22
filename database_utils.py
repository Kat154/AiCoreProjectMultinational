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

	def read_rds_table(self):
		




