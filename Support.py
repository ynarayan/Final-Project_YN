import InputData as D
import SimPy.SamplePathClasses as PathCls
import SimPy.FigureSupport as Figs
import SimPy.StatisticalClasses as Stat
import SimPy.EconEvalClasses as Econ
import matplotlib.pyplot as plt


def print_outcomes(sim_outcomes, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param sim_outcomes: outcomes of a simulated cohort
    :param therapy_name: the name of the selected therapy
    """
    # mean and confidence interval of patient survival time
    survival_mean_CI_text = sim_outcomes.statSurvivalTime\
        .get_formatted_mean_and_interval(interval_type='c',
                                         alpha=D.ALPHA,
                                         deci=2)

    # mean and confidence interval text of discounted total cost
    cost_mean_CI_text = sim_outcomes.statCost\
        .get_formatted_mean_and_interval(interval_type='c',
                                         alpha=D.ALPHA,
                                         deci=0,
                                         form=',')

    # mean and confidence interval text of discounted total utility
    # utility_mean_CI_text = sim_outcomes.statUtility\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)

    # print outcomes
    print(therapy_name)
    print("  Estimate of mean survival time and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
          survival_mean_CI_text)
    print("  Estimate of discounted cost and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
          cost_mean_CI_text)
    # print("  Estimate of discounted utility and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       utility_mean_CI_text)
    print("")


def plot_survival_curves_and_histograms(sim_outcomes_amino, sim_outcomes_immuno):
    """ draws the survival curves and the histograms of time until Chron's
    :param sim_outcomes_amino: outcomes of a cohort simulated under mono therapy
    :param sim_outcomes_immuno: outcomes of a cohort simulated under combination therapy
    """

    # get survival curves of both treatments
    survival_curves = [
        sim_outcomes_amino.nLivingPatients,
        sim_outcomes_immuno.nLivingPatients
    ]

    # graph survival curve
    PathCls.graph_sample_paths(
        sample_paths=survival_curves,
        title='Survival curve',
        x_label='Simulation time step (year)',
        y_label='Number of alive patients',
        legends=['Aminosalicylate Therapy', 'Immunosuppresive Therapy']
    )

    # histograms of survival times
    set_of_survival_times = [
        sim_outcomes_amino.survivalTimes,
        sim_outcomes_immuno.survivalTimes
    ]

    # graph histograms
    Figs.graph_histograms(
        data_sets=set_of_survival_times,
        title='Histogram of patient survival time',
        x_label='Survival time (year)',
        y_label='Counts',
        bin_width=1,
        legends=['Aminosalicylate Therapy', 'Immunosuppresive Therapy'],
        transparency=0.6
    )


def print_comparative_outcomes(sim_outcomes_amino, sim_outcomes_immuno):
    """ prints average increase in survival time, discounted cost, and discounted utility
    under immunosuppresive therapy compared to aminosalicylate therapy
    :param sim_outcomes_amino: outcomes of a cohort simulated under mono therapy
    :param sim_outcomes_immuno: outcomes of a cohort simulated under combination therapy
    """

    # increase in mean survival time under immuno therapy with respect to amino therapy
    increase_survival_time = Stat.DifferenceStatIndp(
        name='Increase in mean survival time',
        x=sim_outcomes_immuno.survivalTimes,
        y_ref=sim_outcomes_amino.survivalTimes)

    # estimate and CI
    estimate_CI = increase_survival_time.get_formatted_mean_and_interval(interval_type='c',
                                                                         alpha=D.ALPHA,
                                                                         deci=2)
    print("Increase in mean survival time and {:.{prec}%} confidence interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_CI)

    # increase in mean discounted cost under immuno therapy with respect to amino therapy
    increase_discounted_cost = Stat.DifferenceStatIndp(
        name='Increase in mean discounted cost',
        x=sim_outcomes_immuno.costs,
        y_ref=sim_outcomes_amino.costs)

    # estimate and CI
    estimate_CI = increase_discounted_cost.get_formatted_mean_and_interval(interval_type='c',
                                                                           alpha=D.ALPHA,
                                                                           deci=2,
                                                                           form=',')
    print("Increase in mean discounted cost and {:.{prec}%} confidence interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_CI)
    #
    # increase in number of patients alive under immuno therapy with respect to amino therapy
    increase_patients_alive = Stat.DifferenceStatIndp(
        name='Increase in mean number of patients alive',
        x=sim_outcomes_immuno.numPatientsAlive,
        y_ref=sim_outcomes_amino.numPatientsAlive)

    # estimate and CI
    estimate_CI = increase_patients_alive.get_formatted_mean_and_interval(interval_type='c',
                                                                              alpha=D.ALPHA,
                                                                               deci=2)
    print("Increase in mean number of patients alive and {:.{prec}%} confidence interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_CI)


def report_CEA_CBA(sim_outcomes_amino, sim_outcomes_immuno):
    """ performs cost-effectiveness and cost-benefit analyses
    :param sim_outcomes_amino: outcomes of a cohort simulated under aminosalicylate therapy
    :param sim_outcomes_immuno: outcomes of a cohort simulated under immunosuppresive therapy
    """

    # define two strategies
    amino_therapy_strategy = Econ.Strategy(
        name='Aminosalicylate Therapy',
        cost_obs=sim_outcomes_amino.costs,
        effect_obs=sim_outcomes_amino.numPatientsAlive,
        color='green'
    )
    immuno_therapy_strategy = Econ.Strategy(
        name='Immunosuppresive Therapy',
        cost_obs=sim_outcomes_immuno.costs,
        effect_obs=sim_outcomes_immuno.numPatientsAlive,
        color='blue'
    )

    # do CEA
    CEA = Econ.CEA(
        strategies=[amino_therapy_strategy, immuno_therapy_strategy],
        if_paired=False
    )

    # show the cost-effectiveness plane
    show_ce_figure(CEA=CEA)

    # report the CE table
    CEA.build_CE_table(
        interval_type='c',
        alpha=D.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2)

    # CBA
    NBA = Econ.CBA(
        strategies=[amino_therapy_strategy, immuno_therapy_strategy],
        if_paired=False
    )
    # show the net monetary benefit figure
    NBA.graph_incremental_NMBs(
        min_wtp=0,
        max_wtp=50000,
        title='Cost-Benefit Analysis',
        x_label='Willingness-to-pay for one additional QALY ($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval_type='c',
        show_legend=True,
        figure_size=(6, 5)
    )


def show_ce_figure(CEA):

    # create a cost-effectiveness plot
    plt.figure(figsize=(5, 5))

    # find the frontier (x, y)'s
    frontier_utilities = []
    frontier_costs = []
    for s in CEA.get_shifted_strategies_on_frontier():
        frontier_utilities.append(s.aveEffect)
        frontier_costs.append(s.aveCost)

    # draw the frontier line
    plt.plot(frontier_utilities, frontier_costs,
             c='k',  # color
             alpha=0.6,  # transparency
             linewidth=2,  # line width
             label="Frontier")  # label to show in the legend

    # add the strategies
    for s in CEA.get_shifted_strategies():
        # add the center of the cloud
        plt.scatter(s.aveEffect, s.aveCost,
                    c=s.color,      # color
                    alpha=1,        # transparency
                    marker='o',     # markers
                    s=75,          # marker size
                    label=s.name    # name to show in the legend
                    )

    plt.legend()        # show the legend
    plt.axhline(y=0, c='k', linewidth=0.5)  # horizontal line at y = 0
    plt.axvline(x=0, c='k', linewidth=0.5)  # vertical line at x = 0
    plt.xlim([-2.5, 10])              # x-axis range
    plt.ylim([-50000, 200000])     # y-axis range
    plt.title('Cost-Effectiveness Analysis')
    plt.xlabel('Additional number of patients alive')
    plt.ylabel('Additional discounted cost')
    plt.show()

