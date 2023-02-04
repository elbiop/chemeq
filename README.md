<H3>chemeq DESCRIPTION</H3>
<p> 
Package capable of balance chemical equations and contains<br>
most used portion of the periodic table of elements.<br>
<br>
the package has two objects: &#60;equation&#62; and &#60;periodic_table&#62.</a><br>
<br>
<b>1. equation</b><br>
========<br>
&emsp;CLASS that receives as input a chemical equation in the form<br>
&emsp;of a string of the shape:<br>
&emsp;"reactant_1 + ... + reactant_n  = product_1 + ... + product_n"<br>
&ensp;      properties:<br>
&emsp;&emsp;&emsp;      <b>is_balanced</b><br>
&emsp;&emsp;&emsp;&emsp;&emsp;     Boolean (True or False)<br>
&emsp;&emsp;&emsp;      <b>reactants</b><br>
&emsp;&emsp;&emsp;&emsp;&emsp;     pandas.DtataFrame where each row represents one<br>
&emsp;&emsp;&emsp;&emsp;&emsp;     of the reactant compounds, Their elements and<br>
&emsp;&emsp;&emsp;&emsp;&emsp;     molecular weight.<br>
&emsp;&emsp;&emsp;      <b>products</b><br>
&emsp;&emsp;&emsp;&emsp;&emsp;     pandas.DtataFrame where each row represents one<br>
&emsp;&emsp;&emsp;&emsp;&emsp;     of the product compounds. Their elements and<br>
&emsp;&emsp;&emsp;&emsp;&emsp;     molecular weight.<br>
&ensp;&ensp;      Method:<br>
&emsp;&emsp;&emsp;      <b>balance()</b><br>
&emsp;&emsp;&emsp;&emsp;&emsp;     Balances the equation if it is unbalanced.<br>>

<b> 2. periodic_table</b><br>
&emsp;     pandas.DataFrame with data from the periodic table of elements<br>
&emsp;     contains: Z, name, symbol, atomic mass, atomic mass error, period,<br>
&emsp;     group & state.<br>
&emsp;     Source for the periodic table of elements:<br>
&emsp;     IUPAC - International Union of Pure and Applied Chemistry<br>
&emsp;     https://iupac.org/what-we-do/periodic-table-of-elements/<br>
</p>
<H3>LIMITATIONS</H3>
<p>
  1. Does not include Rare earths, synthetic elements, Rn, Fr & Ra.
  2. Intermediate prefixes like those from hydrates such as Cu(SO4)•5H2O
     must be represented with subindexes like Cu(SO4)(H2O)5.
</p>
<p>
<H3>EXAMPLES</H3>
```
  >>> from chemeq import equation
  >>> eq = equation("C2H5(OH) + O2 = CO2 + H2O")
  >>> eq.is_balanced
  False
```</p>
  The balance status of the equation is also visible in
  the equation object itself.
<pre>  >>> eq
  &#60;Unbalanced equation: "C2H5(OH) + O2 = CO2 + H2O"&#62;</pre>

  To balance the equation invoque the balance() method
<pre>  >>> eq.balance()
  >>> eq.is_balanced
  True
  >>> eq
  &#60;Balanced equation: "C2H5(OH) + 3O2 = 2CO2 + 3H2O"&#62;
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
  

  An equation can be created with their indexes to test
  if it is balanced. If it is not it can be balanced later.
<pre>  >>> eq = equation("CuS + 8HNO3 = CuSO4 + 8NO2 + 4H2O")
  >>> eq.is_balanced
  True
  >>> eq = equation("73CuS + 73HNO3 = 11CuSO4 + 11NO2 + 11H2O")
  >>> eq.is_balanced
  False
  >>> eq.balance()
  >>> eq
  &#60;Balanced equation: "CuS + 8HNO3 = CuSO4 + 8NO2 + 4H2O"&#62;

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
</pre>
