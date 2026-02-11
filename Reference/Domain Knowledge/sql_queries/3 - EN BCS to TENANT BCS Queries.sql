------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------EN BCS to TENANT BCS--------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------


----------------------------------------------------------------------------------------------------------------------------------------------------------------
-----  QUERIES FOR EN db  ---------------------------------------------------------------------------------------------------------------------------------

/*

 ******MUST BE RUN IN EN db********
 *****bcs_line-item data***********
  RETURNS EXPECTED DATA FOR COMPARISON TO JSON file from EN db bcs, bcs_period and bcs_line_item tables
  USED TO POPULATE THE "EN db generated JSON w_codes" tab  in the "EN Shipping_EN BCS_Tenant BCS QA File"

*/

select b.bcs_id
,b.bcs_code
,b.bcs_name
,b.bcs_type_name
,t.en_terminal_name
,b.primary_terminal_alias
,b.terminal_alias_type_code
,bp.bcs_period_id
,bp.bcs_id as bp_bcs_id
,bp.start_date
,bp.end_date
,bli.bcs_line_item_id
,bli.bcs_period_id as bli_bcs_period_id
,pr.product_code
,bli.product_alias
,bli.product_alias_type_code
,lit.line_item_type_name
,bli.line_item_type_alias
,bli.lit_alias_type_code
,si.spot_index_code
,bli.index_alias
,bli.index_alias_type_code
,bli.price_day_alias
,bli.price_day_alias_type_code
,bli.line_item_adder
,bli.line_item_percent 
from bcs b
left join bcs_period bp using(bcs_id)
left join bcs_line_item bli on bli.bcs_period_id = bp.bcs_period_id
left join terminal t on t.terminal_id = b.primary_terminal_alias
left join product pr on pr.product_id = bli.product_alias
left join spot_index si on bli.index_alias=si.spot_index_id
left join line_item_type lit on lit.line_item_type_id = bli.line_item_type_alias
--WHERE bp.modified_date::date >='2023-10-01' 
--bp.start_date = '2023-10-01' and bp.end_date = '2023-12-31'
order by b.bcs_code,bp.start_date,bp.end_date,bli.product_alias,bli.line_item_type_alias





/*

 ******MUST BE RUN IN EN db********
  RETURNS EXPECTED EN bcs_period USED IN "EN db bcs_period" tab  in the "EN Shipping_EN BCS_Tenant BCS QA File"
 
*/


select b.bcs_code,bp.bcs_period_id,bp.start_date,bp.end_date 
from bcs_period bp 
left join bcs b using(bcs_id) 
order by b.bcs_code,bp.start_date



-----------------------------------------------------------------------------------------------------------------------------------------------------------
--  NEXT STEPS  -------------------------------------------------------------------------------------------------------------------------------------------


/*  GENERATE EN BCS TO TENANT BCS FILE IN UI     */



/* PUBLISH JSON FILE THAT YOU GENERATED IN THE UI   */



/* 

  *****   DELETE ALL FILES (FOLDER WILL BE DELETED) FROM ALPHA IF YOU DO NOT WANT TO PUBLISH TO THAT TENANT PRIOR TO TRIGGERING EN BCS TO TENANT BCS PROCESS   

*/



/*    TRIGGER EN BCS TO TENANT BCS IN THE UI     */



----------------------------------------------------------------------------------------------------------------------------------------------------------------
-----  QUERIES FOR CATALOG db  ---------------------------------------------------------------------------------------------------------------------------------

--QUERY TO REFLECT THE RESULTS OF A PROCESSED EN BCS TO TENANT BCS FILE BY TENANT
--  QUERY MUS BE RUN IN CATALOG DB IN ACTIVITY_TRACKING SCHEMA

select st.tenant_id,st.filename,at.activity_type_name,st.count,st.activity_date,st.created_date
from activity_tracking.shipping_tracking  st
left join activity_tracking.activity_type at using(activity_type_id)
order by st.created_date desc,tenant_id,at.activity_type_name








----------------------------------------------------------------------------------------------------------------------------------------------------------------
-----  QUERIES FOR TENANT db  ---------------------------------------------------------------------------------------------------------------------------------

--QUERIES TO SEE ETL PROCESS HAS STARTED AND COMPLETED ALONG WITH VIEWING ANY ERRORS
--THESE ARE RUN IN THE TENANT DB'S

select * from batch order by created_date desc


select * from terminal_alias_error order by created_date desc
select * from product_alias_error order by created_date desc
select * from index_alias_error order by created_date desc
select * from line_item_type_alias_error order by created_date desc
select * from price_day_alias_error order by created_date desc




--RUN QUERIES BELOW IN TENANT DB'S AFTER RUNNING EN BCS TO TENANT BCS TRIGGER

--BCS, BCS PERIOD AND BCS LINE ITEM FOR SHIPPING BCS IN TENANT DB
--RUN IN TENANT DB QA AFTER INSERTS FROM EN BCS JSON FILE
--RUN SUBQUERY TO BE USED TO POPULATE THE "Tenant shipping bcs" tab  in the "EN Shipping_EN BCS_Tenant BCS QA File"
--OVERALL QUERY SHOWS ANY LINE ITEMS (EXCLUDING COMBINED ADDER) THAT DO NOT HAVE AN INDEX ID)

