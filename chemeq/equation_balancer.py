import os
import sys
import numpy as np
import pandas as pd

# installed = util.find_spec("chemeq")
# if installed.has_location:
    # PATH = installed.origin[:-11]
# else:
PATH = os.path.abspath(".")

sys.path.insert(0, PATH)
os.chdir(PATH)

from chemeq.syntax_review import syntax_review
from chemeq.count_elements import count_elements

periodic_table = pd.read_csv("periodic_table.csv", header=3)

class chemeq():
    '''CLASS that receives a string representing a chemical equation of the
    form:
    "reactant_1 + ... + reactant_n  = product_1 + ... + product_n"

    LIMITATIONS
    1. Does not include Rare earths, synthetic elements, Rn, Fr & Ra.
    2. Intermediate prefixes like those from hydrates such as Cu(SO4)·5H2O
          must be represented with subindexes like Cu(SO4)(H2O)5.

    EXAMPLES
    if an unbalanced equation is provided:
    >>> eq = chemeq("C2H5(OH) + O2 = CO2 + H2O")
    >>> eq
    <Unbalanced equation: "C2H5(OH) + O2 = CO2 + H2O">

    If a balanced equation is provided:
    >>> eq = chemeq("3O2 + C2H5(OH) = 2CO2 + 3H20")
    >>> eq
    <Balanced equation: "3O2 + C2H5(OH) = 2CO2 +3H2O">'''

    def __init__(self, equation):
        self.__eq = equation.replace(" ", "")
        self.__react = []
        self.__react = pd.DataFrame()
        self.__prod = pd.DataFrame()
        self.__balanced = False
        self.__extract()
        self.__reformat()
        self.__checkbal(self.__react['coefficient'].values,
                        self.__react[self.__elem__].values,
                        self.__prod['coefficient'].values,
                        self.__prod[self.__elem__].values)

    def __str__(self):
        return self.__eq

    def __repr__(self):
        if self.__balanced:
            return f'<Balanced equation: "{self.__eq}">'
        else:
            return f'<Unbalanced equation: "{self.__eq}">'

    @property
    def is_balanced(self):
        'Values are boolean: True or False'
        return self.__balanced

    @property
    def reactants(self) -> pd.DataFrame:
        '''pandas.DtataFrame where each row represents one of the reactant
        compounds, its molecular weights and elements.

        EXAMPLE:
        >>>eq = chemeq("C2H5(OH) + 3O2 = 2CO2 + 3H2O")
        >>> eq.reactants

                coefficient   formula  C  H  O  Mass(g/mol)
              0            1  C2H5(OH)  2  6  1       46.069
              1            3        O2  0  0  2       31.998'''
        return self.__react

    @property
    def products(self) -> pd.DataFrame:
        '''pandas.DtataFrame where each row represents one of the product
        compounds, molecular weights and elements.

        EXAMPLE:
        >>>eq = chemeq("C2H5(OH) + 3O2 = 2CO2 + 3H2O")
        >>>eq.products

            coefficient formula  C  H  O  Mass(g/mol)
          0            2     CO2  1  0  2       44.009
          1            3     H2O  0  2  1       18.015'''
        return self.__prod

    def __reformat(self):
        '''reassemble the equation with single spaces between  and
        symbols '''
        eq = ""
        for i, comp in enumerate(self.__react['formula']):
            prefix = int(self.__react['coefficient'][i])
            if prefix == 1:
                prefix = ""
            else:
                prefix = str(prefix)
            eq += prefix + comp + " + "
        eq = eq[:-2]
        eq += "= "
        for i, comp in enumerate(self.__prod['formula']):
            prefix = int(self.__prod['coefficient'][i])
            if prefix == 1:
                prefix = ""
            else:
                prefix = str(prefix)
            eq += prefix + comp + " + "
        self.__eq = eq[:-3]

    def __extract(self):
        '''Extract relevant information from equation such as reactant
        compounds, product compounds, Elements in each, the total quantity of
        each element and the respetive molecular masses of reactants and
        compounds'''
        all_symbols = periodic_table['symbol']
        reac, prod, elem = syntax_review(self.__eq)
        self.__react['formula'] = reac
        self.__prod['formula'] = prod
        self.__elem__ = elem
        atomic_masses = periodic_table[all_symbols.isin(
                                    self.__elem__)].sort_values(by="symbol")
        atomic_masses = atomic_masses['atomic_mass'].values

        # Extract coefficients formula and elements count
        formulas, coefficients, counts = [], [], []
        for i, comp in enumerate(self.__react['formula']):
            formula, coefficient, count = count_elements(comp, self.__elem__)
            formulas += [formula]
            coefficients += [coefficient]
            counts += [count]
        self.__react = pd.DataFrame(np.array(coefficients)[:, np.newaxis],
                                    columns=['coefficient'])
        self.__react['formula'] = formulas
        self.__react = pd.concat([self.__react,
                                  pd.DataFrame(counts,
                                               columns=self.__elem__,
                                               dtype=np.int64)], axis=1)
        self.__react['Mass(g/mol)'] = np.sum(np.multiply(counts,
                                             atomic_masses), axis=1)

        formulas, coefficients, counts = [], [], []
        for i, comp in enumerate(self.__prod['formula']):
            formula, coefficient, count = count_elements(comp, self.__elem__)
            formulas += [formula]
            coefficients += [coefficient]
            counts += [count]

        self.__prod = pd.DataFrame(np.array(coefficients)[:, np.newaxis],
                                   columns=['coefficient'])
        self.__prod['formula'] = formulas
        self.__prod = pd.concat([self.__prod,
                                 pd.DataFrame(counts,
                                              columns=self.__elem__,
                                              dtype=np.int64)],
                                axis=1)
        self.__prod['Mass(g/mol)'] = np.sum(np.multiply(counts,
                                            atomic_masses), axis=1)

    def __checkbal(self, reac_coef, reac_count, prod_coef, prod_count):
        '''check if elements in both sides of eq are in equal amounts.'''
        reac_atoms = np.matmul(reac_coef, reac_count)
        prod_atoms = np.matmul(prod_coef, prod_count)
        if np.multiply.reduce(reac_atoms == prod_atoms):
            self.__balanced = True
        else:
            self.__balanced = False
        return (reac_atoms, prod_atoms)

    def balance(self):
        '''balances a chemical equation of the form:
        "compound_1 + ... + compound_n  = product_1 + ... + product_n"


        limitations
        -----------
        - Does not include Rare earths, synthetetic elements, Rn, Fr & Ra.
        - Hidrates representations must have coefficient like Cu(SO4)(H2O)5
          instead of prefixes like Cu(SO4)·5H2O

        examples
        --------
        >>> eq = chemeq('C2H6 + O2 = CO2 + H2O')
        >>> eq
            <Unbalanced equation: "C2H6 + O2 = CO2 + H2O">
        >>> eq.balance()
        >>> eq
            <Balanced equation: '2C2H6 + 7O2 = 4CO2 + 6H2O'>
        '''
        # separate the compounds of each side of equation
        # create the matrices of subindexes and coefficients of both sides
        # each row will be a compound and each column one of the elements
        #         that are present in the equation

        if self.__balanced:
            return None

        reac_count = self.__react[self.__elem__].values.astype(np.int64)
        prod_count = self.__prod[self.__elem__].values.astype(np.int64)
        reac_coef = np.full(reac_count.shape[0], 1, dtype=np.int64)
        prod_coef = np.full(prod_count.shape[0], 1, dtype=np.int64)

        ''' ****Algorithm****
        if the equation is unbalanced the sum of elements in one side will be
        not equal to the elements in the other side
            choose the side with more elements ( reac or prod )
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
        reac_atoms, prod_atoms = self.__checkbal(reac_coef, reac_count,
                                                 prod_coef, prod_count)

        while not(self.__balanced):
            # if right side has more elements count
            #     find the coefficient and the coefficient of the element that
            #     has more elements and multiply by the compound in the left
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
                # What elements are more abundant in the product?
                elem_index = np.where(prod_atoms > reac_atoms)[0]
                # pick at random one of the elements that are in excess
                elem_index = elem_index[np.random.randint(len(elem_index))]
                # pick at random a compound of reactants that has that atom
                # compounds where the sub is > 0, i.e. the atom is present
                comp_index = np.where(reac_count[:, elem_index] > 0)[0]
                comp_index = comp_index[np.random.randint(len(comp_index))]
                # how many elements has to be added to the coefficient to equal
                #    the elements in the other side take the difference between
                #    the number of elements in both sides and divide by the
                #    sub-index of the element in the selected compound
                increment = (prod_atoms - reac_atoms)[elem_index]/reac_count[
                                                        comp_index, elem_index]
                try:
                    if increment % 1 > 0:
                        reac_coef = reac_coef + reac_count[comp_index,
                                                           elem_index]

                        reac_coef[comp_index] = (reac_coef[comp_index] +
                                                 (prod_atoms - reac_atoms)
                                                 [elem_index] - reac_count
                                                 [comp_index, elem_index]
                                                 )
                    else:

                        reac_coef[comp_index] = (reac_coef[comp_index] +
                                                 increment
                                                 )
                except Exception:
                    # In case the increment overflows int64 capacity
                    pass

            elif out_of_balance == 'reactants':
                # What elements are more abundant in the reactants?
                elem_index = np.where(reac_atoms > prod_atoms)[0]
                # pick a random element that is in excess
                elem_index = elem_index[np.random.randint(len(elem_index))]
                # pick a random compound of the products that has that element
                # compounds where the sub is > 0, i.e. the element is present
                comp_index = np.where(prod_count[:, elem_index] > 0)[0]
                comp_index = comp_index[np.random.randint(len(comp_index))]
                # how many elements has to be added to the coefficient to equal
                #    the elements in the other side take the difference between
                #    the number of elements in both sides and divide by the
                #    sub-index of the element in the selected compound
                increment = (reac_atoms - prod_atoms)[elem_index]/prod_count[
                                                    comp_index, elem_index]
                try:
                    if increment % 1 > 0:
                        prod_coef = prod_coef + prod_count[comp_index,
                                                           elem_index]
                        prod_coef[comp_index] = (prod_coef[comp_index] + (
                                    reac_atoms - prod_atoms)[elem_index] -
                                    prod_count[comp_index, elem_index])
                    else:
                        prod_coef[comp_index] = (prod_coef[comp_index] +
                                                 increment)
                except Exception:
                    # In case the increment overflows int64 capacity
                    pass
            reac_atoms, prod_atoms = self.__checkbal(
                            reac_coef, reac_count, prod_coef, prod_count)
            # break here before restarting coefficients in case is balanced
            if self.__balanced:
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

        # Simplify coeficients dividing by the greatest common divider
        reac_coef = np.array(reac_coef, np.int64)
        prod_coef = np.array(prod_coef, np.int64)
        gcd = np.gcd.reduce(np.hstack([reac_coef, prod_coef]))
        reac_coef = reac_coef/gcd
        prod_coef = prod_coef/gcd
        self.__react['coefficient'] = reac_coef.astype(np.int64)
        self.__prod['coefficient'] = prod_coef.astype(np.int64)
        self.__reformat()
