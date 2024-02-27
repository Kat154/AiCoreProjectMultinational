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
ALTER TABLE dim_products ALTER column EAN  SET DATA TYPE varchar(20);
ALTER TABLE dim_products ALTER column product_code SET DATA TYPE varchar(15);
ALTER TABLE dim_products ALTER column date_added SET DATA TYPE date;
ALTER TABLE dim_products ALTER column uuid SET DATA TYPE uuid using uuid::uuid;
update dim_products set still_available = 'True' where still_available = 'still_available';
update dim_products set still_available = 'False' where still_available = 'removed';
ALTER TABLE dim_products ALTER column still_available SET DATA TYPE bool using still_available::boolean;
ALTER TABLE dim_products ALTER column  SET DATA TYPE 
ALTER TABLE dim_products ALTER column  SET DATA TYPE 
