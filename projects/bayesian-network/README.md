# Bayes Nets

## Context

Bayes Nets allow us to reason with uncertainty (aka with imperfect information/uncertain axioms about the world).

Bayes Nets let us reason about the probability of a particular hypothesis being true given a set of evidence.

We reason about hypotheses (whether or not they hold) given evidence, and for Bayes Nets
in particular, this manifests as questions like, "What is the probability that it isn't
raining given that the grass is wet and it's cloudy?"

## The Network

In `my_network.py`, the `ask` function returns the probability of a hypothesis/model given some evidence: $P(H|E)$. 

The function takes four arguments:

* `var` is the name of the hyptothesis variable.
* `value` indicates whether the hypothesis being asked about is `True` or `False`.
* `evidence` is the set of variables known to be `True` or `False`.
* `bn` is the `BayesNet` (in the provided module) pertaining to the problem.

To calculate $P(H|E)$, `ask` should calculate and return $\frac{P(H,E)}{\alpha}$, where:

* $P(H,E)$ is the joint probability of the hypothesis (`var` = `value`) and the
  evidence (`evidence`), and

* $\alpha$ is the Normalization Constant (the joint probability of the hypothesis and the
  evidence plus the joint probability of $\neg$hypothesis and the
  evidence). 

## Notes

### On Joint Probability

To calculate the joint probability, we can break things down into terms that we can just lookup in the `BayesNet`.  For example, if we don't have $P(b,e,a)$, but we do have $P(b)$, $P(e)$, and $P(a|b,e)$, then  we can handle this recursively by recognizing the following:
	$P(b,e,a) = P(b) P(e,a|b)$ (This is called the Chain Rule.).
Similarly, we know that $P(e,a|b) = P(e|b) P(a|b,e)$.

When calculating the joint probability, we need to include all the variables that may influence the final result.  This includes all the variables that are parents of the variables in the call to `ask`.

To get the list of variables in order and to get the whole list of variables, use `BayesNet.variables`.

### Variables and known values

In code, we represent the values of variables as a dictionary keyed on the _name_ of the variable.  The value of the dictionary entry is either `True` or `False`. 

An example:

```
{
  'Alarm': True, 'Burglar': False, 'Earthquake': False,
  'JohnCalls': False, 'MaryCalls': False
}
```

This representation is used for the `evidence` argument in the call to `ask`.


### On The Normalization Constant

The Normalization Constant is the sum of: (1) the joint probability of the hypothesis and the evidence and (2) the joint probability of _not_ the hypothesis and the evidence. For
example, the Normalization Constant $\alpha$ for $P(a|b)$ is: $$\alpha = P(a,b) + P(\neg a,b)$$


### On the BayesNet Module

In the `BayesNet` class, the `variables` field is an iterator of all of the variables in the net.

Each variable in a `BayesNet` is an instance of `BayesNode`, of which the most important
fields are `name` and `evidence`.  You will also need to use the `probability` function to look up probabilities in the CPT.