SELECT b.bcs_id
,b.bcs_code
,b.bcs_name
,bt.bcs_type_name
,b.primary_terminal_id
,bp.bcs_period_id
,bp.bcs_id AS bp_bcs_id
,bp.start_date
,bp.end_date
,bli.bcs_line_item_id
,bli.bcs_period_id AS bli_bcs_period_id
,bli.product_id
,pr.product_code
,bli.line_item_type_id
,lit.line_item_type_name
,bli.index_id
,x.index_code
,bli.price_day_id
,pd.price_day_name
,bli.line_item_adder
,bli.line_item_percent
,bli.modified_date
,b.created_date
,bp.created_date
,bp.modified_date
FROM bcs_line_item bli
LEFT JOIN bcs_period bp using(bcs_period_id)
LEFT JOIN bcs b on bp.bcs_id=b.bcs_id
LEFT JOIN bcs_type bt on b.bcs_type_id=bt.bcs_type_id
LEFT JOIN product pr on bli.product_id=pr.product_id
LEFT JOIN line_item_type lit on bli.line_item_type_id=lit.line_item_type_id
LEFT JOIN price_day pd on bli.price_day_id=pd.price_day_id
LEFT JOIN index x USING (index_id)
WHERE bt.bcs_type_name = 'Shipping'
 --and  bcs_code ilike 'EN_Shipping_Jacksonville FL_2112%'
ORDER BY b.bcs_code,start_date,end_date,pr.product_code,lit.display_order




--QUERIES TO UPDATE ALIAS DATA TABS FOR EN SHIPPING_EN BCS_TENANT BCS QA FILE

select ia.*,at.alias_type_code from index_alias ia left join alias_type at using(alias_type_id)

select pa.*,at.alias_type_code from product_alias pa left join alias_type at using(alias_type_id)

select ta.*,at.alias_type_code from terminal_alias ta left join alias_type at using(alias_type_id) --where terminal_alias_code = 'e6937961-3027-40bf-a78b-67bb1db07db2'


select lita.*,at.alias_type_code from line_item_type_alias lita left join alias_type at using(alias_type_id)

select pda.*,at.alias_type_code from price_day_alias pda left join alias_type at using(alias_type_id)



select * from bcs where bcs_type_id = '43b2c528-cecc-4369-a498-88645827bec0' order by bcs_code

select * from bcs where bcs_type_id = 'bef3e549-28a0-4244-abd6-b5054ce5f234'

select sm.spot_market_name,si.* from index x left join spot_index si using si.index_id = x.index_id left join spot_market sm using sm.spot_market_id = si.spot_market_id  where index_code  ilike 'PL_C%' order by index_code


/*  DEEP DIVE QUERIES    */


select * from spot_index where spot_index_code ilike '%ETH%'


select * from bcs where bcs_type_id = (select bcs_type_id from bcs_type where bcs_type_name = 'Shipping')
---use this query to ensure the bcs_period_status_override was not defaulted back to zero for Atlanta Contract newest period - should be 1 with bcs_period_status_id = 'c5029f94-3e92-41ca-9bf9-1804376bea79'
select * from bcs_period where bcs_id = (select bcs_id from bcs where bcs_name ilike 'Atlanta GA BP Gas 2022') order by created_date desc

---use below queries for a quick glance or details from specific bcs tables to see recent changes

select * from bcs where bcs_type_id = (select bcs_type_id from bcs_type where bcs_type_name = 'Shipping')

select * from bcs order by modified_date desc

select * from bcs_period where cwg_status_id is null order by modified_date desc

select * from bcs_line_item order by modified_date desc

select * from bcs_line_item where bcs_period_id in('fc728442-2e9c-4e84-bdb0-327b6f7f49b6','d324ee6b-afe4-4c98-b529-108fbffb18c3') order by product_id,line_item_type_id


--query to get count of Shipping status and bcs_period status to compare to Shipping Expired values in shipping_tracking table
--this should be run in tenant db
select distinct z.shipping_status, count(z.bcs_code) as count,z.bp_status
from(
select distinct x.bcs_code
,case when sum(x.current_shipping) >= 1 then 'Current'
	  when sum(x.future_shipping) >= 1 and sum(x.current_shipping) = 0 then 'Future'
	  when sum(x.expired_shipping) >= 1 and sum(x.current_shipping) = 0 and sum(x.future_shipping) = 0 then 'Expired'
	  else NULL end as shipping_status
--,case when sum(x.expired_shipping) >= 1 and sum(x.current_shipping) = 0 and sum(x.future_shipping) = 0 then exb.bp_status end as bp_status
,exb.bp_status
from(
select distinct b.bcs_code,bp.start_date,bp.end_date
,case when bp.start_date<CURRENT_DATE and bp.end_date<CURRENT_DATE then 1 else 0 end as expired_shipping
,case when bp.start_date<=CURRENT_DATE and bp.end_date>=CURRENT_DATE then 1 else 0 end as current_shipping
,case when bp.start_date>CURRENT_DATE and bp.end_date>CURRENT_DATE then 1 else 0 end as future_shipping
from bcs b
left join bcs_period bp on bp.bcs_id=b.bcs_id
left join bcs_type bt on b.bcs_type_id=bt.bcs_type_id
where bt.bcs_type_name = 'Shipping'
order by b.bcs_code,bp.end_date desc)x
left join(select distinct b.bcs_code,bps.bcs_period_status_name as bp_status
		  from  bcs_period bp
				left join bcs_period_status bps on bp.bcs_period_status_id=bps.bcs_period_status_id
				left join bcs b on bp.bcs_id=b.bcs_id
		  		left join bcs_type bt on bt.bcs_type_id = b.bcs_type_id
			where bcs_type_name = 'Shipping'
		  		--and bp.end_date <CURRENT_DATE --and bps.bcs_period_status_name = 'In Progress'
			order by bcs_code)exb on x.bcs_code = exb.bcs_code
group by x.bcs_code,exb.bp_status
order by x.bcs_code,shipping_status,bp_status)z
group by z.shipping_status,z.bp_status
order by z.shipping_status,z.bp_status