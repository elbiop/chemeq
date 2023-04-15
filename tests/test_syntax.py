# -*- coding: utf-8 -*-
import pytest
import sys
import os
os.chdir("..")
ABS_PATH = os.getcwd() + os.sep + "chemeq"
sys.path.insert(0, ABS_PATH)
os.chdir(ABS_PATH)
from syntax_review import syntax_review


def test_syntax_review():
    # Must be a string
    with pytest.raises(TypeError):
        syntax_review(1234)

    with pytest.raises(ValueError):
        # Only valid characters: +, =, Letters, numbers, perentheses.
        syntax_review("#$% + *&^ = #$%*&")
        # must have at least one equal sign
        syntax_review("H2+O2 H2O")
        # only one equal sign
        syntax_review("H2+O2=H2O=H2O")
        # Must have reactants
        syntax_review("=H2O")
        # Must have products
        syntax_review("H2+O2=")
        # canot have empty parentheses
        syntax_review("C6H9()(OOH)3+O2 =CO2+H2O")
        # cannot have open pearentheses
        syntax_review(")H2+O2=H2O")
        # cannot have open pearentheses
        syntax_review("(H2+O2=)H2O")
        # case sensitive
        syntax_review("Ca+O2=caO")
        # reactants and products have the same elements
        syntax_review("H2+O2=NaCl")
        # Only periodic table symbols
        syntax_review("abc = abc")
        # Reactants and Product elements must be the same
        syntax_review("Na + Cl = KCl")
