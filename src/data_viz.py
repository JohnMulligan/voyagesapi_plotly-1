#formerly graphs.py

scatter_plot_x_vars=[
	'voyage_dates__imp_arrival_at_port_of_dis_year',
	'voyage_dates__length_middle_passage_days',
	'voyage_dates__imp_length_home_to_disembark',
	'voyage_crew__crew_voyage_outset',
	'voyage_crew__crew_first_landing',
	'voyage_slaves_numbers__imp_total_num_slaves_embarked',
	'voyage_slaves_numbers__imp_total_num_slaves_disembarked'
]

scatter_plot_y_vars=[
	'voyage_dates__imp_length_home_to_disembark',
	'voyage_dates__length_middle_passage_days',
	'voyage_ship__tonnage_mod',
	'voyage_crew__crew_voyage_outset',
	'voyage_crew__crew_first_landing',
	'voyage_slaves_numbers__imp_total_num_slaves_embarked',
	'voyage_slaves_numbers__imp_total_num_slaves_disembarked',
	'voyage_slaves_numbers__percentage_men',
	'voyage_slaves_numbers__percentage_women',
	'voyage_slaves_numbers__percentage_boy',
	'voyage_slaves_numbers__percentage_girl',
	'voyage_slaves_numbers__percentage_male',
	'voyage_slaves_numbers__percentage_child',
	'voyage_slaves_numbers__percentage_adult',
	'voyage_slaves_numbers__percentage_female',
	'voyage_slaves_numbers__imp_mortality_ratio',
	'voyage_slaves_numbers__imp_jamaican_cash_price'
]

scatter_plot_factors = [
	'voyage_ship__imputed_nationality',
	'voyage_itinerary__imp_port_voyage_begin',
	'voyage_ship__imputed_nationality'
]