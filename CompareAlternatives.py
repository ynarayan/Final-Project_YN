import InputData as D
import ParameterClasses as P
import MarkovModelClasses as Cls
import Support as Support


# print(Cls.CohortOutcomes.numPatientsAlive)
# simulating amino therapy
# create a cohort
cohort_amino = Cls.Cohort(id=0,
                         pop_size=D.POP_SIZE,
                         parameters=P.ParametersFixed(therapy=P.Therapies.AMINOSALICYLATE))
# simulate the cohort
cohort_amino.simulate(n_time_steps=D.SIM_LENGTH)

# simulating immuno therapy
# create a cohort
cohort_immuno = Cls.Cohort(id=1,
                          pop_size=D.POP_SIZE,
                          parameters=P.ParametersFixed(therapy=P.Therapies.IMMUNOSUPPRESIVE))
# simulate the cohort
cohort_immuno.simulate(n_time_steps=D.SIM_LENGTH)

# print the estimates for the mean survival time and mean time to disease
Support.print_outcomes(sim_outcomes=cohort_amino.cohortOutcomes,
                       therapy_name=P.Therapies.AMINOSALICYLATE)
Support.print_outcomes(sim_outcomes=cohort_immuno.cohortOutcomes,
                       therapy_name=P.Therapies.IMMUNOSUPPRESIVE)

# draw survival curves and histograms
Support.plot_survival_curves_and_histograms(sim_outcomes_amino=cohort_amino.cohortOutcomes,
                                            sim_outcomes_immuno=cohort_immuno.cohortOutcomes)


# print comparative outcomes
Support.print_comparative_outcomes(sim_outcomes_amino=cohort_amino.cohortOutcomes,
                                   sim_outcomes_immuno=cohort_immuno.cohortOutcomes)

# report the CEA results
Support.report_CEA_CBA(sim_outcomes_amino=cohort_amino.cohortOutcomes,
                       sim_outcomes_immuno=cohort_immuno.cohortOutcomes)
