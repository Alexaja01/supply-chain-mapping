----  EN COSTING TO EN SHIPPING-------------------------------------------------------------------------------------------------------------

--GET BACKUP OF SHIPPING_PERIOD
--USED TO POPULATE THE "shipping_period backup" TAB IN THE "EN Costing to EN Shipping" test file

select * from shipping_period


---GET BACKUP OF SHIPPING_LINE_ITEM TABLE
--USED TO POPULATE THE "shipping_line_item backup" TAB IN THE "EN Costing to EN Shipping" test file

select * from shipping_line_item order by shipping_period_id,product_id



--TO START FROM SCRATCH DELETE SHIPPING_LINE_ITEM AND SHIPPING_PERIOD DATA

--DELETE FROM shipping_line_item

--DELETE FROM shipping_period




--QUERY TO RETURN EXPECTED SHIPPING_PERIOD DATA FROM COSTING TO SHIPPING_PERIOD
--USE TO POPULATE THE "query_expected_shipping_period" TAB IN THE "EN Costing to EN Shipping" test file

-- Get the shipping period insert data (spin) for each terminal
	-- BE SURE TO UPDATE THE CURRENT_DATE TO AN EFFECTIVE DATE IF PULLING MORE THAN JUST THE CURRENT PERIODS
	-- you should have one record per terminal_id
	-- we use the above query to pull the set of costing data that we want to use to find the period start and end dates
		
SELECT DISTINCT spin.terminal_id, MAX(spin.start_date) AS shipping_period_start_date, MIN(spin.end_date) AS shipping_period_end_date
	FROM (
		SELECT	DISTINCT co.costing_id, co.terminal_id, co.product_category_id, co.costing_item_id, co.costing_value, co.start_date, co.end_date, ci.shipping_status
			FROM costing co
				JOIN costing_item ci USING (costing_item_id)
				JOIN (
					SELECT tp.terminal_id, tp.product_id, ss.base_product_id, bpr.product_category_id
						FROM public.terminal_product tp
							JOIN public.shipping_setup ss USING (terminal_product_id)
							JOIN public.product bpr ON ss.base_product_id = bpr.product_id
						WHERE tp.shipping_status = 1
					) tpss ON co.terminal_id = tpss.terminal_id AND co.product_category_id = tpss.product_category_id
			WHERE co.start_date <= '2024-02-01' AND co.end_date >= '2024-02-01'	-- Replace CURRENT_DATE with user defined effective date
				AND co.terminal_id 
					--= '06244245-90ce-4817-8919-f293a9eed020'
					IN (SELECT DISTINCT tp.terminal_id FROM public.terminal_product tp WHERE tp.shipping_status = 1)	-- Get the list of terminals that we can push into Shipping tables
				AND ci.shipping_status = 1
	) spin
	GROUP BY terminal_id
	ORDER BY terminal_id,shipping_period_start_date
;




---  NEW QUERY WHEN CHANGES ARE MADE WITH SSI-1443
--- BE SURE TO UPDATE THE EFFECTIVE DATE FOR THE PERIOD IF RUNNING PAST AND CURRENT
--- IF RUNNING JUST CURRENT USE TODAY OR FUTURE DATE

