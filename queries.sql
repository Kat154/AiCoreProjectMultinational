alter table orders_table alter column store_code SET DATA TYPE varchar(12);
alter table orders_table alter column card_number SET DATA TYPE varchar(19);
alter table orders_table alter column product_code SET DATA TYPE varchar(11);
alter table orders_table alter column product_quantity SET DATA TYPE smallint;
alter table orders_table alter column date_uuid SET DATA TYPE uuid using date_uuid::uuid;
alter table orders_table alter column user_uuid SET DATA TYPE uuid using user_uuid::uuid;
alter table dim_users alter column


