from enum import Enum
import numpy as np
import InputData as Data


class HealthStates(Enum):
    """ health states of patients with HIV """
    REMISSION = 0
    MILD = 1
    DRUG_RESPONSIVE = 2
    DRUG_DEPENDENT = 3
    DRUG_REFRACTORY = 4
    SURGERY = 5
    POST_SURGERY_REMISSION = 6
    DEATH = 7


class Therapies(Enum):
    """ amino vs. immuno therapy """
    AMINOSALICYLATE = 0
    IMMUNOSUPPRESIVE = 1


class ParametersFixed:
    def __init__(self, therapy):

        # selected therapy
        self.therapy = therapy

        # initial health state
        self.initialHealthState = HealthStates.REMISSION

        # annual treatment cost
        if self.therapy == Therapies.AMINOSALICYLATE:
            self.annualTreatmentCost = Data.Aminosalicylate_COST
        else:
            self.annualTreatmentCost = Data.Aminosalicylate_COST + Data.Immunosuppresive_COST

        # transition probability matrix of the selected therapy
        self.probMatrix = []

        # calculate transition probabilities between treatment states
        if self.therapy == Therapies.AMINOSALICYLATE:
            # calculate transition probability matrix for the amino therapy
            self.probMatrix = Data.TRANS_MATRIX

        else:
            self.probMatrix = Data.TRANS_MATRIX

        # annual state costs and utilities
        self.annualStateCosts = Data.ANNUAL_STATE_COST
        # self.annualStateUtilities = Data.ANNUAL_STATE_UTILITY

        # discount rate
        self.discountRate = Data.DISCOUNT


# do i even need these matrices??
# def get_prob_matrix_amino(trans_matrix):
#     """
#     :param trans_matrix: transition matrix containing counts of transitions between states
#     :return: transition probability matrix
#     """
#
#     # initialize transition probability matrix
#     trans_prob_matrix = []
#
#     # for each row in the transition matrix
#     for row in trans_matrix:
#         # calculate the transition probabilities
#         prob_row = np.array(row)/sum(row)
#         # add this row of transition probabilities to the transition probability matrix
#         trans_prob_matrix.append(prob_row)
#
#     return trans_prob_matrix
#
#
# def get_prob_matrix_immuno(prob_matrix_amino, combo_rr):
#     """
#     :param prob_matrix_mono: (list of lists) transition probability matrix under mono therapy
#     :param combo_rr: relative risk of the combination treatment
#     :returns (list of lists) transition probability matrix under combination therapy """
#
#     # create an empty list of lists
#     matrix_immuno = []
#     for row in prob_matrix_amino:
#         matrix_immuno.append(np.zeros(len(row)))  # adding a row [0, 0, 0]
#
#     # populate the combo matrix
#     # calculate the effect of combo-therapy on non-diagonal elements
#     for s in range(len(matrix_immuno)):
#         for next_s in range(s + 1, len(HealthStates)):
#             matrix_immuno[s][next_s] = combo_rr * prob_matrix_amino[s][next_s]
#
#     # diagonal elements are calculated to make sure the sum of each row is 1
#     for s in range(len(matrix_immuno)):
#         matrix_immuno[s][s] = 1 - sum(matrix_immuno[s][s+1:])
#
#     return matrix_immuno


# # tests
# matrix_mono = get_prob_matrix_mono(Data.TRANS_MATRIX)
# matrix_combo = get_prob_matrix_combo(matrix_mono, Data.TREATMENT_RR)
#
# print(matrix_mono)
# print(matrix_combo)
