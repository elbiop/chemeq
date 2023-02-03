<H3 orientation="center"><u> Project Description </u></H3>
balances a chemical equation of the form:<br>
<b>reactant_1 + ... + reactant_n  = product_1 + ... + product_n</b><br>
By creating an equation object and invokng the <i><b> balance()</b></i> method<br>
<H3><u> Examples </u></H3>
<pre>
>>> from chemeq import equation
>>> eq = equation("C2H5(OH) + O2 = CO2 + H2O")
</pre>
To check if the equation is balanced use the <b><i>is_balanced</i></b> propertie
<pre>
>>> eq.is_balanced
    False</pre>
this information is also visible in the equation object itsef

<pre>
>>> eq
    &#60;Unbalanced equation: "C2H5(OH) + O2 = CO2 + H2O"&#62;
</pre>
To balance the equation invoque the <b><i> balance()</i></b> method
<pre>
>>> eq.balance()
>>> eq.is_balanced
    True
>>> eq
    &#60;Balanced equation: "C2H5(OH) + 3O2 = 2CO2 + 3H2O"&#62;
>>> str(eq)
    "C2H5(OH) + 3O2 = 2CO2 + 3H2O"
</pre>
Also you can input an equation with their indexes to test if it is balanced<br>
or balance it even when the indexes are wrong.
<pre>
>>> eq = equation("CuS + 8HNO3 = CuSO4 + 8NO2 + 4H2O")
>>> eq.is_balanced
    True
>>> eq = equation("7CuS + 8HNO3 = CuSO4 + 8NO2 + 4H2O")
>>> eq.is_balanced
    False
>>> eq.balance()
>>> eq
    &#60;Balanced equation: "CuS + 8HNO3 = CuSO4 + 8NO2 + 4H2O"&#62;
</pre>


The equation objects have two other properties: <b>reactants</b> and <b>products</b><br>
when invoked they return a <b><i>pandas.DataFrame</i></b> detailing the content<br>
of each of the compounds in that group.<br>
<pre>
>>> eq.reactants
       coefficient   formula  C  H  O  Weight (g/mol)
    0            1  C2H5(OH)  2  6  1          46.069
    1            3        O2  0  0  2          31.998
>>> eq.products
       coefficient formula  C  H  O  Weight (g/mol)
    0            2     CO2  1  0  2          44.009
    1            3     H2O  0  2  1          18.015
</pre>
There is a periodic table of elements avalable through another import
which is a <b><i>pandas.DataFrame</i></b><pre> 
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
Source for the periodic table of elements:<br>
IUPAC - International Union of Pure and Aplied Chemistry<br>
https://iupac.org/what-we-do/periodic-table-of-elements/<br>

<H3><u>Limitations</u></H3>
<ul>
<li>Does not include Rare earths, synthetetic elements, Rn, Fr & Ra.</li>
<li>Hidrates representations must have subindexes like Cu(SO4)(H2O)5<br>
          instead of prefixes like Cu(SO4)•5H2O</li>
</ul>