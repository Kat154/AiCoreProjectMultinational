import database_utils
import pandas
import yaml

class DataCleaning:

	def clean_user_data(self,user_data_df):
		clean_df = user_data_df.dropna(axis = 1,how = 'all')
		# to drop column where all data is null values
		clean_df.fillna(0,inplace = True)
		# for remaining null values we replace them with zero
		

