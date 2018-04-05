import operator


class FuzzySystem(object):
    def __init__(self):
        pass

    def set_operation_types(self,
                            composition_tnorm='tn_min',
                            composition_tconorm='tc_max',
                            implication='imp_m',
                            combination_vars='tn_min',
                            combination_rules='tc_max'):

        self.composition_tnorm = self.get_fuzzyset_op(composition_tnorm)
        self.composition_tconorm = self.get_fuzzyset_op(composition_tconorm)
        self.combination_vars = self.get_fuzzyset_op(combination_vars)
        self.combination_rules = self.get_fuzzyset_op(combination_rules)

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
            self.composition_tnorm = operator.mul

    @staticmethod
    def get_fuzzyset_op(type_name):
        if type_name == 'tn_min':
            return min
        if type_name == 'tn_ap':
            return operator.mul
        if type_name == 'tn_bp':
            return bounded_product
        if type_name == 'tn_dp':
            return drastic_product
        if type_name == 'tc_max':
            return max
        if type_name == 'tc_as':
            return algebraic_sum
        if type_name == 'tc_bs':
            return bounded_sum
        return drastic_sum


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
