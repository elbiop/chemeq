# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import re

"""
Created on Fri Jan 21 07:15:03 2023
Python 3.10.6

@author:
    Elbio Peña
    elbioemilio@outlook.es
    linkedin.com/in/ingeniero-elbio-peña
    github.com/elbiop/chemeq

"""

'''Source for the periodic table of elements:
IUPAC - International Union of Pure and Aplied Chemistry
https://iupac.org/what-we-do/periodic-table-of-elements/'''
path1 = "C:\\Users\\Omar\\Documents\\Python\\chemeq\\"
path2 = "source_files\\periodic_table.csv"
path = path1 + path2
periodic_table = pd.read_csv(path)
periodic_table.set_index('Z', inplace=True)
del(path1, path2, path)


class equation():

    def __init__(self, equation):
        self.__eq__ = equation
        self.__elem__ = []
        self.reactants = pd.DataFrame()
        self.products = pd.DataFrame()
        self.is_balanced = False
        self.__verify__()
        self.__check_bal__(self.reactants['coefficient'].values,
                           self.reactants[self.__elem__].values,
                           self.products['coefficient'].values,
                           self.products[self.__elem__].values)

    def __verify__(self):
        '''Verify the syntax of equation and if it is correct, return
        the reactants and products compounds as well as details about each
        of the compounds like the quantity'''

        # Check is a string
        if not isinstance(self.__eq__, str):
            text = "Equation must be a string not a "
            raise TypeError(text + f"{type(self.__eq__)}")
        # look for characters other than valid characters.
        wrong_symbols = list(re.findall(r"[^a-z0-9A-Z ()\+=]+",
                                        self.__eq__))
        if len(wrong_symbols):
            text = 'Unrecognized symbol: '
            for symbol in wrong_symbols:
                text += '"' + symbol + '", '
            raise ValueError(text[:-2])
        if len(list(re.findall("(=)", self.__eq__))) > 1:
            raise ValueError("Too many equal signs")
        try:
            left_hand_side, right_hand_side = self.__eq__.replace(
                                                " ", "").split("=")
        except ValueError:
            raise ValueError('Missing equal sign "=" in equation')

        if len(left_hand_side) == 0:
            raise ValueError(f'Reactants missing in:  "{self.__eq__}"')
        if len(right_hand_side) == 0:
            raise ValueError(f'Products missing in: "{self.__eq__}"')

        reac_formulas = left_hand_side.split("+")
        prod_formulas = right_hand_side.split("+")

        for comp in np.hstack([reac_formulas, prod_formulas]):
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
            for el in self.__get_elements__(comp):
                if el not in reac_elements:
                    reac_elements += [el]
        reac_elements.sort()
        prod_elements = []
        for comp in prod_formulas:
            for el in self.__get_elements__(comp):
                if el not in prod_elements:
                    prod_elements += [el]
        prod_elements.sort()
        if reac_elements != prod_elements:
            text = "Reactant's elements are different to product's elements"
            raise ValueError(text)
        self.__elem__ = reac_elements

        atomic_masses = periodic_table[periodic_table['symbol'].isin(
                                    self.__elem__)].sort_values(by="symbol")
        atomic_masses = atomic_masses['atomic_mass'].values

        # Extract coefficients and atom count
        formulas, coefficients, counts = [], [], []
        for i, comp in enumerate(reac_formulas):
            formula, coefficient, count = self.__count__(comp)
            formulas += [formula]
            coefficients += [coefficient]
            counts += [count]
        self.reactants = pd.DataFrame(np.array(coefficients)[:, np.newaxis],
                                      columns=['coefficient'])
        self.reactants['formula'] = formulas
        self.reactants = pd.concat([self.reactants,
                                    pd.DataFrame(counts,
                                                 columns=self.__elem__,
                                                 dtype=np.int64)], axis=1)
        self.reactants['Mass(g/mol)'] = np.sum(np.multiply(counts,
                                               atomic_masses), axis=1)

        formulas, coefficients, counts = [], [], []
        for i, comp in enumerate(prod_formulas):
            formula, coefficient, count = self.__count__(comp)
            formulas += [formula]
            coefficients += [coefficient]
            counts += [count]

        self.products = pd.DataFrame(np.array(coefficients)[:, np.newaxis],
                                     columns=['coefficient'])
        self.products['formula'] = formulas
        self.products = pd.concat([self.products,
                                   pd.DataFrame(counts,
                                                columns=self.__elem__,
                                                dtype=np.int64)],
                                  axis=1)
        self.products['Mass(g/mol)'] = np.sum(np.multiply(counts,
                                              atomic_masses), axis=1)

    def __get_elements__(self, compound):
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

        all_elements = periodic_table['symbol'].values
        elements_in_comp = []

        # separate  subgroups of molecule and find their elements
        for subgroup in re.split("[(]", compound):
            # varify each subgroup contains Uppercase letters
            if len(re.findall("[A-Z]+", subgroup)) == 0:
                if subgroup.find(")") >= 0:
                    subgroup = "(" + subgroup
                text = f'''compound "{subgroup}" doesn't have valid elements or there are too many plus (+) signs'''
                raise ValueError(text)
            # find words beginning in uppercase followed by lowercase/numbers
            # like O, Be, H20 and check  if they match an elements.
            pattern = re.compile("[A-Z]{1}[a-z]*[0-9]*|[a-z]+[0-9]*")
            matches = pattern.finditer(subgroup)
            for found in matches:
                symbol = re.match(r"^[A-Z]*[a-z]*|\W*", found.group()).group()
                if symbol in all_elements:
                    elements_in_comp += [symbol]
                else:
                    raise TypeError(f'Unrecognized symbol: "{symbol}" in "{compound}"')
        return list(np.unique(elements_in_comp))

    def __count__(self, compound):
        '''counts the number of appearances of a list of elements in a
        compound

        parameters
        ----------
        compound  : string representing a chemical compound
        elements  : list_like containing atomic symbols of chemical elements
                    ordered alphabetically.

        examples
        --------
        >>> count("H2O",['H','O'])
        array([2., 1.])
        >>> count("H2O")
        array([2., 1.])
        >>> count("Cu(CO3)(OH)2",['C', 'Cu', 'H', 'O'])
        array([1., 1., 2., 5.])
        '''
        coefficient = re.findall("^[0-9]+(?=[A-Z])", compound)
        if len(coefficient):
            compound = compound[len(coefficient[0]):]
            coefficient = int(coefficient[0])
        else:
            coefficient = 1

        subindexes = np.zeros(len(self.__elem__))
        # iterate over each subgroup of the compound
        # e.g.:
        for group in compound.split("("):
            group_sub_ix = 1
            if group.find(")") > 0:
                group, remain = group.split(")")
                if len(remain):
                    group_sub_ix = int(remain)
            '''find the element that is followed by 0 or more numbers and
            without retrieval not followed by lowercase to avoid false positive
            of single letters elements with two letter elements that begin with
            the same letter'''
            # add whitespace to comply with the regex in case of no sub index
            group += " "
            for k, el in enumerate(self.__elem__):
                pattern = re.compile(f'{el}' + '{1}[0-9]*(?=[^a-z])')
                matches = list(pattern.finditer(group))
                for m in matches:
                    # if match is not followed by numbers add 1
                    # if is add that number"
                    if len(m.group()[len(el):]):
                        subindexes[k] += group_sub_ix*int(m.group()[len(el):])
                    else:
                        subindexes[k] += group_sub_ix
        return(compound, coefficient, subindexes)

    def __check_bal__(self, reac_coef, reac_count, prod_coef, prod_count):
        '''chech if elements in both sides of eq are in equal amounts.'''
        reac_atoms = np.matmul(reac_coef, reac_count)
        prod_atoms = np.matmul(prod_coef, prod_count)
        if np.multiply.reduce(reac_atoms == prod_atoms):
            self.is_balanced = True
        else:
            self.is_balanced = False
        return (reac_atoms, prod_atoms)

    def balance(self):
        '''balances a chemical equation of the form:
       "compound_1 + ... + compound_n  = product_1 + ... + product_n"


        limitations
        -----------
        - Does not include Rare earths, synthetetic elements, Rn, Fr & Ra.
        - Hidrates representations must have coefficient like Cu(SO4)(H2O)5
          instead of prefixes like Cu(SO4)•5H2O

        examples
        --------
        >>>eq = equation('C2H6 + O2 = CO2 + H2O')
        >>>eq.balance()
        >>>eq
            <Balanced equation: '2C2H6 + 7O2 = 4CO2 + 6H2O'>
        '''
        # separate the compounds of each side of equation
        # create the matrices of subindexes and coefficients of both sides
        # each row will be a compound and each column one of the elements
        #         that are present in the equation

        if self.is_balanced:
            return None

        reactants = self.reactants['formula'].values
        products = self.products['formula'].values
        reac_count = self.reactants[self.__elem__].values.astype(np.int64)
        prod_count = self.products[self.__elem__].values.astype(np.int64)
        reac_coef = np.full(reac_count.shape[0], 1, dtype=np.int64)
        prod_coef = np.full(prod_count.shape[0], 1, dtype=np.int64)

        ''' ****Algorithm****
        if the equation is unbalanced the sum of all atoms in one side will be
        not equal to the atoms in the other side
           choose the side with more atoms ( reac or prod )
           find which element has a different sum
           pick one at random.
           find the compounds in the other side that have that element
           Update the coefficient of that compund to counteract the difference
           check if it is balanced if not repeat
            '''
        # the maximum coefficient in the intermediate equation while is being
        # balanced can be higher than the final coefficient but is proportional
        # to the maximum subindex in the equation
        max_coef = 50*np.sqrt(np.max(np.hstack([np.max(reac_count, axis=0),
                                                np.max(prod_count, axis=0)])))
        # Maximum number of iterations
        high_limit = 50_000
        counter = 0
        reac_atoms, prod_atoms = self.__check_bal__(reac_coef, reac_count,
                                                    prod_coef, prod_count)

        while not(self.is_balanced):
            # if right side has more atoms count
            #     find the coefficient and the coefficient of the element that
            #     has more atoms and multiply by the compound in the left
            #     side with that element update the coefficients

            if (True in (prod_atoms > reac_atoms)) and (True in (reac_atoms >
                                                                 prod_atoms)):
                out_of_balance = ['reactants',
                                  'products'][np.random.randint(2)]
            elif True in (prod_atoms > reac_atoms):
                out_of_balance = 'products'
            else:
                out_of_balance = 'reactants'

            if out_of_balance == 'products':
                # What atoms are more abundant in the product?
                atom_index = np.where(prod_atoms > reac_atoms)[0]
                # pick at random one of the atoms that are in excess
                atom_index = atom_index[np.random.randint(len(atom_index))]
                # pick at random a compound of reactants that has that atom
                # compounds where the sub is > 0, i.e. the atom is present
                comp_index = np.where(reac_count[:, atom_index] > 0)[0]
                comp_index = comp_index[np.random.randint(len(comp_index))]
                # how many atoms has to be added to the coefficient to equal
                #    the atoms in the other side take the difference between
                #    the number of atoms in both sides and divide by the sub
                #    of the element in the selected compound
                increment = (prod_atoms - reac_atoms)[atom_index]/reac_count[
                                                        comp_index, atom_index]
                try:
                    if increment % 1 > 0:
                        reac_coef = reac_coef + reac_count[comp_index,
                                                           atom_index]

                        reac_coef[comp_index] = (reac_coef[comp_index] +
                                                 (prod_atoms - reac_atoms)
                                                 [atom_index] - reac_count
                                                 [comp_index, atom_index]
                                                 )
                    else:

                        reac_coef[comp_index] = (reac_coef[comp_index] +
                                                 increment
                                                 )
                except Exception:
                    # In case the increment overflows int64 capacity
                    pass

            elif out_of_balance == 'reactants':
                # What atoms are more abundant in the reactants?
                atom_index = np.where(reac_atoms > prod_atoms)[0]
                # pick a random atom that is in excess
                atom_index = atom_index[np.random.randint(len(atom_index))]
                # pick a random compound of the products that has that atom
                # compounds where the sub is > 0, i.e. the atom is present
                comp_index = np.where(prod_count[:, atom_index] > 0)[0]
                comp_index = comp_index[np.random.randint(len(comp_index))]
                # how many atoms has to be added to the coefficient to equal
                #    the atoms in the other side take the difference between
                #    the number of atoms in both sides and divide by the sub
                #    of the element in the selected compound
                increment = (reac_atoms - prod_atoms)[atom_index]/prod_count[
                                                    comp_index, atom_index]
                try:
                    if increment % 1 > 0:
                        prod_coef = prod_coef + prod_count[comp_index,
                                                           atom_index]
                        prod_coef[comp_index] = (prod_coef[comp_index] + (
                                    reac_atoms - prod_atoms)[atom_index] -
                                    prod_count[comp_index, atom_index])
                    else:
                        prod_coef[comp_index] = (prod_coef[comp_index] +
                                                 increment)
                except Exception:
                    # In case the increment overflows int64 capacity
                    pass
            reac_atoms, prod_atoms = self.__check_bal__(
                           reac_coef, reac_count, prod_coef, prod_count)
            # break here before restarting coefficients in case is balanced
            if self.is_balanced:
                break

            # force stop if reach high limit
            counter += 1
            if counter == high_limit:
                text = f"The equation couldn't be solved, {high_limit:,}"
                raise RuntimeError(text + " iterations reached!")

            # if the coeficents reach a number to high restart the coefficients
            if np.max(np.hstack([reac_coef, prod_coef])) > max_coef:
                reac_coef = np.full(len(reac_coef), 1)
                prod_coef = np.full(len(prod_coef), 1)

        # Find the greatest common divider of all coefficients and divide
        reac_coef = np.array(reac_coef, np.int64)
        prod_coef = np.array(prod_coef, np.int64)
        gcd = np.gcd.reduce(np.hstack([reac_coef, prod_coef]))
        reac_coef = reac_coef/gcd
        prod_coef = prod_coef/gcd
        self.reactants['coefficient'] = reac_coef.astype(np.int64)
        self.products['coefficient'] = prod_coef.astype(np.int64)

        # assemble the equation add the prefix from the coef to each of the
        # compounds only if it greater than 1
        eq = ""
        for i, comp in enumerate(reactants):
            prefix = int(reac_coef[i])
            if prefix == 1:
                prefix = ""
            else:
                prefix = str(prefix)
            eq += prefix + comp + " + "
        eq = eq[:-2]
        eq += "= "
        for i, comp in enumerate(products):
            prefix = int(prod_coef[i])
            if prefix == 1:
                prefix = ""
            else:
                prefix = str(prefix)
            eq += prefix + comp + " + "
        self.__eq__ = eq[:-3]

    def __str__(self):
        return self.__eq__

    def __repr__(self):
        if self.is_balanced:
            return f'<Balanced equation: "{self.__eq__}">'
        else:
            return f'<Unbalanced equation: "{self.__eq__}">'
