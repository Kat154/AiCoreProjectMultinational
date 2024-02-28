alter table orders_table alter column store_code SET DATA TYPE varchar(12);
alter table orders_table alter column card_number SET DATA TYPE varchar(19);
alter table orders_table alter column product_code SET DATA TYPE varchar(11);
alter table orders_table alter column product_quantity SET DATA TYPE smallint;
alter table orders_table alter column date_uuid SET DATA TYPE uuid using date_uuid::uuid;
alter table orders_table alter column user_uuid SET DATA TYPE uuid using user_uuid::uuid;
alter table dim_users alter column first_name SET DATA TYPE varchar(255);

alter table dim_users alter column first_name SET DATA TYPE varchar(255);
alter table dim_users alter column last_name SET DATA TYPE varchar(255);
alter table dim_users alter column country_code SET DATA TYPE varchar(2);
alter table dim_users alter column date_of_birth SET DATA TYPE date;
alter table dim_users alter column join_date SET DATA TYPE date;
alter table dim_users alter column user_uuid SET DATA TYPE uuid using user_uuid::uuid;

alter table dim_store_details alter column locality  SET DATA TYPE varchar(255) ;
alter table dim_store_details alter column store_code  SET DATA TYPE varchar(12);
alter table dim_store_details alter column opening_date SET DATA TYPE date;
alter table dim_store_details alter column country_code SET DATA TYPE varchar(2) ;
alter table dim_store_details alter column continent  SET DATA TYPE varchar(255);
alter table dim_store_details alter column longitude SET DATA TYPE float using longitude::float;
alter table dim_store_details alter column staff_numbers SET DATA TYPE smallint using staff_numbers::smallint;
alter table dim_store_details alter column latitude SET DATA TYPE float using latitude::float;
alter table dim_store_details alter column store_type SET DATA TYPE varchar(255) ;
alter table dim_store_details alter column store_type DROP NOT NULL ;
update dim_store_details set locality = NULL where locality ='N/A';


alter table dim_products ADD weight_class varchar(15);
alter table dim_products alter column weight set DATA TYPE float using weight::double precision;
update dim_products set weight_class = 'Light' where weight < 2;
update dim_products set weight_class = 'Mid-Sized' where weight >= 2 and weight < 40;
update dim_products set weight_class = 'Heavy' where weight >= 40 and weight < 140;
update dim_products set weight_class = 'Truck_Required' where weight >=140;
ALTER TABLE dim_products RENAME COLUMN removed TO still_available;
ALTER TABLE dim_products ALTER column product_price SET DATA TYPE float using product_price::double precision;
ALTER TABLE dim_products ALTER column "EAN"  SET DATA TYPE varchar(20);
ALTER TABLE dim_products ALTER column product_code SET DATA TYPE varchar(15);
ALTER TABLE dim_products ALTER column date_added SET DATA TYPE date;
ALTER TABLE dim_products ALTER column uuid SET DATA TYPE uuid using uuid::uuid;
update dim_products set still_available = 'True' where still_available = 'Still_avaliable';
update dim_products set still_available = 'False' where still_available = 'Removed';
ALTER TABLE dim_products ALTER column still_available SET DATA TYPE bool using still_available::boolean;
ALTER TABLE dim_products ALTER column weight_class SET DATA TYPE varchar(15);




ALTER TABLE dim_date_times ALTER column month SET DATA TYPE varchar(2);
ALTER TABLE dim_date_times ALTER column year SET DATA TYPE varchar(4);
ALTER TABLE dim_date_times ALTER column day SET DATA TYPE varchar(2);
ALTER TABLE dim_date_times ALTER column time_period SET DATA TYPE varchar(15);
ALTER TABLE dim_date_times ALTER column date_uuid  SET DATA TYPE uuid using date_uuid::uuid;



ALTER TABLE dim_card_details ALTER column card_number SET DATA TYPE varchar(50);
ALTER TABLE dim_card_details ALTER column expiry_date SET DATA TYPE varchar(50);
ALTER TABLE dim_card_details ALTER column date_payment_confirmed SET DATA TYPE date;

ALTER TABLE dim_card_details ADD PRIMARY KEY (card_number);
ALTER TABLE dim_date_times ADD PRIMARY KEY (date_uuid);
ALTER TABLE dim_products ADD PRIMARY KEY (product_code);
ALTER TABLE dim_users ADD PRIMARY KEY (user_uuid);
ALTER TABLE dim_store_details ADD PRIMARY KEY (store_code);


ALTER TABLE orders_table ADD CONSTRAINT foreign_key_for_dim_card_details FOREIGN KEY (card_number) REFERENCES dim_card_details (card_number);
ALTER TABLE orders_table ADD CONSTRAINT foreign_key_for_dim_date_times FOREIGN KEY (date_uuid) REFERENCES dim_date_times (date_uuid);
ALTER TABLE orders_table ADD CONSTRAINT foreign_key_for_dim_products FOREIGN KEY (product_code) REFERENCES dim_products (product_code);
ALTER TABLE orders_table ADD CONSTRAINT foreign_key_for_dim_users FOREIGN KEY (user_uuid) REFERENCES dim_users (user_uuid);
ALTER TABLE orders_table ADD CONSTRAINT foreign_key_for_store_details FOREIGN KEY (store_code) REFERENCES dim_store_details (store_code);