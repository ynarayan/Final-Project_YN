import ParameterClasses as P
import SimPy.RandomVariantGenerators as RVGs
import SimPy.SamplePathClasses as Path
import SimPy.EconEvalClasses as Econ
import SimPy.StatisticalClasses as Stat


class Patient:
    def __init__(self, id, parameters):
        """ initiates a patient
        :param id: ID of the patient
        :param parameters: an instance of the parameters class
        """
        self.id = id
        self.rng = RVGs.RNG(seed=id)
        self.params = parameters
        self.stateMonitor = PatientStateMonitor(parameters=parameters)

    def simulate(self, n_time_steps):
        """ simulate the patient over the specified simulation length """

        k = 0  # simulation time step

        # while the patient is alive and simulation length is not yet reached
        while self.stateMonitor.get_if_alive() and k < n_time_steps:

            # find the transition probabilities to future states
            trans_probs = self.params.probMatrix[self.stateMonitor.currentState.value]

            # create an empirical distribution
            empirical_dist = RVGs.Empirical(probabilities=trans_probs)

            # sample from the empirical distribution to get a new state
            # (returns an integer from {0, 1, 2, ...})
            new_state_index = empirical_dist.sample(rng=self.rng)

            # update health state
            self.stateMonitor.update(time_step=k, new_state=P.HealthStates(new_state_index))

            # increment time
            k += 1


class PatientStateMonitor:
    """ to update patient outcomes (years survived, cost, etc.) throughout the simulation """
    def __init__(self, parameters):

        self.currentState = parameters.initialHealthState   # initial health state
        self.survivalTime = None      # survival time
        self.numAlive = 0

        # patient's cost and utility monitor
        self.costUtilityMonitor = PatientCostUtilityMonitor(parameters=parameters)

    def update(self, time_step, new_state):
        """
        update the current health state to the new health state
        :param time_step: current time step
        :param new_state: new state
        """

        # if the patient has died, do nothing
        if self.currentState == P.HealthStates.DEATH:
            return

        # update survival time
        if new_state == P.HealthStates.DEATH:
            self.survivalTime = time_step + 0.5  # corrected for the half-cycle effect

        # update cost and utility
        self.costUtilityMonitor.update(k=time_step,
                                       current_state=self.currentState,
                                       next_state=new_state)

        # update current health state
        self.currentState = new_state

    def get_if_alive(self):
        """ returns true if the patient is still alive """
        if self.currentState != P.HealthStates.DEATH:
            # return True
            self.numAlive += 1

        # else:
        #     return False



class PatientCostUtilityMonitor:

    def __init__(self, parameters):

        # model parameters for this patient
        self.params = parameters

        # total cost and utility
        self.totalDiscountedCost = 0
        # self.totalDiscountedUtility = 0

    def update(self, k, current_state, next_state):
        """ updates the discounted total cost and health utility
        :param k: simulation time step
        :param current_state: current health state
        :param next_state: next health state
        """

        # update cost
        cost = 0.5 * (self.params.annualStateCosts[current_state.value] +
                      self.params.annualStateCosts[next_state.value])
        # update utility
        # utility = 0.5 * (self.params.annualStateUtilities[current_state.value] +
        #                  self.params.annualStateUtilities[next_state.value])

        # add the cost of treatment
        # if Chron's death will occur, add the cost for half-year of treatment
        if next_state == P.HealthStates.DEATH:
            cost += 0.5 * self.params.annualTreatmentCost
        else:
            cost += 1 * self.params.annualTreatmentCost

        # update total discounted cost and utility (corrected for the half-cycle effect)
        self.totalDiscountedCost += Econ.pv_single_payment(payment=cost,
                                                           discount_rate=self.params.discountRate / 2,
                                                           discount_period=2 * k + 1)
        # self.totalDiscountedUtility += Econ.pv_single_payment(payment=utility,
        #                                                       discount_rate=self.params.discountRate / 2,
        #                                                       discount_period=2 * k + 1)


class Cohort:
    def __init__(self, id, pop_size, parameters):
        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        :param parameters: parameters
        """
        self.id = id
        self.initialPopSize = pop_size  # initial population size
        self.patients = []  # list of patients
        self.cohortOutcomes = CohortOutcomes()  # outcomes of the this simulated cohort

        # populate the cohort
        for i in range(pop_size):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=id * pop_size + i, parameters=parameters)
            # add the patient to the cohort
            self.patients.append(patient)

    def simulate(self, n_time_steps):
        """ simulate the cohort of patients over the specified number of time-steps
        :param n_time_steps: number of time steps to simulate the cohort
        """
        # simulate all patients
        for patient in self.patients:
            # simulate
            patient.simulate(n_time_steps=n_time_steps)

        # store outputs of this simulation
        self.cohortOutcomes.extract_outcomes(simulated_patients=self.patients)


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []         # patients' survival times
        self.costs = []                 # patients' discounted costs
        # self.utilities =[]              # patients' discounted utilities
        self.nLivingPatients = None  # survival curve (sample path of number of alive patients over time)
        self.numPatientsAlive = []

        self.statSurvivalTime = None    # summary statistics for survival time
        self.statAlive = None
        self.statCost = None            # summary statistics for discounted cost
        self.statUtility = None         # summary statistics for discounted utility

    def extract_outcomes(self, simulated_patients):
        """ extracts outcomes of a simulated cohort
        :param simulated_patients: a list of simulated patients"""

        # record patient outcomes
        for patient in simulated_patients:
            # survival time
            if not (patient.stateMonitor.survivalTime is None):
                self.survivalTimes.append(patient.stateMonitor.survivalTime)

            # discounted cost and number of patients alive
            self.costs.append(patient.stateMonitor.costUtilityMonitor.totalDiscountedCost)
            self.numPatientsAlive.append(patient.stateMonitor.numAlive)
            # self.utilities.append(patient.stateMonitor.costUtilityMonitor.totalDiscountedUtility)

        # summary statistics
        self.statSurvivalTime = Stat.SummaryStat('Survival time', self.survivalTimes)
        self.statCost = Stat.SummaryStat('Discounted cost', self.costs)
        self.statAlive = Stat.SummaryStat('Number of patients alive', self.numPatientsAlive)
        # self.statUtility = Stat.SummaryStat('Discounted utility', self.utilities)

        # survival curve
        self.nLivingPatients = Path.PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size=len(simulated_patients),
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )

