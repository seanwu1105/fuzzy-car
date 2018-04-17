import math
import operator

import numpy as np


class FuzzySystem(object):
    def __init__(self, consequence, *antecedents):
        self.consequence = consequence
        self.antecedents = antecedents
        self.rules = dict()

    def set_operation_types(self,
                            implication='imp_m',
                            combination_vars='tn_min',
                            combination_rules='tc_max',
                            defuzzifier='gravity_center'):

        if implication == 'imp_dr':
            self.implication = dienes_rescher_imp
        elif implication == 'imp_l':
            self.implication = lukasieweicz_imp
        elif implication == 'imp_z':
            self.implication = zadel_imp
        elif implication == 'imp_g':
            self.implication = godel_imp
        elif implication == 'imp_m':
            self.implication = mandani_imp
        else:  # imp_p
            self.implication = product_imp

        if combination_vars == 'tn_min':
            self.combination_var = min
        elif combination_vars == 'tn_ap':
            self.combination_var = operator.mul
        elif combination_vars == 'tn_bp':
            self.combination_var = bounded_product
        else:  # 'tn_dp'
            self.combination_var = drastic_product

        if combination_rules == 'tc_max':
            self.combination_rule = max
        elif combination_rules == 'tc_as':
            self.combination_rule = algebraic_sum
        elif combination_rules == 'tc_bs':
            self.combination_rule = bounded_sum
        else:  # tc_ds
            self.combination_rule = drastic_sum

        if defuzzifier == 'gravity_center':
            self.defuzzifier = gravity_center_defuzzifier
        elif defuzzifier == 'maxima_mean':
            self.defuzzifier = maxima_mean_defuzzifier
        elif defuzzifier == 'modified_maxima_mean':
            self.defuzzifier = modified_maxima_mean_defuzzifier

    def add_rule(self, consequence_fuzzy_set_name, antecedent_fuzzy_set_names):
        """Add a fuzzy rule.

        Args:
            consequence_fuzzy_set_name (string): One fuzzy set name of
                consequence.
            antecedent_fuzzy_set_names (tuple(string)): A tuple containing
                fuzzy set names for each antecedents in the same sequence of
                `self.antecedents`.

        Raises:
            KeyError: When the name cannot be found in the fuzzy set of
                corresponding variable.
            IndexError: When the # of 'antecedent_fuzzy_set_names' is not equal
                to the 'self.antecedents'.
        """

        if consequence_fuzzy_set_name not in self.consequence.fuzzy_sets.keys():
            raise KeyError("Cannot find '%s' in 'self.consequence'" %
                           consequence_fuzzy_set_name)
        if len(antecedent_fuzzy_set_names) != len(self.antecedents):
            raise IndexError("The # of inputs must be the same with "
                             "'self.antecedents': %d" % len(self.antecedents))
        for name, var in zip(antecedent_fuzzy_set_names, self.antecedents):
            if name not in var.fuzzy_sets.keys():
                raise KeyError("Cannot find '%s' in '%s'" %
                               (name, var.fuzzy_sets.keys()))
        self.rules[antecedent_fuzzy_set_names] = consequence_fuzzy_set_name

    def singleton_result(self, *inputs):
        def combi_var_outs(outs):
            """Calculate the combined-vars result from each variable's
            membership_function(crisp_input) by
            `self.combination_var`.

            Args:
                outs (list(float)): a list contains each variable's
                    membership_function(crisp_input).

            Returns:
                float: the result of combining every variable's crisp output.
            """

            if len(outs) == 2:
                return self.combination_var(outs[0], outs[1])
            return self.combination_var(outs[0], combi_var_outs(outs[1:]))

        def combi_rule_outs(outs):
            """Basically, this is the same as `combi_var_outs`, except that this
            is for combining each rule's crisp output.

            Args:
                outs (list(float)): a list contains each rule's
                    rule_membership_function(crisp_input).

            Returns:
                float: the result of combining every rule's crisp output.
            """

            if len(outs) == 2:
                return self.combination_rule(outs[0], outs[1])
            return self.combination_rule(outs[0], combi_rule_outs(outs[1:]))

        def system_membershipf(crisp_input):
            """Calculate the crisp output according to ALL rules and ALL
            antecedents.

            Args:
                crisp_input (float): the crisp input to the WHOLE fuzzy system.

            Returns:
                float: the crisp output of the WHOLE fuzzy system.
            """

            return combi_rule_outs([f(crisp_input) for f in self.__rule_membershipfs])

        if len(inputs) != len(self.antecedents):
            raise IndexError("The # of inputs must be the same with "
                             "'self.antecedents': %d" % len(self.antecedents))

        self.__rule_membershipfs = []
        # create the membership functions for each rule
        for antecedent_names, consequence_name in self.rules.items():
            antecedent_outs = []
            # get the results from each membership function of antecedent with
            # crisp inputs
            for crisp, var, name in zip(inputs, self.antecedents, antecedent_names):
                # save the results from each membership function of antecedent
                antecedent_outs.append(var.fuzzy_sets[name](crisp))
            # store the membership functions for each rule
            self.__rule_membershipfs.append(
                self.implication(combi_var_outs(antecedent_outs),
                                 self.consequence.fuzzy_sets[consequence_name]))

        # Defuzzify
        return self.defuzzifier(system_membershipf)


