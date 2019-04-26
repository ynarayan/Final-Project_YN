
# simulation settings
POP_SIZE = 1000     # cohort population size
SIM_LENGTH = 2/12   # length of simulation (years). this is 2 months
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.05     # annual discount rate
# annual probability of background mortality (number per year per 1,000 population)
ANNUAL_PROB_BACKGROUND_MORT = 1.6/100   # according to https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1856159/

# transition matrix
TRANS_MATRIX = [
    [0.89688, 0.07016, 0.00939, 0.00639, 0.00363, 0.00793, 0.00395, 0.00167],   # Remission
    [0.05751, 0.90952, 0.00829, 0.00619, 0.00968, 0.00585, 0.00281, 0.00015],   # Mild
    [0.25261, 0.22170, 0.41262, 0.02563, 0.00817, 0.04569, 0.02733, 0.00626],   # Drug-responsive
    [0.05274, 0.03484, 0.00193, 0.88626, 0.00592, 0.01071, 0.00543, 0.00217],   # drug-dependent
    [0.06174, 0.05888, 0.00392, 0.02599, 0.74207, 0.06435, 0.03466, 0.00839],   # drug-refractory
    [0.00657, 0.06906, 0.00801, 0.03421, 0.02397, 0.33714, 0.52022, 0.00082],   # surgery
    [0.00054, 0.00849, 0.00100, 0.00152, 0.00096, 0.00436, 0.98126, 0.00187],   # post surgery remission
    [0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000],   # Death
    ]

# annual cost of each health state
ANNUAL_STATE_COST = [
    4849,     # Remission
    11467,    # Mild
    1147,     # drug-responsive
    1938,     # drug-dependent
    2062,     # drug-refractory
    17526,    # surgery
    916,      # post-surgery remission
    0,        # death
    ]

# # annual health utility of each health state
# ANNUAL_STATE_UTILITY = [
#     0.75,   # CD4_200to500
#     0.50,   # CD4_200
#     0.25,   # AIDS
#     0,      # Dead
#     ]

# annual therapy costs
Aminosalicylate_COST = 11467
Immunosuppresive_COST = 5147

# # treatment relative risk
# TREATMENT_RR = 0.509



