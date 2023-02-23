# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 13:21:25 2023

@author: User
"""
import re


def syntax_review(equation, all_symbols):
    '''Verify the syntax of equation and if it is correct, return
    the reactants and products compounds and a list of the present elements'''

    def get_elements(compound, all_symbols):
        '''returns a list with all elements present in a compound

        parameter
        ---------
        compound : string representing a chemical compound

        examples
        --------
        >>> get_elements("H2O")
        ['H','O']
        >>> get_elements("Cu(CO3)(OH)2")
        ['C', 'Cu', 'H', 'O']'''

        elements_in_comp = []

        # separate  subgroups of molecule and find their elements
        pattern = re.compile(r"(\()([A-Z]+[a-z]*[0-9]*)+(\))[0-9]*")
        subgroups = [x.group() for x in pattern.finditer(compound)]
        for subgroup in subgroups:
            compound = compound.replace(subgroup, "")
        if len(compound):
            subgroups = [compound] + subgroups
        subgroups = [x.replace("(", "") for x in subgroups]
        for subgroup in subgroups:
            # find words beginning in uppercase followed by lowercase/numbers
            # like O, Be, H20 and check  if they match an elements.
            pattern = re.compile("[A-Z]{1}[a-z]*[0-9]*|[a-z]+[0-9]*")
            matches = pattern.finditer(subgroup)
            for found in matches:
                symbol = re.match(r"^[A-Z]*[a-z]*|\W*", found.group()).group()
                if symbol in all_symbols:
                    elements_in_comp += [symbol]
                else:
                    text = f'Unrecognized element: "{symbol}" in "{compound}"'
                    raise ValueError(text)
        return list(elements_in_comp)

    def unique(list_of_elements):
        singles = []
        for element in list_of_elements:
            if element not in singles:
                singles += [element]
        return singles

    ########################################################################
    ########################################################################

    # Check equation is a string
    if not isinstance(equation, str):
        text = "Equation must be a string not a "
        raise TypeError(text + f"{type(equation)}")
    # look for characters other than valid characters.
    wrong_symbols = list(re.findall(r"[^a-z0-9A-Z ()\+=]+",
                                    equation))
    if len(wrong_symbols):
        text = 'Unrecognized symbol: '
        for symbol in wrong_symbols:
            text += '"' + symbol + '", '
        raise ValueError(text[:-2])
    # If the group is empty there are two contigous "+" signs
    if len(list(re.findall("(=)", equation))) > 1:
        raise ValueError("Too many equal signs")
    try:
        left_hand_side, right_hand_side = equation.replace(
                                            " ", "").split("=")
    except ValueError:
        raise ValueError('Missing equal sign "=" in equation')

    if len(left_hand_side) == 0:
        raise ValueError(f'Reactants missing in:  "{equation}"')
    if len(right_hand_side) == 0:
        raise ValueError(f'Products missing in: "{equation}"')

    reac_formulas = left_hand_side.split("+")
    prod_formulas = right_hand_side.split("+")
    if ('' in reac_formulas) | ('' in prod_formulas):
        text = 'there are too many plus (+) signs'
        raise ValueError(text)
    for comp in (reac_formulas + prod_formulas):
        # verify no empty parentheses are found
        if len(re.findall(r"(\(\))+", comp)):
            raise ValueError(f'Empty parentheses in "{comp}"')

        # verify every parenthesis is closed.
        parentheses = list(re.findall("[(]{1}|[)]{1}", comp))
        if len(parentheses):
            state = 0
            for item in parentheses:
                if item == '(':
                    state += 1
                else:
                    state += -1
            if state != 0:
                text = 'Open parentheses in: "' + comp + '"'
                raise ValueError(text)

    # find elements in both sides of eq and verify they are the same type
    reac_elements = []
    for comp in reac_formulas:
        for el in unique(get_elements(comp, all_symbols)):
            if el not in reac_elements:
                reac_elements += [el]
    reac_elements.sort()
    prod_elements = []
    for comp in prod_formulas:
        for el in unique(get_elements(comp, all_symbols)):
            if el not in prod_elements:
                prod_elements += [el]
    prod_elements.sort()
    if reac_elements != prod_elements:
        text = "Reactant's elements are different to product's elements"
        raise ValueError(text)
    return reac_formulas, prod_formulas, reac_elements