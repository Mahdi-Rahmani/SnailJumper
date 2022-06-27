player_smartness = 3
# top_k natijr behtar
#selection_mode = "roulette_wheel"
selection_mode = "top_k"
parent_selection_mode = "Q_tournament"
#parent_selection_mode = "all"
Q = 5
replace = False
crossover_method = "multi_points_crossover_method2"
#crossover_method = "multi_points"
#crossover_method = "uniform"
n = 2
P_c = 0.7
P_m = 0.3
hyper_parameter = 0.3