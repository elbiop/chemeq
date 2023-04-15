## PROJECT DESCRIPTION  

Package capable of balance chemical equations and containsthe most used portion of the periodic table of elements.   
The package has two objects: **chemeq** and **periodic_table**

### 1. chemeq
&emsp; CLASS, Receives a string representing a chemical equation  as input.  
&emsp; In the shape: "reactant_1 + ... + reactant_n  = product_1 + ... + product_n".    

&emsp; The **chemeq CLASS** has three properties and one method.  

&emsp;&emsp;      **is_balanced** : Property. Boolean (True or False)  
&emsp;&emsp;      **reactants** &emsp;: Property. pandas.DtataFrame where each row represents one of the reactants (left side) compounds,  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; molecular weights and elements.   
&emsp;&emsp;      **products** &emsp; : Property. pandas.DtataFrame where each row represents one of the product (right side) compounds,  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; molecular weights and elements.   
&emsp;&emsp;      **balance()** &emsp; : Method. Balances the equation if it is unbalanced.  


### 2. periodic_table
&emsp;  pandas.DataFrame containing a portion of the periodic table of elements contains: Z, name, symbol, atomic mass,  
&emsp;  atomic mass error, period, group & state.  

&emsp;     Source for the periodic table of elements:   
&emsp;     IUPAC - International Union of Pure and Applied Chemistry   
&emsp;     https://iupac.org/what-we-do/periodic-table-of-elements/   

## LIMITATIONS
- Does not include Rare earths, synthetic elements, Radon, Francium & Radium.  
- Intermediate prefixes like those from hydrates such as Cu(SO4)•5H2O    
&emsp; must be represented with subindexes like Cu(SO4)(H2O)5.

## EXAMPLES
```
  >>> from chemeq import chemeq
  >>> eq = chemeq("C2H5(OH) + O2 = CO2 + H2O")
  >>> eq.is_balanced
  False
```  
  The balance status of the equation is also visible in the equation object itself.
```
  >>> eq
  <Unbalanced equation: "C2H5(OH) + O2 = CO2 + H2O">
```
  To balance the equation invoke the balance() method
```
>>> eq.balance()
  >>> eq.is_balanced
  True
  >>> eq
  <Balanced equation: "C2H5(OH) + 3O2 = 2CO2 + 3H2O">
```
Example of its properties
```
  >>> str(eq)
  "C2H5(OH) + 3O2 = 2CO2 + 3H2O"
  >>> eq.reactants
     coefficient   formula  C  H  O  Mass(g/mol)
  0            1  C2H5(OH)  2  6  1       46.069
  1            3        O2  0  0  2       31.998
  >>> eq.products
     coefficient formula  C  H  O  Mass(g/mol)
  0            2     CO2  1  0  2       44.009
  1            3     H2O  0  2  1       18.015</pre>
```

  An equation can be created with their indexes to test if it is balanced. If it is not it can be balanced later.
```
>>> eq = chemeq("CuS + 8HNO3 = CuSO4 + 8NO2 + 4H2O")
  >>> eq.is_balanced
  True
  >>> eq = chemeq("73CuS + 73HNO3 = 11CuSO4 + 11NO2 + 11H2O")
  >>> eq.is_balanced
  False
  >>> eq.balance()
  >>> eq
<Balanced equation: "CuS + 8HNO3 = CuSO4 + 8NO2 + 4H2O">
```
```
  >>> from chemeq import periodic_table
  >>> periodic_table
                      name symbol  atomic_weight   error  group  period state
  atomic_number
  1               Hydrogen      H         1.0080  0.0002      1       1     g
  2                 Helium     He         4.0026  0.0001     18       1     g
  3                Lithium     Li         6.9400  0.0600      1       2     s
  4              Beryllium     Be         9.0122  0.0001      2       2     s
  5                  Boron      B        10.8100  0.0200     13       2     s
  ...                  ...    ...            ...     ...    ...     ...   ...
  79                  Gold     Au       196.9700  0.0100     11       6     s
  80               Mercury     Hg       200.5900  0.0100     12       6     l
  81              Thallium     Tl       204.3800  0.0100     13       6     s
  82                  Lead     Pb       207.2000  1.1000     14       6     s
  83               Bismuth     Bi       208.9800  0.0100     15       6     s
  [67 rows x 7 columns]
```
