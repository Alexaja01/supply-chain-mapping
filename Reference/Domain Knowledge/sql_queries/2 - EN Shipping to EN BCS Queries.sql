------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------EN Shipping to EN BCS-------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------

--TO START FROM SCRATCH DELETE BCS_LINE_ITEM,BCS_PERIOD AND BCS TABLES

select * from bcs
select * from bcs_period
select * from bcs_line_item


--DELETE FROM bcs_line_item;  was 6688
--DELETE FROM bcs_period;  was 454
--DELETE FROM bcs;  was 227




----EXPECTED DATA QUERIES  ---------------------------------------------------------------------------------------------------------------

----EN BCS TABLE--------------------------------------------------------------------------------------------------------------------------
---- GENERATE EXPECTED DATA FOR INSERTS FOR EN BCS TABLE ---------------------------------------------------------------------------------------------

--USE TO POPULATE THE "query_bcs" TAB IN THE EN Shipping to EN BCS Test File (EXCEL)
SELECT
concat('EN_Shipping_',x.terminal_market_name,'_',x.tcn4) AS bcs_code
,concat('EN_Shipping_',x.terminal_market_name,'_',x.tcn4) AS bcs_name
,'Shipping' AS bcs_type_name
,x.terminal_id AS primary_terminal_alias
,'EN Master UUID' AS terminal_alias_type_code
FROM(
		SELECT DISTINCT sp.terminal_id,tm.terminal_market_name,t.tcn4
				 FROM shipping_period sp 
				 LEFT JOIN terminal t USING(terminal_id) 
				 LEFT JOIN terminal_market tm USING(terminal_market_id) 
				 WHERE sp.terminal_id=tm.shipping_terminal_id 
					-- and sp.start_date = '2023-10-01' and sp.end_date='2023-12-31'
					   AND (tm.modified_date::date >='2024-01-23' OR sp.modified_date::date >='2024-01-23'))x
ORDER BY primary_terminal_alias
;



select * from shipping_period where terminal_id = 'd6e0daa7-dbc0-4b37-b19e-492536f0f325'


----YOU HAVE TO TRIGGER THE EN SHIPPING TO EN BCS BEFORE YOU CAN RUN THE QUERIES BELOW



----EN BCS_PERIOD TABLE----------------------------------------------------------------------------------------------------------------------
----GENERATE EXPECTED DATA FOR INSERTS FOR EN BCS_PERIOD TABLE---------------------------------------
--BE SURE THAT ALL DATES MATCH THE USER DEFINED DATE USED IN ALL QUERIES
--USE TO POPULATE THE "query_bcs_period" TAB IN THE EN Shipping to EN BCS Test File (EXCEL)

SELECT DISTINCT
b.bcs_id
,sp.start_date
,sp.end_date
FROM bcs b
JOIN shipping_period sp ON b.primary_terminal_alias=sp.terminal_id
JOIN terminal_market tm ON sp.terminal_id=tm.shipping_terminal_id
WHERE tm.modified_date::date >='2024-01-23' OR sp.modified_date::date >='2024-01-23'
ORDER BY b.bcs_id
;





select * from shipping_period where terminal_id in ('0c687d26-1f8a-4181-ad28-3f05e2c1a3b0','d6e0daa7-dbc0-4b37-b19e-492536f0f325')
select * from shipping_line_item where shipping_period_id = '03ce5892-dcbd-493f-9182-6cdd13c2fc27'





----EN BCS_LINE_ITEM-----------------------------------------------------------------------------------------------------------------------
--USE TO POPULATE THE "query_expected_bcs" TAB IN THE EN Shipping to EN BCS Test File (EXCEL)
--YOU HAVE TO TRIGGER THE EN SHIPPING TO EN BCS BEFORE YOU CAN RUN THIS QUERY
--MUST RUN  BELOW TWO QUERIES TO POPULATE THE query_expected_bcs_line_items tab
--BE SURE THAT ALL DATES MATCH THE USER DEFINED DATE USED IN ALL QUERIES


----generate data for inserts for EN BCS_LINE_ITEM table---------------------------------------

--#1

SELECT
b.bcs_code
,bp.bcs_period_id
,bp.start_date
,bp.end_date
,sli.product_id AS product_alias
,'EN Master UUID' AS prod_alias_type_code
,sli.line_item_type_id AS line_item_type_alias
,'EN Master UUID' AS lit_alias_type_code
,si.spot_index_id AS index_alias
,'EN Master UUID' AS index_alias_type_code
,(SELECT price_day_id FROM price_day WHERE price_day_name = 'Prior Day') AS price_day_alias
,'EN Master UUID' as price_day_alias_type_code
,0 AS line_item_adder
,sli.line_item_percent
FROM shipping_line_item sli
JOIN shipping_period sp USING(shipping_period_id)
JOIN bcs b ON b.primary_terminal_alias=sp.terminal_id
JOIN bcs_period bp ON bp.bcs_id=b.bcs_id AND (bp.start_date=sp.start_date AND bp.end_date=sp.end_date)
LEFT JOIN spot_index si ON si.spot_index_id=sli.spot_index_id
LEFT JOIN terminal te ON te.terminal_id=sp.terminal_id
LEFT JOIN terminal_market tm ON te.terminal_market_id=tm.terminal_market_id
WHERE sp.terminal_id=tm.shipping_terminal_id AND (tm.modified_date::date >='2024-01-23' OR sp.modified_date::date >='2024-01-23')
ORDER BY b.bcs_code
;


