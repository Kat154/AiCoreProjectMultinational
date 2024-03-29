import database_utils
import pandas as pd
import yaml
import numpy as np

class DataCleaning:
# -----------------------------user data----------------------------------------
	def clean_user_data(self,user_data_df):
		clean_df = user_data_df.dropna(axis = 1,how = 'all')
		clean_df = clean_df.set_index(clean_df.columns[0])
		# to drop column where all data is null values
		clean_df = self._clean_first_name(clean_df)
		clean_df = self._clean_last_name(clean_df)
		clean_df = self._clean_date_of_birth(clean_df)
		clean_df = self._clean_company(clean_df)
		clean_df = self._clean_email_address(clean_df)
		clean_df = self._clean_address(clean_df)
		clean_df = self._clean_country(clean_df)
		clean_df = self._clean_country_code(clean_df)
		clean_df = self._clean_phone_number(clean_df)
		clean_df = self._clean_join_date(clean_df)
		clean_df = self._clean_user_uuid(clean_df)
		return clean_df

	def _clean_first_name(self,clean_df):
		clean_df['first_name'] = clean_df['first_name'].apply(self._change_name)
		return clean_df

	def _clean_last_name(self,clean_df):
		clean_df['last_name'] = clean_df['last_name'].apply(self._change_name)
		return clean_df

	def _change_name(self,value):
		for letter in str(value):
			if letter in '0123456789@#$%^&*()_+':
				return np.nan 
		return value 

	def _clean_date_of_birth(self,clean_df):
		clean_df['date_of_birth'] = pd.to_datetime(clean_df['date_of_birth'],format = 'mixed',infer_datetime_format = True,errors = 'coerce')
		return clean_df


	def _clean_company(self,clean_df):
		clean_df['company'] = clean_df['company'].apply(self._change_company)
		return clean_df

	def _change_company(self,value):
		if str(value) == 'NULL':
			return np.nan 
		else:
			return value 


	def _clean_email_address(self,clean_df):
		clean_df['email_address'] = clean_df['email_address'].apply(self._change_email)
		return clean_df
	def _change_email(self,value):
		if '@' not in str(value):
			return np.nan 
		else:
			return value 

	def _clean_address(self,clean_df):
		clean_df['address'] = clean_df['address'].apply(self._change_address)
		return clean_df
	def _change_address(self,value):
		if str(value) == 'NULL':
			return np.nan 
		else: 
			return value 


	def _clean_country(self,clean_df):
		clean_df['country'] = clean_df['country'].apply(self._change_country)
		return clean_df

	def _change_country(self,value):
		valid_country_code = ['United Kingdom','Germany','United States']
		if value not in valid_country_code:
			return np.nan 
		else:
			return value 

	def _clean_country_code(self,clean_df):
		clean_df['country_code'] = clean_df['country_code'].apply(self._change_country_code)
		return clean_df

	def _clean_phone_number(self,clean_df):
		clean_df['phone_number'] = clean_df['phone_number'].apply(self._change_phone_number)
		return clean_df

	def _change_phone_number(self,value):
		for literal in str(value):
			if literal in '()+-X.x ':
				value = value.replace(literal,'')
		if value == 'NULL':
			return np.nan
		return value

	def _clean_join_date(self,clean_df):
		clean_df['join_date'] = pd.to_datetime(clean_df['join_date'],format = 'mixed',infer_datetime_format = True,errors = 'coerce')
		return clean_df

	def _clean_user_uuid(self,clean_df):
		clean_df['user_uuid'] = clean_df['user_uuid'].apply(self._change_user_uuid)
		return clean_df

	def _change_user_uuid(self,value):
		if str(value) == 'NULL':
			return np.nan
		elif len(str(value)) < 36:
			return np.nan
		else:
			return value

# ----------------------------------------card data -------------------------------------------------------------------------------------
	def clean_card_data(self,card_data_df):
		clean_df = card_data_df.dropna(axis = 1,how = 'all')
		# breakpoint()
		# first we will remove non int values from card number:
		clean_df = self._clean_card_number_column(clean_df)
		clean_df = self._clean_expiry_date(clean_df)
		clean_df = self._clean_date_payment_confirmed(clean_df)
		return clean_df

	def _clean_card_number_column(self,clean_df):
		clean_df = clean_df[pd.to_numeric(clean_df['card_number'],errors = 'coerce').notnull()]
		return clean_df

	def _clean_expiry_date(self,clean_df):
		# breakpoint()
		clean_df['expiry_date']=clean_df['expiry_date'].astype('str')
		# now we will separate expiry month and expiry year from the column
		expiry_month_list = []
		expiry_year_list = []
		for value in clean_df["expiry_date"]:
			expiry_month_list.append(value.split('/')[0])
			expiry_year_list.append(value.split('/')[1])
		clean_df['expiry_month'] = expiry_month_list
		clean_df['expiry_year'] = expiry_year_list
		clean_df = clean_df.drop('expiry_date',axis = 1)
		return clean_df

	def _clean_date_payment_confirmed(self,clean_df):
		clean_df['date_payment_confirmed'] = pd.to_datetime(clean_df['date_payment_confirmed'],format = 'mixed',infer_datetime_format = True)
		return clean_df
