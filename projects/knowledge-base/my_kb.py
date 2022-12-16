from colorsys import rgb_to_hsv
from email.headerregistry import ParameterizedMIMEHeader
import fractions
from operator import rshift
from ssl import CHANNEL_BINDING_TYPES
import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact or Rule) - Fact or Rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact_rule):
        """Retract a fact or a rule from the KB

        Args:
            fact_rule (Fact or Rule) - Fact or Rule to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact_rule])
        ####################################################
        # If fact_rule has no support: remove it and adjust supported_by, supported_facts, supported_rules
        # If fact_rule is asserted and has support: unassert it
        # Else: do nothing

        if factq(fact_rule): # if we have a fact
            for fact in self.facts: # search all facts in KB
                if fact == fact_rule and not fact.supported_by: # if fact has no support
                     # remove the fact
                    self.facts.remove(fact) 

                    # adjust facts it supports
                    for supportedfact in fact.supports_facts: 
                        for list in supportedfact.supported_by: # the items in supported_by are [fact, rule] lists
                            if fact in list:
                                supportedfact.supported_by.remove(list)
                                # lists containing the retracted fact no longer support the supportedfact 
                        # call retract recursively -- if our supportedfact no longer has support, it will be retracted
                        self.kb_retract(supportedfact) 

                    # adjust rules it supports
                    for supportedrule in fact.supports_rules:
                        for list in supportedrule.supported_by: 
                            if fact in list:
                                supportedrule.supported_by.remove(list)
                        self.kb_retract(supportedrule) 

                elif fact == fact_rule and fact.supported_by: # if our fact has support
                    if fact.asserted: #if the fact is asserted, unassert it
                        fact.asserted = False 
        
        else: # if we have a rule
            for rule in self.rules:
                if rule == fact_rule and not rule.supported_by: 
                    # remove the rule
                    self.rules.remove(rule) 

                    # adjust facts it supports
                    for supportedfact in rule.supports_facts: 
                        for list in supportedfact.supported_by:
                            if rule in list:
                                supportedfact.supported_by.remove(list)
                        self.kb_retract(supportedfact)
                    
                    # adjust rules it supports
                    for supportedrule in rule.supports_rules:
                        for list in supportedrule.supported_by: 
                            if rule in list: 
                                supportedrule.supported_by.remove(list)
                        self.kb_retract(supportedrule) 

                elif rule == fact_rule and rule.supported_by: 
                    if rule.asserted:
                        rule.asserted = False 

class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        
        ####################################################
        #Implement the Forward Chaining inferences that occur 
        # upon asserting facts and rules into the KB - i.e., 
        # implement the `InferenceEnginer.fc_infer` method.

        # given a fact and a rule, we want to see if they can be used to infer new facts or rules
        # first, we obtain the possible bindings that can be produced from the fact and rule
        binding = match(rule.lhs[0], fact.statement)
        # we are matching the first element of the rule LHS and the fact
        # this will return either a list of bindings or FALSE
        # example: rule LHS might be mother of ?x ?y, and a fact might be motherof ada bing
        # then the binding gives: ?x = ada, ?y = bing
        
        if binding:  
            inference = instantiate(rule.rhs, binding) # derive a statement from the rule and binding
            if len(rule.lhs) > 1: #if we have a rule
                newlhs = [] # create new lhs for new rule
                for n in range(1, len(rule.lhs)): # for every element in rule.lhs except the first element
                    lhsadd = instantiate(rule.lhs[n], binding)
                    newlhs.append(lhsadd)
                newrule = Rule([newlhs, inference], [[fact, rule]]) # create new instance of rule
                fact.supports_rules.append(newrule) #the old fact supports the new rule
                rule.supports_rules.append(newrule) #the old rule supports the new rule
                kb.kb_add(newrule) #add new rule to kb
            else: #if we have a fact
                newfact = Fact(inference, [[fact, rule]]) 
                fact.supports_facts.append(newfact) 
                rule.supports_facts.append(newfact) 
                kb.kb_add(newfact) 