--#2
--query for inserts for combined_adder line items

SELECT DISTINCT
b.bcs_code
,bp.bcs_period_id
,bp.start_date
,bp.end_date
,sli.product_id AS product_alias
,'EN Master UUID' AS prod_alias_type_code
,(SELECT line_item_type_id FROM line_item_type WHERE line_item_type_name = 'Combined Adder') AS line_item_type_alias
,'EN Master UUID' AS lit_alias_type_code
,NULL AS index_alias
,NULL AS index_alias_type_code
,NULL AS price_day_alias
,NULL AS priceday_alias_type_code
,ca.combined_adder AS line_item_adder
,1.0000 AS line_item_percent
FROM shipping_line_item sli
JOIN shipping_period sp USING(shipping_period_id)
JOIN line_item_type lit USING(line_item_type_id)
JOIN bcs b ON b.primary_terminal_alias=sp.terminal_id
JOIN bcs_period bp ON bp.bcs_id=b.bcs_id AND (bp.start_date=sp.start_date AND bp.end_date=sp.end_date)
JOIN product p ON p.product_id=sli.product_id
LEFT JOIN terminal te ON te.terminal_id=sp.terminal_id
LEFT JOIN terminal_market tm ON te.terminal_market_id=tm.terminal_market_id
JOIN (SELECT aa.shipping_period_id, aa.product_id, SUM(aa.line_item_norm_adder) AS combined_adder
			FROM (SELECT sli.shipping_period_id, sli.product_id, sli.line_item_type_id, (sli.line_item_adder * sli.line_item_percent) AS line_item_norm_adder FROM shipping_line_item sli) aa
			GROUP BY aa.shipping_period_id, aa.product_id
			ORDER BY aa.shipping_period_id, aa.product_id) ca ON sli.shipping_period_id = ca.shipping_period_id AND sli.product_id = ca.product_id
WHERE sp.terminal_id=tm.shipping_terminal_id AND tm.modified_date::date >='2024-01-23' OR sp.modified_date::date >='2024-01-23'
ORDER BY b.bcs_code
;





----ACTUAL TABLE DATA QUERIES FOR COMPARISON TO EXPECTED  --------------------------------------------------------------------------------
----USED TO PULL DATA FROM EN db BCS_LINE_ITEM TABLE TO CONFIRM AGAINST EXPECTED
----USED TO POPULATE THE "EN bcs tables-after-trigger" TAB IN THE "EN Shipping to EN BCS Test File"


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
--WHERE bcs_code = '%_4751'
--WHERE bp.modified_date::date >='2023-10-01' 
--bp.start_date = '2023-10-01' and bp.end_date = '2023-12-31'
order by b.bcs_code,bp.start_date,bp.end_date,bli.product_alias,bli.line_item_type_alias







--NO LONGER USING IN TEST FILE
-- EN db bcs_period tab data query
select b.bcs_code,bp.bcs_period_id,bp.start_date,bp.end_date 
from bcs_period bp 
left join bcs b using(bcs_id) 
order by b.bcs_code,bp.start_date



select * from bcs
select * from bcs_period
select * from bcs_line_item






--ADDITIONAL QUERIES FOR DEEP DIVES


select b.bcs_code,bp.bcs_period_id,bp.start_date,bp.end_date,pr.product_code,lit.line_item_type_name,bli.line_item_adder,bli.line_item_percent
from bcs_line_item bli 
join bcs_period bp using(bcs_period_id) 
join bcs b on b.bcs_id=bp.bcs_id
join line_item_type lit on bli.line_item_type_alias=lit.line_item_type_id
join product pr on bli.product_alias=pr.product_id
where bli.bcs_period_id in('23dbb192-ac1d-4c9f-b4e6-c7434e24b9bb','833471fb-c401-4572-b6f3-ca2f487d5bdd','ff026dde-fea4-4ad5-b13e-98dbdacd54d6')




--confirm number of inserts into bcs table and grab back_up data
select * from bcs order by modified_date desc

--confirm number of inserts into bcs_period table and grab back_up data
select * from bcs_period order by modified_date desc

--confirm number of inserts into bcs_line_item table and grab back_up data
select * from bcs_line_item order by modified_date desc