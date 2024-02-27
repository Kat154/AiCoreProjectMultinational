
import database_utils
import pandas as pd
import psycopg2
from sqlalchemy import create_engine,text
import tabula 
import requests
import boto3
import json 

class DataExtractor:

	def __init__(self):
		self.db_connector = database_utils.DatabaseConnector()
		self.engine = self.db_connector.init_db_engine()

	def read_rds_table(self,table_name):
		with self.engine.connect() as connection:
			user_data_df = pd.read_sql_table(table_name,self.engine)
			return user_data_df

	def list_db_tables(self):
		# engine = database_utils.DatabaseConnector.init_db_engine()
		with self.engine.connect() as connection:
			list_of_tables = pd.read_sql_query('select * from information_schema.tables',self.engine)['table_name']
			return list_of_tables
	

	def retrieve_pdf_data(self, link_to_pdf_file='https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'):
		df = tabula.read_pdf(link_to_pdf_file,pages = 'all')
		# now df here is actually list of dataframes which we need to merge into single dataframe before returning it.
		new_df = pd.concat(df)
		return new_df 

	def list_number_of_stores(self,number_of_stores_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores',header_details_dict =  {'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}):
		response = requests.get(url = number_of_stores_endpoint,headers = header_details_dict)
		if response.status_code == 200:
			return response.json()['number_stores']
		else:
			return 'no value found'

	def retrieve_stores_data(self,store_endpoint = f'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/',header_details_dict={'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}):
		total_stores = self.list_number_of_stores()
		total_stores_list = []
		for store_number in range(0,total_stores,1):
		# replace below line with above one when all work is done ~~sonia.
		# for store_number in range(1,20,1):
			response = requests.get(url = store_endpoint+str(store_number),headers = header_details_dict)
			our_dict = response.json()
			total_stores_list.append(our_dict)
		all_stores_df = pd.DataFrame.from_records(total_stores_list)
		all_stores_df_with_index_correction = all_stores_df.set_index(all_stores_df.columns[0])
		return all_stores_df_with_index_correction

	def extract_from_s3(self, s3_address = 's3://data-handling-public/products.csv'):
		s3 = boto3.client('s3')
		# s3.download_file('data-handling-public','s3://data-handling-public/products.csv','~/mnt/d/work/multinational/downloaded_product_details.csv')
		product_details_df = pd.read_csv(s3_address)
		product_details_df = product_details_df.set_index(product_details_df.columns[0])
		return product_details_df
		
	def extract_datetime_from_s3(self,s3_address = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'):
		s3 = boto3.client('s3')
		datetime_json_df = pd.read_json(s3_address)
		print(f'priting json: {datetime_json_df}')
		datetime_json_df = datetime_json_df.set_index(datetime_json_df.columns[0])
		return datetime_json_df

