import os
import unittest

from dynamic_stack_decider.parser import DSDParser
from dynamic_stack_decider.tree import DecisionTreeElement, ActionTreeElement, SequenceTreeElement


class ParserTest(unittest.TestCase):
    def setUp(self):
        parser = DSDParser()
        self.tree = parser.parse(os.path.join(os.path.dirname(__file__), 'test.dsd'))

    def test_root_element(self):
        root_element = self.tree.root_element
        self.assertTrue(isinstance(root_element, DecisionTreeElement))
        self.assertEqual(root_element.name, 'FirstDecision')

    def test_possible_results(self):
        self.assertSetEqual(set(self.tree.root_element.children.keys()),
                            {'ACTION', 'DECISION', 'SUBBEHAVIOR', 'SEQUENCE', 'PARAMETERS'})

    def test_following_elements(self):
        first_child = self.tree.root_element.get_child('ACTION')
        self.assertEqual(first_child.name, 'FirstAction')
        self.assertTrue(isinstance(first_child, ActionTreeElement))

        second_child = self.tree.root_element.get_child('DECISION')
        self.assertEqual(second_child.name, 'SecondDecision')
        self.assertTrue(isinstance(second_child, DecisionTreeElement))

    def test_nested_decision(self):
        decision_child = self.tree.root_element.get_child('DECISION')
        self.assertSetEqual(set(decision_child.children.keys()), {'FIRST', 'SECOND'})
        self.assertEqual(decision_child.get_child('FIRST').name, 'FirstAction')
        self.assertTrue(isinstance(decision_child.get_child('FIRST'), ActionTreeElement))
        self.assertEqual(decision_child.get_child('SECOND').name, 'SecondAction')
        self.assertTrue(isinstance(decision_child.get_child('SECOND'), ActionTreeElement))

    def test_sub_behavior(self):
        sub_behavior_root_decision = self.tree.root_element.get_child('SUBBEHAVIOR')
        self.assertEqual(sub_behavior_root_decision.name, 'ThirdDecision')
        self.assertTrue(isinstance(sub_behavior_root_decision, DecisionTreeElement))
        self.assertSetEqual(set(sub_behavior_root_decision.children.keys()), {'FIRST', 'SECOND'})
        self.assertEqual(sub_behavior_root_decision.get_child('FIRST').name, 'FirstAction')
        self.assertTrue(isinstance(sub_behavior_root_decision.get_child('FIRST'), ActionTreeElement))
        self.assertEqual(sub_behavior_root_decision.get_child('SECOND').name, 'SecondAction')
        self.assertTrue(isinstance(sub_behavior_root_decision.get_child('SECOND'), ActionTreeElement))

    def test_sequence_element(self):
        sequence_element = self.tree.root_element.get_child('SEQUENCE')
        self.assertTrue(isinstance(sequence_element, SequenceTreeElement))
        self.assertEqual(len(sequence_element.action_elements), 2)
        first_action = sequence_element.action_elements[0]
        self.assertEqual(first_action.name, 'FirstAction')
        self.assertTrue(isinstance(first_action, ActionTreeElement))
        second_action = sequence_element.action_elements[1]
        self.assertEqual(second_action.name, 'SecondAction')
        self.assertTrue(isinstance(second_action, ActionTreeElement))

    def test_parameters(self):
        parameter_element = self.tree.root_element.get_child('PARAMETERS')
        self.assertEqual(parameter_element.name, 'FirstAction')
        self.assertTrue(isinstance(parameter_element, ActionTreeElement))
        self.assertDictEqual(parameter_element.parameters, {'key': 'value'})


if __name__ == '__main__':
    unittest.main()
