# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import pandas as pd
import pytest
import sys
import os

os.chdir("..")
ABS_PATH = os.getcwd() + os.sep + "source_files"
sys.path.insert(0, ABS_PATH)
os.chdir(ABS_PATH)

from count_elements import count_elements
from syntax_review import syntax_review
from chemeq import chemeq

symbols = pd.read_csv("periodic_table.csv")['symbol'].values


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
    assert syntax_review(equation, symbols) == (reactants, products, elements)


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
    eq = chemeq("H2 + O2 = H2O")
    balance = eq.is_balanced
    assert balance is False

    react_formulas = (eq.__react__['formula'].values).tolist()
    assert react_formulas == ["H2", "O2"]

    assert eq.__elem__ == ['H', 'O']

    counts = eq.__react__[eq.__elem__].values.tolist()
    print(counts)
    assert counts == [[2, 0], [0, 2]]