class FuzzyVariable(object):
    def __init__(self):
        self.fuzzy_sets = dict()

    def add_membershipf(self, fuzzy_set_name, membershipf):
        self.fuzzy_sets[fuzzy_set_name] = membershipf


def bounded_product(a, b):
    return max(0, a + b - 1)


def drastic_product(a, b):
    if b == 1:
        return a
    if a == 1:
        return b
    return 0


def algebraic_sum(a, b):
    return a + b - a * b


def bounded_sum(a, b):
    return min(1, a + b)


def drastic_sum(a, b):
    if b == 0:
        return a
    if a == 0:
        return b
    return 1


def dienes_rescher_imp(antecedent_out, consequence_membershipf):
    def imp(consequence_crisp):
        return max(1 - antecedent_out, consequence_membershipf(consequence_crisp))
    return imp


def lukasieweicz_imp(antecedent_out, consequence_membershipf):
    def imp(consequence_crisp):
        return min(1, 1 - antecedent_out + consequence_membershipf(consequence_crisp))
    return imp


def zadel_imp(antecedent_out, consequence_membershipf):
    def imp(consequence_crisp):
        return max(min(antecedent_out,
                       consequence_membershipf(consequence_crisp)),
                   1 - antecedent_out)
    return imp


def godel_imp(antecedent_out, consequence_membershipf):
    def imp(consequence_crisp):
        if antecedent_out <= consequence_membershipf(consequence_crisp):
            return 1
        return consequence_membershipf(consequence_crisp) / antecedent_out
    return imp


def mandani_imp(antecedent_out, consequence_membershipf):
    def imp(consequence_crisp):
        return min(antecedent_out, consequence_membershipf(consequence_crisp))
    return imp


def product_imp(antecedent_out, consequence_membershipf):
    def imp(consequence_crisp):
        return operator.mul(antecedent_out, consequence_membershipf(consequence_crisp))
    return imp


def gravity_center_defuzzifier(system_membershipf, support_min=-40, support_max=40):
    support_range = support_max - support_min
    result_fuzzy_area = result_fuzzy_weighted_area = 0
    for crisp in np.linspace(support_min, support_max, support_range * 10, True):
        system_crisp_out = system_membershipf(crisp)
        result_fuzzy_area += system_crisp_out
        result_fuzzy_weighted_area += system_crisp_out * crisp
    if result_fuzzy_area == 0:
        return 0
    return result_fuzzy_weighted_area / result_fuzzy_area


def maxima_mean_defuzzifier(system_membershipf, support_min=-40, support_max=40):
    support_range = support_max - support_min
    support_space = np.linspace(support_min, support_max, support_range * 10, True)
    system_crisp_outs = [system_membershipf(c) for c in support_space]
    max_crisp_out = max(system_crisp_outs)
    max_crisp = [c for c in support_space if system_membershipf(
        c) == max_crisp_out]
    return sum(max_crisp) / len(max_crisp)


def modified_maxima_mean_defuzzifier(system_membershipf, support_min=-40, support_max=40):
    support_range = support_max - support_min
    support_space = np.linspace(support_min, support_max, support_range * 10, True)
    system_crisp_outs = [system_membershipf(c) for c in support_space]
    return (support_space[system_crisp_outs.index(max(system_crisp_outs))]
            - support_space[system_crisp_outs.index(min(system_crisp_outs))]) / 2


def get_gaussianf(mean, sig, ascending, descending):
    def gaussian(var):
        if ascending and var > mean:
            return 1
        if descending and var < mean:
            return 1
        return math.exp(-(var - mean)**2 / sig**2)
    return gaussian
