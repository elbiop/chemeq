# -*- coding: utf-8 -*-
import pytest
import pandas as pd
import sys
import os

ABS_PATH = os.getcwd() #[:-5] + "source_files"
sys.path.insert(0, ABS_PATH)
os.chdir(ABS_PATH)

from syntax_review import syntax_review


all_symbols = pd.read_csv("periodic_table.csv")['symbol'].values


def test_syntax_review():
    # Must be a string
    with pytest.raises(TypeError):
        syntax_review(1234, all_symbols)

    with pytest.raises(ValueError):
        # Only valid characters: +, =, Letters, numbers, perentheses.
        syntax_review("#$% + *&^ = #$%*&", all_symbols)
        # must have at least one equal sign
        syntax_review("H2+O2 H2O", all_symbols)
        # only one equal sign
        syntax_review("H2+O2=H2O=H2O", all_symbols)
        # Must have reactants
        syntax_review("=H2O", all_symbols)
        # Must have products
        syntax_review("H2+O2=", all_symbols)
        # canot have empty parentheses
        syntax_review("C6H9()(OOH)3+O2 =CO2+H2O", all_symbols)
        # cannot have open pearentheses
        syntax_review(")H2+O2=H2O", all_symbols)
        # cannot have open pearentheses
        syntax_review("(H2+O2=)H2O", all_symbols)
        # case sensitive
        syntax_review("Ca+O2=caO", all_symbols)
        # reactants and products have the same elements
        syntax_review("H2+O2=NaCl", all_symbols)
        # Only periodic table symbols
        syntax_review("abc = abc", all_symbols)
        # Reactants and Product elements must be the same
        syntax_review("Na + Cl = KCl", all_symbols)