# --------------------------------store details-----------------------------------------------------------------

	def clean_store_data(self,store_dataframe):
		clean_store_df = store_dataframe.dropna(axis = 1,thresh = 350)
		clean_store_df = clean_store_df.dropna(axis = 0, thresh = 8)
		clean_store_df = self._clean_opening_date_column(clean_store_df)
		clean_store_df = self._clean_country_code(clean_store_df)
		clean_store_df = self._clean_continent(clean_store_df)
		clean_store_df = self._clean_store_type(clean_store_df)
		clean_store_df = self._clean_staff_number(clean_store_df)
		clean_store_df = self._clean_latitude_and_longitude(clean_store_df)

		return clean_store_df

	def _clean_opening_date_column(self,store_dataframe):
		store_dataframe['opening_date'] = pd.to_datetime(store_dataframe['opening_date'],infer_datetime_format = True,errors='coerce')
		return store_dataframe
		

	def _clean_country_code(self,store_dataframe):
		# country code can have only two character long values so any values longer than that can be replaces with NULL or row can be dropped
		store_dataframe['country_code']=store_dataframe['country_code'].apply(self._change_country_code)
		return store_dataframe

	def _change_country_code(self,value):
		if len(str(value))>2:
			return np.nan
		else:
			return value

	def _clean_continent(self,store_dataframe):
		store_dataframe['continent'] = store_dataframe['continent'].apply(self._change_continent)
		return store_dataframe

	def _change_continent(self,value):
		valid_continent_value = ['AMERICA','EUROPE']
		if value.upper() in valid_continent_value:
			return value 
		else:
			return np.nan 

	def _clean_latitude(self,store_dataframe):
		store_dataframe['latitude'] = pd.to_numeric(store_dataframe['latitude'],errors = 'coerce')
		return store_dataframe

	def _clean_store_type(self,store_dataframe):
		store_dataframe['store_type']=store_dataframe['store_type'].apply(self._change_store_type)
		return store_dataframe

	def _change_store_type(self,value):
		valid_store_types = ['Local','Super Store','Mall Kiosk','Outlet','Web Portal']
		if value in valid_store_types:
			return value 
		else:
			return np.nan 

	def _clean_staff_number(self,store_dataframe):
		store_dataframe['staff_numbers'] = store_dataframe['staff_numbers'].apply(self._change_staff_numbers)
		return store_dataframe

	def _change_staff_numbers(self,value):
		string_value = str(value)
		for literal in string_value:
			if str(value) not in '0123456789':
				return np.nan
		return value

	def _clean_latitude_and_longitude(self,store_dataframe):
		store_dataframe['longitude'] = store_dataframe['longitude'].apply(self._change_latitude_and_longitude)
		store_dataframe['latitude'] = store_dataframe['latitude'].apply(self._change_latitude_and_longitude)
		return store_dataframe

	def _change_latitude_and_longitude(self,value):
		for literal in str(value):
			if literal not in '0123456789.':
				return np.nan 
		return value
