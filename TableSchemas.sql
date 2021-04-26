Create table dim_product(
product_id VARCHAR(255) ,
product_name VARCHAR(255),
business_unit VARCHAR(255),
file_name VARCHAR(255)
);

Create table public.fct_rx_dispense(
npi_id VARCHAR(255) ,
business_unit VARCHAR(255),
product_id VARCHAR(255),
true_week_end date,
rx_packs float(25),
file_name VARCHAR(255)
);

Create table public.dim_hcp(
npi_id VARCHAR(255) ,
business_unit VARCHAR(255),
territory_id VARCHAR(255),
target_status VARCHAR(255),
date_updated date,
file_name VARCHAR(255)
);

--4) Write a query that will output the total number of Epinephrine
--packs written between January 2018 and June 2018 split by product.
select product_id, ROUND(cast(sum(rx_packs) as numeric),2)
from public.fct_rx_dispense
where business_unit = 'Epinephrine' and true_week_end between '2018-01-01' and '2018-06-01'
group by 1;

-- 5) How many Auvi-Q packs were dispensed by product each week?
Select a.product_name,b.true_week_end,ROUND(cast(sum(b.rx_packs) as numeric),2) as rx_packs
from public.dim_product a
left join public.fct_rx_dispense b
on a.product_id=b.product_id
where  a.product_name like '%AUVI-Q%'
group by 1,2
order by a.product_name,b.true_week_end;

-- 6) Examine Auvi-Q products against all Epinephrine products
-- in territory V0101 in this same time period.
-- How much Auvi-Q is dispensed in this territory,
-- how much of that total was dispensed by targeted HCPs?

Select 'Auvi-Q' as Product_name,ROUND(cast(sum(rx_packs) as numeric),2) as rx_packs,target_status
from(
Select product_name, ROUND(cast(sum(rx_packs) as numeric),2) as rx_packs,target_status,territory_id
from(
      Select a.* ,c.target_status,c.territory_id
      from(
			 Select a.product_name,
	               b.rx_packs
	               ,round(cast(b.npi_id as numeric),0) as npi_id
			 from
			     (Select * from public.dim_product where product_name like '%AUVI-Q%')a
			  join (Select *
					from public.fct_rx_dispense
					where true_week_end between '2018-01-01' and '2018-06-01'
				   )b on a.product_id=b.product_id

			union
	        Select a.product_name,
	                b.rx_packs
	                 ,round(cast(b.npi_id as numeric),0) as npi_id
			 from
			     (Select * from public.dim_product where product_name like '%EPINEPHRINE%')a
			 join (Select *
					from public.fct_rx_dispense
					where true_week_end between '2018-01-01' and '2018-06-01'
				   )b on a.product_id=b.product_id

		  )a
join
    (Select round(cast(npi_id as numeric),0) as npi_id,business_unit,target_status,territory_id,
             date_updated from public.dim_hcp where territory_id='V0101')  c
on a.npi_id=c.npi_id
)d group by 1,3,4 order by product_name
)e where e.product_name like '%AUVI-Q%'
group by 1,3
;

