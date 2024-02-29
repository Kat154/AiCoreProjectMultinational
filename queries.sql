-- milestone 3 create database schema----------------------------------
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


ALTER TABLE orders_table ADD CONSTRAINT foreign_key_for_dim_date_times FOREIGN KEY (date_uuid) REFERENCES dim_date_times (date_uuid);
ALTER TABLE orders_table ADD CONSTRAINT foreign_key_for_dim_products FOREIGN KEY (product_code) REFERENCES dim_products (product_code);
ALTER TABLE orders_table ADD CONSTRAINT foreign_key_for_dim_users FOREIGN KEY (user_uuid) REFERENCES dim_users (user_uuid);
ALTER TABLE orders_table ADD CONSTRAINT foreign_key_for_store_details FOREIGN KEY (store_code) REFERENCES dim_store_details (store_code);
ALTER TABLE orders_table ADD CONSTRAINT foreign_key_for_dim_card_details FOREIGN KEY (card_number) REFERENCES dim_card_details (card_number);


---------------------Milestore 4 querying the data---------------------------------

 select count(*),country_code from dim_store_details group by country_code;
 select count(*),locality from dim_store_details group by locality order by count(*) desc limit 7;
 select sum(ordertable.product_quantity),datetime.month from orders_table "ordertable" 
 inner join dim_date_times "datetime" on ordertable.date_uuid = datetime.date_uuid group by datetime.month order by sum(ordertable.product_quantity) desc limit 6;
 
 select sum(ordertable.product_quantity) as "product_quantity_count",count(*) as "number_of_sales", case when store.store_type = 'Web Portal' 
 then 'Web' else 'Offline' end as "location"  from dim_store_details "store" inner join orders_table "ordertable" on store.store_code = ordertable.store_code group by location order by number_of_sales;

select sum(total_sales) from (select store.store_type,ROUND(cast(sum(ordertable.product_quantity * products.product_price) as numeric),2) as "total_sales" from dim_products "products" inner join orders_table "ordertable" on products.product_code = ordertable.product_code inner join dim_store_details "store" on store.store_code = ordertable.store_code group by store.store_type order by sum(ordertable.product_quantity * products.product_price) desc) as subquery1;


-- TASK #5

select store.store_type, Round(cast(sum(ordertable.product_quantity*products.product_price) as numeric),2) as "total_sales" ,
Round(cast(sum(ordertable.product_quantity*products.product_price)*100/
	(select sum(o.product_quantity*p.product_price) from orders_table "o" inner join dim_products "p" on o.product_code = p.product_code) as numeric),2) as "percentage_total(%)"
	from 
		orders_table "ordertable" inner join 
		dim_products "products" 
			on ordertable.product_code = products.product_code
		inner join dim_store_details "store" 
		on store.store_code = ordertable.store_code
		group by store.store_type
		order by "percentage_total(%)" desc;

-- TASK #6
select 
datetime.year ,datetime.month ,ROUND(cast(sum(ordertable.product_quantity * products.product_price) as numeric),2) as "total_sales" 
from 
orders_table "ordertable" inner join dim_date_times "datetime" 
on ordertable.date_uuid = datetime.date_uuid inner join dim_products "products" on products.product_code = ordertable.product_code 
group by datetime.year,datetime.month order by ROUND(cast(sum(ordertable.product_quantity * products.product_price) as numeric),2) desc limit 14;
-- TASK #7
 select count(user_uuid),country_code from dim_users group by country_code order by count(user_uuid) desc;

-- TASK #8

select ROUND(cast(sum(ordertable.product_quantity * products.product_price) as numeric),2) as "total_sales" , store.store_type, store.country_code
from orders_table "ordertable" 
inner join dim_products "products" on ordertable.product_code = products.product_code 
inner join dim_store_details "store" on store.store_code = ordertable.store_code and store.country_code = 'DE'
group by store.store_type,store.country_code
order by ROUND(cast(sum(ordertable.product_quantity * products.product_price) as numeric),2);



-- TASK 9



	select 
	   sum(abs(subquery2.next_hour-subquery2.current_hour))*60*60 as "hours_to_seconds",
	   sum(abs(subquery2.next_minute-subquery2.current_minute))*60 as "minutes_to_seconds",
	   sum(abs(subquery2.next_second-subquery2.current_second)) as "seconds",
	   subquery2.year,
	   count(subquery2.date_uuid)
	from
	(
		select cast(substring(subquery1.current_timestamp,1,2) as numeric) as "current_hour",
			   cast(substring(subquery1.current_timestamp,4,2) as numeric) as "current_minute" ,
			   cast(substring(subquery1.current_timestamp,7,2) as numeric) as "current_second" ,
			   cast(substring(subquery1.next_time_stamp,1,2) as numeric) as "next_hour",
			   cast(substring(subquery1.next_time_stamp,4,2) as numeric) as "next_minute" ,
			   cast(substring(subquery1.next_time_stamp,7,2) as numeric) as "next_second" ,
			   subquery1.year ,
			   subquery1.date_uuid
		from 
				(
				
					select datetime.timestamp as "current_timestamp",
					lead(datetime.timestamp,1,NULL) OVER (order by datetime.timestamp ) as "next_time_stamp" ,
					datetime.year as "year",
					datetime.date_uuid as "date_uuid"
					from    
					dim_date_times "datetime"

				) as subquery1
	) as subquery2 
	group by subquery2.year




	-- select 
	--    (sum(abs(subquery2.next_hour-subquery2.current_hour))*60*60) + (sum(abs(subquery2.next_minute-subquery2.current_minute))*60)+ (sum(abs(subquery2.next_second-subquery2.current_second))) as "difference_total_seconds",
	--    ((sum(abs(subquery2.next_hour-subquery2.current_hour))*60*60) + (sum(abs(subquery2.next_minute-subquery2.current_minute))*60)+ (sum(abs(subquery2.next_second-subquery2.current_second))))/count(subquery2.date_uuid) as "average_difference_in_seconds",
	--    subquery2.year,
	--    count(subquery2.date_uuid)
	-- from
	-- (
	-- 	select cast(substring(subquery1.current_timestamp,1,2) as numeric) as "current_hour",
	-- 		   cast(substring(subquery1.current_timestamp,4,2) as numeric) as "current_minute" ,
	-- 		   cast(substring(subquery1.current_timestamp,7,2) as numeric) as "current_second" ,
	-- 		   cast(substring(subquery1.next_time_stamp,1,2) as numeric) as "next_hour",
	-- 		   cast(substring(subquery1.next_time_stamp,4,2) as numeric) as "next_minute" ,
	-- 		   cast(substring(subquery1.next_time_stamp,7,2) as numeric) as "next_second" ,
	-- 		   subquery1.year ,
	-- 		   subquery1.date_uuid
	-- 	from 
	-- 			(
				
	-- 				select datetime.timestamp as "current_timestamp",
	-- 				lead(datetime.timestamp,1,NULL) OVER (order by datetime.timestamp ) as "next_time_stamp" ,
	-- 				datetime.year as "year",
	-- 				datetime.date_uuid as "date_uuid"
	-- 				from    
	-- 				dim_date_times "datetime"

	-- 			) as subquery1
	-- ) as subquery2 
	-- group by subquery2.year
	
