-- Compare count and sum of tariff values in the costing and tariff tables
	-- Can use where clauses for terminals and product categories
	-- Ensure all Date and other Where clauses line up across query
SELECT	co.terminal_id, co.product_category_id, ter.en_terminal_name, pc.product_category_code,
		COUNT(co.costing_id) AS costing_count, SUM(co.costing_value) AS costing_value, MAX(co.start_date) AS costing_start, MIN(co.end_date) AS costing_end,
		aa.tariff_count, aa.tariff_cost, aa.tariff_start, aa.tariff_end
	FROM public.costing co
		JOIN public.terminal ter USING (terminal_id)
		JOIN public.product_category pc USING (product_category_id)
		JOIN public.costing_item ci USING (costing_item_id)
		JOIN (
			SELECT DISTINCT co.terminal_id, co.product_category_id, ter.en_terminal_name, pc.product_category_code,
					COUNT(DISTINCT tarpl.tariff_id) AS tariff_count, SUM(DISTINCT tc.tariff_value) AS tariff_cost, MAX(tl.tariff_start_date) AS tariff_start, MIN(tl.tariff_end_date) AS tariff_end
				FROM public.costing co
					JOIN public.terminal ter USING (terminal_id)
					JOIN public.product_category pc USING (product_category_id)
					JOIN public.terminal_path_link terpl ON co.terminal_id = terpl.terminal_id AND co.product_category_id = terpl.product_category_id
					JOIN public.tariff_path_link tarpl ON terpl.shipping_path_id = tarpl.shipping_path_id
					JOIN public.tariff tar ON tarpl.tariff_id = tar.tariff_id
					JOIN public.tariff_cost tc ON tarpl.tariff_id = tc.tariff_id
					JOIN public.tariff_library tl ON tc.tariff_library_id = tl.tariff_library_id
				WHERE tl.tariff_start_date <= '2023-10-01' AND tl.tariff_end_date >= '2023-10-01'
					AND pc.product_category_code IN ('GAS', 'ETH')
					--AND co.terminal_id in ('fbfdc94e-3126-4d49-8545-0ef4687f059f', 'bc75f4d9-7e7a-49c0-858b-58ceb0884376', '5d136db0-82fa-4bf9-b8b3-dc34dcbe5976'
							--			   , 'dd6bec8e-9186-4f77-bb45-68a08da1c2bf', '24f981d4-2747-4ca6-975e-05b138b18b64','14ea70b5-8971-43b4-acc5-67a0dc02885e')
				GROUP BY co.terminal_id, co.product_category_id, ter.en_terminal_name, pc.product_category_code
		)aa USING (terminal_id, product_category_id, en_terminal_name, product_category_code)
	WHERE co.start_date <= '2023-10-01' AND co.end_date >= '2023-10-01'
		AND ci.costing_item_name = 'tariff'
		AND pc.product_category_code IN ('GAS', 'ETH')
		--AND co.terminal_id in ('fbfdc94e-3126-4d49-8545-0ef4687f059f', 'bc75f4d9-7e7a-49c0-858b-58ceb0884376', '5d136db0-82fa-4bf9-b8b3-dc34dcbe5976', 'dd6bec8e-9186-4f77-bb45-68a08da1c2bf'
						--	   , '24f981d4-2747-4ca6-975e-05b138b18b64','14ea70b5-8971-43b4-acc5-67a0dc02885e')
	GROUP BY co.terminal_id, co.product_category_id, ter.en_terminal_name, pc.product_category_code, aa.tariff_count, aa.tariff_cost, aa.tariff_start, aa.tariff_end
	ORDER BY ter.en_terminal_name,pc.product_category_code,aa.tariff_start
;


-- Get costing detail for deep dive
SELECT	co.terminal_id, co.product_category_id, co.costing_id,
		ter.en_terminal_name, pc.product_category_code, co.start_date, co.end_date, co.costing_value, co.created_date, co.modified_date
	FROM public.costing co
		JOIN public.terminal ter USING (terminal_id)
		JOIN public.product_category pc USING (product_category_id)
		JOIN public.costing_item ci USING (costing_item_id)
	WHERE /*co.start_date <= '2024-01-01' AND co.end_date >= '2024-01-01'
		AND */ci.costing_item_name = 'tariff'
		AND pc.product_category_code IN ('GAS', 'ETH')
		--AND co.terminal_id in('14ea70b5-8971-43b4-acc5-67a0dc02885e')
;


