# create periodic table file
import os
import sys
from importlib import util

PERIODIC_TABLE_CONTENT = """Source for the periodic table of elements:
IUPAC - International Union of Pure and Applied Chemistry
https://iupac.org/what-we-do/periodic-table-of-elements/

z,name,symbol,atomic_mass,error,group,period,state
1,Hydrogen,H,1.008,0.0002,1,1,g
2,Helium,He,4.0026,0.0001,18,1,g
3,Lithium,Li,6.94,0.06,1,2,s
4,Beryllium,Be,9.0122,0.0001,2,2,s
5,Boron,B,10.81,0.02,13,2,s
6,Carbon,C,12.011,0.002,14,2,s
7,Nitrogen,N,14.007,0.001,15,2,g
8,Oxygen,O,15.999,0.001,16,2,g
9,Fluorine,F,18.998,0.001,17,2,g
10,Neon,Ne,20.18,0.001,18,2,g
11,Sodium,Na,22.99,0.001,1,3,s
12,Magnesium,Mg,24.305,0.002,2,3,s
13,Aluminum,Al,26.982,0.001,13,3,s
14,Silicon,Si,28.085,0.001,14,3,s
15,Phosphorus,P,30.974,0.001,15,3,s
16,Sulfur,S,32.06,0.02,16,3,s
17,Chlorine,Cl,35.45,0.01,17,3,g
18,Argon,Ar,39.95,0.16,18,3,g
19,Potassium,K,39.098,0.001,1,4,s
20,Calcium,Ca,40.078,0.004,2,4,s
21,Scandium,Sc,44.956,0.001,3,4,s
22,Titanium,Ti,47.867,0.001,4,4,s
23,Vanadium,V,50.942,0.001,5,4,s
24,Chromium,Cr,51.996,0.001,6,4,s
25,Manganese,Mn,54.938,0.001,7,4,s
26,Iron,Fe,55.845,0.002,8,4,s
27,Cobalt,Co,58.933,0.001,9,4,s
28,Nickel,Ni,58.693,0.001,10,4,s
29,Copper,Cu,63.546,0.003,11,4,s
30,Zinc,Zn,65.38,0.02,12,4,s
31,Gallium,Ga,69.723,0.001,13,4,s
32,Germanium,Ge,72.63,0.008,14,4,s
33,Arsenic,As,74.922,0.001,15,4,s
34,Selenium,Se,78.971,0.008,16,4,s
35,Bromine,Br,79.904,0.003,17,4,l
36,Krypton,Kr,83.798,0.002,18,4,g
37,Rubidium,Rb,85.468,0.001,1,5,s
38,Strontium,Sr,87.62,0.01,2,5,s
39,Yttrium,Y,88.906,0.001,3,5,s
40,Zirconium,Zr,91.224,0.002,4,5,s
41,Niobium,Nb,92.906,0.001,5,5,s
42,Molybdenum,Mo,95.95,0.01,6,5,s
44,Ruthenium,Ru,101.07,0.02,8,5,s
45,Rhodium,Rh,102.91,0.01,9,5,s
46,Palladium,Pd,106.42,0.01,10,5,s
47,Silver,Ag,107.87,0.01,11,5,s
48,Cadmium,Cd,112.41,0.01,12,5,s
49,Indium,In,114.82,0.01,13,5,s
50,Tin,Sn,118.71,0.01,14,5,s
51,Antimony,Sb,121.76,0.01,15,5,s
52,Tellurium,Te,127.6,0.03,16,5,s
53,Iodine,I,126.9,0.01,17,5,s
54,Xenon,Xe,131.29,0.01,18,5,g
55,Cesium,Cs,132.91,0.01,1,6,s
56,Barium,Ba,137.33,0.01,2,6,s
72,Hafnium,Hf,178.49,0.01,4,6,s
73,Tantalum,Ta,180.95,0.01,5,6,s
74,Tungsten,W,183.84,0.01,6,6,s
75,Rhenium,Re,186.21,0.01,7,6,s
76,Osmium,Os,190.23,0.03,8,6,s
77,Iridium,Ir,192.22,0.01,9,6,s
78,Platinum,Pt,195.08,0.02,10,6,s
79,Gold,Au,196.97,0.01,11,6,s
80,Mercury,Hg,200.59,0.01,12,6,l
81,Thallium,Tl,204.38,0.01,13,6,s
82,Lead,Pb,207.2,1.1,14,6,s
83,Bismuth,Bi,208.98,0.01,15,6,s"""


CURRENT_PATH = os.path.abspath(".")
installed = util.find_spec("chemeq")

# Different imports if package is installed or in source directory
if installed.has_location:
    # if installed run installed version
    INSTALLATION_PATH = installed.submodule_search_locations[0] + os.sep
    os.chdir(INSTALLATION_PATH)
    if "periodic_table.csv" not in os.listdir():
        with open('periodic_table.csv', 'w') as pt:
            pt.write(PERIODIC_TABLE_CONTENT)

    # shorten import paths
    from chemeq.equation_balancer import chemeq
    from chemeq.equation_balancer import periodic_table
    from chemeq.syntax_review import syntax_review
    from chemeq.count_elements import count_elements
    os.chdir(CURRENT_PATH)
else:
    # if not installed run from source location
    sys.path.insert(0, CURRENT_PATH)
    from equation_balancer import chemeq
    from equation_balancer import periodic_table
    from syntax_review import syntax_review
    from count_elements import count_elements


__all__ = [
            "chemeq",
            "periodic_table",
            "count_elements",
            "syntax_review"
          ]
__author__ = "Elbio Peña Almonte"