select distinct tp.terminal_product_id,t.en_terminal_name,x.*
,lit.line_item_type_name
,case when sx.spot_index_id is null then sie.spot_index_id else sx.spot_index_id end as spot_index_id
,case when sx.spot_index_code is null then sie.spot_index_code else sx.spot_index_code end as spot_index_code
from(SELECT tp.terminal_id, tp.product_id, ss.line_item_type_id, ss.base_product_id,bpr.product_code, ss.line_item_percent, bpr.product_category_id, SUM(spin.costing_value)
		--,pr.product_code,bpr.product_code,lit.line_item_type_name
			FROM public.terminal_product tp
				JOIN public.shipping_setup ss USING (terminal_product_id)
				JOIN public.line_item_type lit on ss.line_item_type_id=lit.line_item_type_id
				JOIN public.product pr on tp.product_id=pr.product_id
				JOIN public.product bpr ON ss.base_product_id = bpr.product_id
				LEFT JOIN (
					SELECT	DISTINCT co.costing_id, co.terminal_id, co.product_category_id, co.costing_item_id, co.costing_value, co.start_date, co.end_date, ci.shipping_status
						FROM costing co
							JOIN costing_item ci USING (costing_item_id)
							JOIN (
								SELECT tp.terminal_id, tp.product_id, ss.base_product_id, bpr.product_category_id
									FROM public.terminal_product tp
										JOIN public.shipping_setup ss USING (terminal_product_id)
										JOIN public.product bpr ON ss.base_product_id = bpr.product_id
									WHERE tp.shipping_status = 1
								) tpss ON co.terminal_id = tpss.terminal_id AND co.product_category_id = tpss.product_category_id
						WHERE co.start_date <=CURRENT_DATE AND co.end_date >=  CURRENT_DATE-- CURRENT_DATE	-- Replace CURRENT_DATE with user defined effective date
							AND co.terminal_id IN (SELECT DISTINCT tp.terminal_id FROM public.terminal_product tp WHERE tp.shipping_status = 1)	-- Get the list of terminals that we can push into Shipping tables
							AND ci.shipping_status = 1 --and co.terminal_id='e5a50489-196c-451d-b089-3f0fd08897ad' and co.product_category_id = '48ea557d-1b8b-4eb6-9337-dba4b41981d3'
				) spin ON tp.terminal_id = spin.terminal_id AND bpr.product_category_id = spin.product_category_id
			WHERE tp.shipping_status = 1 --and tp.terminal_id='e5a50489-196c-451d-b089-3f0fd08897ad'
			GROUP BY tp.terminal_id, tp.product_id, ss.line_item_type_id, ss.base_product_id, ss.line_item_percent, bpr.product_category_id,pr.product_code,bpr.product_code,lit.line_item_type_name
			ORDER BY tp.terminal_id, tp.product_id, ss.line_item_type_id)x
JOIN product bpr ON x.base_product_id = bpr.product_id
JOIN product_category bpc ON bpr.product_category_id = bpc.product_category_id
JOIN line_item_type lit on x.line_item_type_id = lit.line_item_type_id
LEFT JOIN terminal_path_link terpl ON x.terminal_id = terpl.terminal_id AND bpc.product_category_id = terpl.product_category_id
LEFT JOIN shipping_path sp USING (shipping_path_id)
LEFT JOIN spot_market_location_link smll ON sp.shipping_path_origin_id = smll.transportation_location_link_id
LEFT JOIN spot_market sm USING (spot_market_id)
LEFT JOIN spot_index sx ON sm.spot_market_id = sx.spot_market_id AND x.base_product_id = sx.product_id --AND sx.index_component_id = (SELECT index_component_id FROM index_component WHERE index_component_code = 'C')
LEFT JOIN spot_index sxx on x.base_product_id = sxx.product_id --AND sxx.index_component_id = (SELECT index_component_id FROM index_component WHERE index_component_code = 'C')
LEFT JOIN terminal t on x.terminal_id = t.terminal_id
LEFT JOIN terminal_product tp on x.terminal_id = tp.terminal_id and x.product_id = tp.product_id
LEFT JOIN shipping_setup sse on tp.terminal_product_id=sse.terminal_product_id and x.line_item_type_id = sse.line_item_type_id
LEFT JOIN spot_index sie on sse.index_id = sie.spot_index_id
ORDER BY t.en_terminal_name,x.product_id,x.line_item_type_id



-----NO LONGER USE QUERY BELOW ONCE CHANGES WERE MADE WITH SSI-1443
--QUERY TO RETURN SHIPPING LINE ITEMS ALONG WITH SPOT INDEXES (SHOWS ANY LINE ITEMS (EXCLUDING COMBINED ADDER) THAT DID NOT FIND A SPOT INDEX)
--USE TO POPULATE THE "query_expected_shppng_line_item" TAB IN THE "EN Costing to EN Shipping" test file