-- Get tariff detail for deep dive
SELECT	DISTINCT co.terminal_id, co.product_category_id, terpl.terminal_path_link_id, tarpl.tariff_path_link_id, tarpl.tariff_id, tc.tariff_cost_id, tl.tariff_library_id,
		ter.en_terminal_name, pc.product_category_code, tar.tariff_code, tl.tariff_start_date, tl.tariff_end_date, tc.tariff_value, tl.created_date, tl.modified_date
	FROM public.costing co
		JOIN public.terminal ter USING (terminal_id)
		JOIN public.product_category pc USING (product_category_id)
		JOIN public.terminal_path_link terpl ON co.terminal_id = terpl.terminal_id AND co.product_category_id = terpl.product_category_id
		JOIN public.tariff_path_link tarpl ON terpl.shipping_path_id = tarpl.shipping_path_id
		JOIN public.tariff tar ON tarpl.tariff_id = tar.tariff_id
		JOIN public.tariff_cost tc ON tarpl.tariff_id = tc.tariff_id
		JOIN public.tariff_library tl ON tc.tariff_library_id = tl.tariff_library_id
	WHERE /*tl.tariff_start_date <= '2024-01-01' AND tl.tariff_end_date >= '2024-01-01'
		AND */pc.product_category_code IN ('GAS', 'ETH')
		AND co.terminal_id in('14ea70b5-8971-43b4-acc5-67a0dc02885e')
;




-- Other queries that we used to get to the queries above
	-- may be helpful if above queries don't answer questions

select distinct co.terminal_id,t.en_terminal_name,pc.product_category_code,co.costing_id,ci.costing_item_name,co.start_date,co.end_date,co.costing_value,tl.tariff_library_code,tl.tariff_start_date,tl.tariff_end_date
from costing co
join costing_item ci using(costing_item_id)
join product_category pc using(product_category_id)
left join terminal t on co.terminal_id = t.terminal_id
left join terminal_path_link tpl on co.terminal_id=tpl.terminal_id
left join tariff_path_link tpll on tpl.shipping_path_id = tpll.shipping_path_id
left join tariff_cost tc on tpll.tariff_id = tc.tariff_id
join tariff_library tl on tc.tariff_library_id = tl.tariff_library_id  --and co.start_date = tl.tariff_start_date and co.end_date = tl.tariff_end_date
where co.terminal_id in('5d136db0-82fa-4bf9-b8b3-dc34dcbe5976')
and co.start_date <= '2024-01-01' AND co.end_date >= '2024-01-01' and pc.product_category_code <>'DSL' and ci.costing_item_name = 'tariff'
order by co.terminal_id,pc.product_category_code,ci.costing_item_name,co.end_date desc



-- Get count and sum of tariffs in the costing table by terminal and product category
SELECT co.terminal_id, co.product_category_id, ter.en_terminal_name, pc.product_category_code, COUNT(co.costing_id), SUM(co.costing_value), MAX(co.start_date), MIN(co.end_date)
	FROM public.costing co
		JOIN public.terminal ter USING (terminal_id)
		JOIN public.product_category pc USING (product_category_id)
		JOIN public.costing_item ci USING (costing_item_id)
	WHERE co.start_date <= '2024-01-01' AND co.end_date >= '2024-01-01'
		AND ci.costing_item_name = 'tariff'
		AND pc.product_category_code IN ('GAS', 'ETH')
		AND co.terminal_id in('fbfdc94e-3126-4d49-8545-0ef4687f059f')
	GROUP BY co.terminal_id, co.product_category_id, ter.en_terminal_name, pc.product_category_code
;

-- Get count and sum of tariffs based on path & tariffs by terminal and product category
SELECT DISTINCT co.terminal_id, co.product_category_id, ter.en_terminal_name, pc.product_category_code, COUNT(DISTINCT tarpl.tariff_id), SUM(DISTINCT tc.tariff_value), MAX(tl.tariff_start_date), MIN(tl.tariff_end_date)
	FROM public.costing co
		JOIN public.terminal ter USING (terminal_id)
		JOIN public.product_category pc USING (product_category_id)
		JOIN public.terminal_path_link terpl ON co.terminal_id = terpl.terminal_id AND co.product_category_id = terpl.product_category_id
		JOIN public.tariff_path_link tarpl ON terpl.shipping_path_id = tarpl.shipping_path_id
		JOIN public.tariff tar ON tarpl.tariff_id = tar.tariff_id
		JOIN public.tariff_cost tc ON tarpl.tariff_id = tc.tariff_id
		JOIN public.tariff_library tl ON tc.tariff_library_id = tl.tariff_library_id
	WHERE tl.tariff_start_date <= '2024-01-01' AND tl.tariff_end_date >= '2024-01-01'
		AND pc.product_category_code IN ('GAS', 'ETH')
		AND co.terminal_id in('fbfdc94e-3126-4d49-8545-0ef4687f059f')
	GROUP BY co.terminal_id, co.product_category_id, ter.en_terminal_name, pc.product_category_code
;




select * from terminal_product where terminal_id in('e65514d2-bfb7-42e2-882d-f5b0e2e8bdc0','5fcf004f-11fe-451f-8b41-3948ea8be642','5a9d44e8-8be4-4411-9436-2e2601b06dd3','6241b98a-7ced-451e-8186-b944f2298a32','a9171ce7-90c2-41cd-a897-20bba8ed1cd1')