# ------------------------------product details-----------------------------------------------------------


	def convert_product_weights(self,product_dataframe):
		product_dataframe['weight'] = product_dataframe['weight'].apply(self._change_weight)
		return product_dataframe

	def _change_weight(self,value):
		x = 1
		try:
			
			x += 1	
			if value is np.nan:
				return np.nan
			elif 'x' in value:
				return np.nan
			elif value[-2:] in ['KG','Kg','kg']:
				return value[:-2]
			elif value[-1] == 'g' and value [-2] in '0123456789':
				value_in_kg = float(value[:-1])/1000
				# print(f'succeded in attempt:{x}')
				return value_in_kg
			elif value[-2:] == 'ml':
				value_in_kg = float(value[:-2])/1000 
				# print(f'succeded in attempt:{x}')
				return value_in_kg
			else:
				# print(f'succeded in attempt:{x}')
				return np.nan

		except TypeError:
			print(f'failed in attempt {x}')
			x += 1
			breakpoint()
		except ValueError:
			print(f'value error for value : {value}')
			breakpoint()

	def clean_products_data(self,product_dataframe):
		clean_products_df = self._clean_product_category(product_dataframe)
		clean_products_df = self._clean_removed(clean_products_df)
		clean_products_df = self._clean_date_added(clean_products_df)
		clean_products_df = self._clean_product_price(clean_products_df)
		clean_products_df = self.convert_product_weights(clean_products_df)
		# breakpoint()
		clean_products_df = self._clean_uuid(clean_products_df)


		return clean_products_df

	def _clean_product_category(self,product_dataframe):
		product_dataframe['category'] = product_dataframe['category'].apply(self._change_product_category)
		return product_dataframe
	def _change_product_category(self,value):
		valid_product_categories = ['homeware','toys-and-games','food-and-drink','pets','sports-and-leisure','health-and-beauty','diy']
		if value in valid_product_categories:
			return value 
		else:
			return np.nan
	def _clean_removed(self,product_dataframe):
		product_dataframe['removed'] = product_dataframe['removed'].apply(self._change_removed_column)
		return product_dataframe

	def _change_removed_column(self,value):
		valid_removed_values = ['Still_avaliable','Removed']
		if value in valid_removed_values:
			return value 
		else:
			return np.nan
	def _clean_product_price(self,product_dataframe):
		product_dataframe['product_price'] = product_dataframe['product_price'].apply(self._change_product_price)
		return product_dataframe 

	def _change_product_price(self,value):
		if value is np.nan:
			return np.nan 
		elif value[0] == '£':
			substring1 = value[1:]
			for letter in substring1:
				if letter not in '0123456789.':
					return np.nan 
			return value[1:]
		else:
			return np.nan
	def _clean_date_added(self,product_dataframe):
		product_dataframe['date_added'] = pd.to_datetime(product_dataframe['date_added'],infer_datetime_format = True,format = 'mixed',errors = 'coerce')
		return product_dataframe
	def _clean_uuid(self,product_dataframe):
		product_dataframe['uuid'] = product_dataframe['uuid'].apply(self._change_uuid)
		return product_dataframe

	def _change_uuid(self,value):
		# breakpoint()
		if value == np.nan:
			return np.nan 
		elif len(str(value)) < 36:
			return np.nan 
		else:
			return value 
# ----------------------------orders data-------------------------------------------
	def clean_orders_data(self,order_dataframe):
		order_dataframe.drop(['first_name','last_name','1'],axis = 1,inplace = True)
		return order_dataframe

# ----------------------datetime json file----------------------------------------
	def clean_datetime_json_df(self,datetime_json_df):
		datetime_json_df = datetime_json_df.reset_index()
		clean_datetime_json_df = self._clean_month(datetime_json_df)
		clean_datetime_json_df = self._clean_year(clean_datetime_json_df)
		clean_datetime_json_df = self._clean_day(clean_datetime_json_df)
		clean_datetime_json_df = self._clean_timestamp(clean_datetime_json_df)
		clean_datetime_json_df = self._clean_date_uuid(clean_datetime_json_df)
		clean_datetime_json_df = self._clean_time_period(clean_datetime_json_df)

		return clean_datetime_json_df

	def _clean_month(self,datetime_json_df):
		datetime_json_df['month'] = datetime_json_df['month'].apply(self._change_month)
		return datetime_json_df 

	def _change_month(self,value):
		# for value in datetime_json_df['month']:
		for literal in str(value):
			if literal not in '0123456789':
				return np.nan 
		return value 

	def _clean_year(self,datetime_json_df):
		datetime_json_df['year'] = datetime_json_df['year'].apply(self._change_year)

		return datetime_json_df 

	def _change_year(self,value):
		# for value in datetime_json_df['year']:
		for literal in str(value):
			if literal not in '0123456789':
				return np.nan 
			
		return value 

	def _clean_day(self,datetime_json_df):
		datetime_json_df['day'] = datetime_json_df['day'].apply(self._change_day)
		return datetime_json_df 

	def _change_day(self,value):
		# for value in datetime_json_df['day']:
		for literal in str(value):
			if literal not in '0123456789':
				return np.nan 
		return value 

	def _clean_timestamp(self,datetime_json_df):
		datetime_json_df['timestamp'] = datetime_json_df['timestamp'].apply(self._change_timestamp)
		datetime_json_df['timestamp'] = pd.to_datetime(datetime_json_df['timestamp'],infer_datetime_format = True,format = 'mixed',errors = 'coerce')
		return datetime_json_df

	def _change_timestamp(self,value):
		# for value in datetime_json_df['timestamp']:
		for literal in str(value):
			if literal not in '0123456789:':
				return np.nan 
		return value 

	def _clean_date_uuid(self,datetime_json_df):
		datetime_json_df['date_uuid'] = datetime_json_df['date_uuid'].apply(self._change_date_uuid)
		return datetime_json_df

	def _change_date_uuid(self,value):
		if str(value) == "NULL":
			return np.nan 
		elif len(str(value))<36:
			return np.nan 
		else:
			return value

	def _clean_time_period(self,datetime_json_df):
		datetime_json_df['time_period'] = datetime_json_df['time_period'].apply(self._change_time_period)
		return datetime_json_df 

	def _change_time_period(self,value):
		valid_time_period_values = ['Evening','Morning','Midday','Late_Hours']
		if value in valid_time_period_values:
			return value 
		else:
			return np.nan