/*returns line items with percents and adders along with spot_index data for those that find a match using the shipping_path origin for the base product
  and those that are defined based on line_item_type, i.e. RIN, CARB 1, CARB 2 and Line Space   */

select distinct tp.terminal_product_id,t.en_terminal_name,x.*
,case when x.line_item_type_id = (select line_item_type_id from line_item_type where line_item_type_name = 'RIN') then sxx.spot_index_id
	  when x.line_item_type_id = (select line_item_type_id from line_item_type where line_item_type_name = 'CARB 1') then sxx.spot_index_id
	  when x.line_item_type_id = (select line_item_type_id from line_item_type where line_item_type_name = 'CARB 2') then sxx.spot_index_id
	  when x.line_item_type_id = (select line_item_type_id from line_item_type where line_item_type_name = 'Line Space') then sxx.spot_index_id
	  when x.line_item_type_id = (select line_item_type_id from line_item_type where line_item_type_name = 'Ethanol') and sx.spot_index_id is null then sxx.spot_index_id
	  else sx.spot_index_id end as spot_index_id
,case when x.line_item_type_id = (select line_item_type_id from line_item_type where line_item_type_name = 'RIN') then sxx.spot_index_code
	  when x.line_item_type_id = (select line_item_type_id from line_item_type where line_item_type_name = 'CARB 1') then sxx.spot_index_code
	  when x.line_item_type_id = (select line_item_type_id from line_item_type where line_item_type_name = 'CARB 2') then sxx.spot_index_code
	  when x.line_item_type_id = (select line_item_type_id from line_item_type where line_item_type_name = 'Line Space') then sxx.spot_index_code
    when x.line_item_type_id = (select line_item_type_id from line_item_type where line_item_type_name = 'Ethanol') and sx.spot_index_code is null then sxx.spot_index_code
	  else sx.spot_index_code end as spot_index_code
from(SELECT tp.terminal_id, tp.product_id, ss.line_item_type_id, ss.base_product_id,bpr.product_code, ss.line_item_percent, bpr.product_category_id, SUM(spin.costing_value),
		lit.line_item_type_name
			FROM public.terminal_product tp
				JOIN public.shipping_setup ss USING (terminal_product_id)
				JOIN public.line_item_type lit on ss.line_item_type_id=lit.line_item_type_id
				JOIN public.product pr on tp.product_id=pr.product_id
				JOIN public.product bpr ON ss.base_product_id = bpr.product_id
				LEFT JOIN (
					SELECT	DISTINCT co.costing_id, co.terminal_id, co.product_category_id, co.costing_item_id, co.costing_value, co.start_date, co.end_date, ci.shipping_status
						FROM costing co
							JOIN costing_item ci USING (costing_item_id)
							JOIN (
								SELECT tp.terminal_id, tp.product_id, ss.base_product_id, bpr.product_category_id
									FROM public.terminal_product tp
										JOIN public.shipping_setup ss USING (terminal_product_id)
										JOIN public.product bpr ON ss.base_product_id = bpr.product_id
									WHERE tp.shipping_status = 1
								) tpss ON co.terminal_id = tpss.terminal_id AND co.product_category_id = tpss.product_category_id
						WHERE co.start_date <='2024-02-01' AND co.end_date >=  '2024-02-01'-- CURRENT_DATE	-- Replace CURRENT_DATE with user defined effective date
							AND co.terminal_id IN (SELECT DISTINCT tp.terminal_id FROM public.terminal_product tp WHERE tp.shipping_status = 1)	-- Get the list of terminals that we can push into Shipping tables
							AND ci.shipping_status = 1 --and co.terminal_id='e5a50489-196c-451d-b089-3f0fd08897ad' and co.product_category_id = '48ea557d-1b8b-4eb6-9337-dba4b41981d3'
				) spin ON tp.terminal_id = spin.terminal_id AND bpr.product_category_id = spin.product_category_id
			WHERE tp.shipping_status = 1 --and tp.terminal_id='e5a50489-196c-451d-b089-3f0fd08897ad'
			GROUP BY tp.terminal_id, tp.product_id, ss.line_item_type_id, ss.base_product_id, ss.line_item_percent, bpr.product_category_id,pr.product_code,bpr.product_code,lit.line_item_type_name
			ORDER BY tp.terminal_id, tp.product_id, ss.line_item_type_id)x
