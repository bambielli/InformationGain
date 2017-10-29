from math import log

def total(values):
    """
    arguments:
    values -> array or tuple of numbers
    return:
    sum of the values from the argument array
    """
    # something like (1, 2). output is a single number, total sum
    return sum(values)

def entropy (vals):
    """
    Entropy for a decision. The average amount of information encoded by this branch.
    Total entropy is calculated by passing in the sum of goal states as a single tuple.

    arguments:
    vals - tuple, where each number represents a goal state classified by a branch of a decision

    return:
    e - entropy for the given branch
    """
    t = total(vals)
    e = 0 # 0 is returned by default if all vals are 0
    for val in vals:
        if val != 0:
            e -= (val / float(t))*log(val / float(t), 2)
    return e

def construct_total_tuple(values):
    """
    Takes a tuple, and adds all positions together.
    This represents the total number of values in the data set
    values - [(0, 1, 1) (1, 2, 1) (0, 2, 3)]
    Return - (1, 5, 5)
    """
    # *values tells zip to "unzip" what was provided
    # e.g. zip(*[(0, 1, 1) (1, 2, 1) (0, 2, 3)]) --> [(0, 1, 0) (1, 2, 2) (1, 1, 3)]
    return tuple(map(sum, zip(*values)))

class InformationGain:

    def __init__(self, attributes):
        """
        Constructs an instance of entropy_calculator

        aruguments:
        attributes - dict() values: [(),...]: Dictionary that represents decision attributes (keys) and the goal state values

        e.g. attributes = {"Outlook": [(2, 3), (4, 0), (3, 2)], "Temp": [(2, 2), (4, 2), (3, 1)], "Humidity": [(3, 4), (6, 1)], "Wind": [(6, 2), (3, 3)]}
        Outlook decision has 3 branches: sunny (2 yes, 3 no), overcast (4 yes, 0 no), rainy (3 yes, 2 no)
        If there are more than 3 goal states (i.e. Yes, No, and Maybe) all tuples should be of length 3.
        If there are no entries of one of the goal states in a particular branch, just leave it as 0.
        """
        self.attributes = attributes
        vals = attributes.values()[0]
        self.total_tuple = construct_total_tuple(vals)
        self.total_entries = total(self.total_tuple)

    def __entropy_remainder(self, branches):
        """
        Calculates the entropy remainder from each branch.

        arguments:
        self - class instance
        branches [(),()] - the branches for a decision, with goal values formatted as array of tuples

        return:
        full_remainder -the amount of information encoded in this decision (smaller is better)
        """
        full_remainder = 0
        for branch in branches:
            rem = [(float(value) / self.total_entries) * entropy(branch) for value in branch]
            full_remainder += sum(rem)
        print "fullremainder is: {0}".format(full_remainder)
        return full_remainder


    def entropy_gain(self):
        """
        return the total amount of information gain for each attribute in the calculator
        Also referred to the toal reduction in entropy.
        Calculated by taking the total entropy, and subtracting the sum of the remainders for each decision branch in an attribute

        return:
        return_dict: dictionary of attribute keys and the amount of information encoded by each (larger is better)
        """
        return_dict = {}
        total_e = entropy(self.total_tuple)
        print total_e
        for k, v in self.attributes.items():
            rem = self.__entropy_remainder(v)
            return_dict[k] = total_e - rem
        return return_dict

    def gini_impurity(self, class_vector):
        """Compute the gini impurity for a list of classes.
        This is a measure of how often a randomly chosen element
        drawn from the class_vector would be incorrectly labeled
        if it was randomly labeled according to the distribution
        of the labels in the class_vector.
        It reaches its minimum at zero when all elements of class_vector
        belong to the same class.

        Args:
            class_vector (list(int)): Vector of classes given as 0 or 1.

        Returns:
            Floating point number representing the gini impurity.
        """
        classes = dict()
        for val in class_vector:
            if not classes.has_key(val):
                classes[val] = 1
            else:
                classes[val] += 1
        impurity = 0
        for k, v in classes.iteritems():
            positive = float(v) / len(class_vector)
            negative = 1 - positive
            impurity += (positive * negative)

        return impurity


    def gini_gain(self, previous_classes, current_classes):
        """Compute the gini impurity gain between the previous and current classes.
        Args:
            previous_classes (list(int)): Vector of classes given as 0 or 1.
            current_classes (list(list(int): A list of lists where each list has
                0 and 1 values).
        Returns:
            Floating point number representing the information gain.
        """
        total_impurity = self.gini_impurity(previous_classes)
        total_remainder = 0
        for branch in current_classes:
            gi_branch = self.gini_impurity(branch)
            # weighted sum of gini_impurity for each branch
            total_remainder += gi_branch * (len(branch) / len(previous_classes))

        return total_impurity - total_remainder

# See https://www.youtube.com/watch?time_continue=1&v=FgUaM-98LDI for example data table.
# See https://www.youtube.com/watch?time_continue=1&v=VvXzh-CHCc8 for answer and calculations.
# Note that calculations in the answer above are using a shortcut for calculating entropy that is applicable when there
# are 2 goal states. This code will work for more than 1 goal state.

attributes = {"A1": [(3, 2), (0, 3)], "A2": [(1, 3), (2, 2)], "A3": [(1, 3), (2, 2)], "A4": [(2, 2), (1, 3)]}
previous_classes = [0, 0, 0, 1, 1, 1, 1, 1]
current_classes_a1 = [[0, 0, 0, 1, 1], [1, 1, 1]]
current_classes_a2 = [[0, 1, 1, 1], [0, 0, 1, 1]]
current_classes_a3 = [[0, 1, 1, 1], [0, 0, 1, 1]]
current_classes_a4 = [[0, 0, 1, 1], [0, 1, 1, 1]]


ig = InformationGain(attributes)

gini_impurity_gain = {"A1": ig.gini_gain(previous_classes, current_classes_a1), "A2": ig.gini_gain(previous_classes, current_classes_a2), "A3": ig.gini_gain(previous_classes, current_classes_a3), "A4": ig.gini_gain(previous_classes, current_classes_a4)}

print "entropy gain is: {0}".format(ig.entropy_gain())
print "impurity gain is: {0}".format(gini_impurity_gain)
