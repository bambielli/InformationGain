
from math import log

# returns total postive values and total values in a tuple from a list of values
# values = [(pos, neg)]
def lam(acc, value):
    acc[0] += value[0]
    acc[1] += value[0] + value[1]
    return acc

def totals(values):
    return reduce(lam, values, [0,0])

def remainder(values, total):
    transform = [((pos + neg) / float(total)) * entropy(pos, pos + neg) for pos, neg in values]
    return sum(transform)

# This calculates information entropy for a value Q
# Equation is as follows:
# B(q) = -qlog2(q) - (1-q)log2(1-q)
# q = quantity desired_results/total number of results
def entropy (pos, total):
    q_val = pos / float(total)
    print "positive is: {0}".format(pos)
    print "total is: {0}".format(total)
    if q_val == 1 or q_val == 0:
        # in this case, the log(1-q_val) would return a domain error.
        # if q_val is 1, we should just return 0.
        return 0
    else:
        return -q_val*log(q_val, 2) - (1-q_val) * log((1-q_val), 2)


class entropy_calculator:
    attributes = {}
    def __init__(self, attributes):
        # dictionary of attributes and an array of the pos / neg values for each of their branches
        # e.g. {"outlook": [(2, 3), (4, 0), (3, 2)]}
        self.attributes = attributes

    # remainder calculates the remainder of entropy after
    # information gain provided
    # values = [(posk, negk),...]
    def gains(self):
        return_dict = {}
        for k, v in self.attributes.items():
            total_pos, total = totals(v)
            total_e = entropy(total_pos, total)
            rem = remainder(v, total)
            import pdb
            pdb.set_trace()
            return_dict[k] = total_e - rem

        return return_dict

attributes_A = {"A": [(3, 1), (0, 2)], "B": [(1, 3), (2, 0)], "C": [(2, 0), (0, 2), (1, 1)]}
# attributes_B = {"A": [(1, 3), (0, 2)], "B": [(1, 3), (0, 2)], "C": [(0, 2), (1, 1), (0, 2)]}
# attributes_C = {"A": [(0, 4), (2, 0)], "B": [(2, 2), (0, 2)], "C": [(0, 2), (1, 1), (1, 1)]}


ec_A = entropy_calculator(attributes_A)
# ec_B = entropy_calculator(attributes_B)
# ec_C = entropy_calculator(attributes_C)

print ec_A.gains()
# print ec_B.gains()
# print ec_C.gains()