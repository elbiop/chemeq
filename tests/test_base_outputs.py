# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import pandas as pd
import pytest
import sys
import os

os.chdir("..")
ABS_PATH = os.getcwd() + os.sep + "chemeq"
sys.path.insert(0, ABS_PATH)
os.chdir(ABS_PATH)

from count_elements import count_elements
from syntax_review import syntax_review
from equation_balancer import chemeq


@pytest.mark.parametrize(
    "equation, reactants, products, elements", [
        # simple equation
        ("C2H5 + O2 = CO2 + H2O",
         ['C2H5', 'O2'],
         ['CO2', 'H2O'],
         ['C', 'H', 'O']),
        # Complex equation
        ("NH4OH + KAl(SO4)2(H2O)12 = Al(OH)3 + (NH4)2SO4 + KOH + H2O",
         ['NH4OH', 'KAl(SO4)2(H2O)12'],
         ['Al(OH)3', '(NH4)2SO4', 'KOH', 'H2O'],
         ['Al', 'H', 'K', 'N', 'O', 'S'])])
def test_syntax_review_outputs(equation, reactants, products, elements):
    assert syntax_review(equation) == (reactants, products, elements)


@pytest.mark.parametrize(
    "compound, elements, formula, prefix, count", [
        # simple compund
        ("NaCl", ["Na", "Cl"], "NaCl", 1, [1, 1]),
        # compound with subindexes
        ("H2O", ["H", "O"], "H2O", 1, [2, 1]),
        # compound with multiple subindexes
        ("C12H22O11", ["C", "H", "O"], "C12H22O11", 1, [12, 22, 11]),
        # compound with prefix
        ("35H2O", ["H", "O"], "H2O", 35, [2, 1]),
        # compound with parentheses
        ("KAl(SO4)(H2O)", ["Al", "H", "K", "O", "S"],
         "KAl(SO4)(H2O)", 1,  [1, 2, 1, 5, 1]),
        # compound with multiple subindexes, groups an prefix
        ("22KAl5(SO4)2(H2O)10", ["Al", "H", "K", "O", "S"],
         "KAl5(SO4)2(H2O)10", 22, [5, 20, 1, 18, 2])
    ])
def test_count_elements(compound, elements, formula, prefix, count):
    assert count_elements(compound, elements) == (formula, prefix, count)


def test_chemeq_parts():
    eq = chemeq("3H2 + O2 = 7H2O")
    balance = eq.is_balanced
    assert balance is False

    react_formulas = (eq.reactants['formula'].values).tolist()
    assert react_formulas == ["H2", "O2"]

    prod_formulas = (eq.products['formula'].values).tolist()
    assert prod_formulas == ["H2O"]

    counts = eq.reactants[['H','O']].values.tolist()
    assert counts == [[2, 0], [0, 2]]
