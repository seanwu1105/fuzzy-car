import math
import operator


class FuzzySystem(object):
    def __init__(self, consequence, *antecedents):
        self.consequence = consequence
        self.antecedents = antecedents

    def set_operation_types(self,
                            implication='imp_m',
                            combination_vars='tn_min',
                            combination_rules='tc_max'):

        if implication == 'imp_dr':
            self.implication = dienes_rescher_imp
        elif implication == 'imp_l':
            self.implication = lukasieweicz_imp
        elif implication == 'imp_z':
            self.implication = zadel_imp
        elif implication == 'imp_g':
            self.implication = godel_imp
        elif implication == 'imp_m':
            self.implication = min
        else:  # imp_p
            self.implication = operator.mul

        if combination_vars == 'tn_min':
            self.combination_vars = min
        elif combination_vars == 'tn_ap':
            self.combination_vars = operator.mul
        elif combination_vars == 'tn_bp':
            self.combination_vars = bounded_product
        else:  # 'tn_dp'
            self.combination_vars = drastic_product

        if combination_rules == 'tc_max':
            self.combination_rules = max
        elif combination_rules == 'tc_as':
            self.combination_rules = algebraic_sum
        elif combination_rules == 'tc_bs':
            self.combination_rules = bounded_sum
        else:  # tc_ds
            self.combination_rules = drastic_sum

    def add_rule(self, consequence_fuzzy_set_name, *antecedent__fuzzy_set_names):
        # XXX: Should check and be able to match the name of membership
        # functions for consequnce and antecedents respectively
        print(consequence_fuzzy_set_name)
        print(antecedent__fuzzy_set_names)

    def singleton_result(self, *inputs):
        # XXX: basically, OR(9 rules with AND(2 antecendents))
        pass


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


def dienes_rescher_imp(a, b):
    return max(1 - a, b)


def lukasieweicz_imp(a, b):
    return min(1, 1 - a + b)


def zadel_imp(a, b):
    return max(min(a, b), 1 - a)


def godel_imp(a, b):
    if a <= b:
        return 1
    return b / a


def get_gaussianf(mean, sig, ascending, descending):
    def gaussian(var):
        if ascending and var > mean:
            return 1
        if descending and var < mean:
            return 1
        return math.exp(-(var - mean)**2 / sig**2)
    return gaussian
