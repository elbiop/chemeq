# -*- coding: utf-8 -*-
import time
import sys
import os

PATH = os.path.abspath("..") + f"{os.sep}tests{os.sep}"
with open(f"{PATH}unbalanced_equations.txt", 'r') as file:
    unbalanced_eq = file.read().split("\n")
with open(f"{PATH}balanced_equations.txt", 'r') as file:
    balanced_eq = file.read().split("\n")

PATH = os.path.abspath("..") + os.sep + "chemeq"
sys.path.insert(0, PATH )
os.chdir(PATH)

from chemeq import chemeq

def main():
    initial = time.time()
    success = 0
    fails = 0
    for i, text in enumerate(unbalanced_eq):
        eq = chemeq(text)
        text = str(eq)
        try:
            eq.balance()
            if str(eq) == balanced_eq[i]:
                success += 1
                header = "  :: balanced Correctly ::"
            else:
                fails += 1
                header = "\n\n!!!!!!!!!!!!!!   Failed   !!!!!!!!!!!!!!"
            print(header + f'\nOriginal: {text}\nResult   {str(eq)}\n')
            
        except Exception as error:
            print(error)
    total = time.time()-initial
    print(f"\n\nTotal time = {total:.4f}")
    print(f"Average equation time = {total/80:.3f}")
    print(f"Succeded: {success} times")
    print(f"Failed: {fails} times")


if __name__ == "__main__":
    main()
