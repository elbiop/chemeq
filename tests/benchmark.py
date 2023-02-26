# -*- coding: utf-8 -*-
import time
import sys
import os

unbalanced_eq = open("unbalanced_equations.txt", 'r').read().split("\n")
balanced_eq = open("balanced_equations.txt", 'r').read().split("\n")

os.chdir("..")
ABS_PATH = os.getcwd() + os.sep + "source_code"
sys.path.insert(0, ABS_PATH)
os.chdir(ABS_PATH)

from chemeq import chemeq

os.chdir(ABS_PATH[:-11] + "tests")


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
            print(f"Error: {error}")
    total = time.time()-initial
    print(f"\n\nTotal time = {total:.4f}")
    print(f"Average equation time = {total/80:.3f}")
    print(f"Succeded: {success} times")
    print(f"Failed: {fails} times")


if __name__ == "__main__":
    main()