JOIN product bpr ON x.base_product_id = bpr.product_id
JOIN product_category bpc ON bpr.product_category_id = bpc.product_category_id
JOIN line_item_type lit on x.line_item_type_id = lit.line_item_type_id
LEFT JOIN terminal_path_link terpl ON x.terminal_id = terpl.terminal_id AND bpc.product_category_id = terpl.product_category_id
LEFT JOIN shipping_path sp USING (shipping_path_id)
LEFT JOIN spot_market_location_link smll ON sp.shipping_path_origin_id = smll.transportation_location_link_id
LEFT JOIN spot_market sm USING (spot_market_id)
LEFT JOIN spot_index sx ON sm.spot_market_id = sx.spot_market_id AND x.base_product_id = sx.product_id --AND sx.index_component_id = (SELECT index_component_id FROM index_component WHERE index_component_code = 'C')
LEFT JOIN spot_index sxx on x.base_product_id = sxx.product_id --AND sxx.index_component_id = (SELECT index_component_id FROM index_component WHERE index_component_code = 'C')
LEFT JOIN terminal t on x.terminal_id = t.terminal_id
LEFT JOIN terminal_product tp on x.terminal_id = tp.terminal_id and x.product_id = tp.product_id
ORDER BY t.en_terminal_name,x.product_id,x.line_item_type_id
;






---- TRIGGER THE EN COSTING TO EN SHIPPING IN UI PRIOR TO RUNNING THE FOLLOWING QUERIES
---- IF RUNNING FOR MULITPLE PERIODS, BE SURE TO RUN THE SHIPPING_PERIOD AND SHIPPING_LINE_ITEM QUERIES BELOW AND POPULATE THE TEST FILE AFTER EACH TRIGGER


---VERFIY DATA REFLECTING IN SHIPPING_PERIOD AFTER TRIGGER THE EN COSTING TO EN SHIPPING IN UI
---USED TO POPULATE THE "shipping_period after trigger" tab in the EN Costing to EN Shipping test file 

select * from shipping_period order by created_date desc



---VERFIY DATA REFLECTING IN SHIPPING_LINE_ITEM AFTER TRIGGER IN UI
---USED TO POPULATE THE "shippng_line_item after trigger" tab in the EN Costing to EN Shipping test file 

select sli.shipping_line_item_id,tp.terminal_product_id,t.en_terminal_name,tp.terminal_id,tp.product_id,sli.line_item_type_id,sli.base_product_id,bpr.product_code,sli.line_item_percent,bpr.product_category_id
,sli.line_item_adder,lit.line_item_type_name,sli.spot_index_id,sx.spot_index_code
from shipping_line_item sli
left join shipping_period sp using(shipping_period_id)
left join line_item_type lit on lit.line_item_type_id = sli.line_item_type_id
left join terminal t on sp.terminal_id = t.terminal_id
left join terminal_product tp on sp.terminal_id=tp.terminal_id and tp.product_id=sli.product_id
left join product bpr on sli.base_product_id=bpr.product_id
left join spot_index sx on sx.spot_index_id = sli.spot_index_id
ORDER BY t.en_terminal_name,sli.product_id,sli.line_item_type_id



--SEE COSTINGS FOR A SPECIFIED TERMINAL FOR A SPECIFIED PERIOD
select t.en_terminal_name,c.* from costing c
left join terminal t using (terminal_id)
where terminal_id in('9ee4fed2-ff0f-4799-9925-aa205157a7a1','e6937961-3027-40bf-a78b-67bb1db07db2') and start_date <='2023-10-01' AND end_date >=  '2023-10-01'