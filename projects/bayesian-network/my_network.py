# recursive helper function 
def helper(vars, unknowns, evidence, bn):
	# set current variable and index
	curr = vars.pop(0)
	currind = bn.variable_names.index(curr)

	if curr not in unknowns: 
		result = bn.variables[currind].probability(evidence[curr], evidence)
		# if len makes it possible, recurse
		if len(vars) > 0: 
			result *= helper(vars.copy(), unknowns, evidence, bn)
		return result
	else:
		if len(vars) <= 0:  # base case
			return 1
		else:
			# set up dictionaries
			truedict = evidence.copy()
			truedict[curr] = True

			falsedict = evidence.copy()
			falsedict[curr] = False

			tp = helper(vars.copy(), unknowns, truedict, bn) * bn.variables[currind].probability(True, truedict)
			fp = helper(vars.copy(), unknowns, falsedict, bn) * bn.variables[currind].probability(False, falsedict)

			return (tp + fp)
			

def ask(var, value, evidence, bn):
	# this function is meant to return the probability of hypothesis/model H given evidence E, P(H|E)
	# var is the name of the hypothesis variable
	# value is whether the hypothesis is True or False
	# evidence is the SET of variables known to be True or False
	# bn is the given BayesNet object

	# this function should calculate and return P(H, E) / alpha
		# P(H, E) is the joint probability of the hypothesis (var = value) and the evidence (evidence)
		# alpha is the Normalization constant (the joint probaility of NOT hypothesis and the evidence)

	evcopy = evidence.copy()
	evcopy[var] = value

	#opposites
	evcoppy = evidence.copy()
	evcoppy[var] = not value

	probhe = helper(bn.variable_names.copy(), bn.variable_names - evcopy.keys(), evcopy, bn)
	alpha = helper(bn.variable_names.copy(), bn.variable_names - evcopy.keys(), evcoppy, bn) + probhe

	return (probhe / alpha)