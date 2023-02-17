# -*- coding: utf-8 -*-
import time
import sys
import os

unbalanced_eq = open("unbalanced_equations.txt", 'r').read().split("\n")
balanced_eq = open("balanced_equations.txt", 'r').read().split("\n")
ABS_PATH = os.getcwd()[:-5] + "source_files"
sys.path.insert(0, ABS_PATH)
os.chdir(ABS_PATH)

from chemeq import chemeq

os.chdir(ABS_PATH[:-12] + "tests")


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
                original = f"::balanced Correctly::\nOriginal: {text}\n"
                result = original + f"Result:   {str(eq)}\n"
            else:
                fails += 1
                result = f"Failed!    <<<<<{eq}>>>>  <<<<{balanced_eq[i]}>>>"
            print(result)
        except Exception as error:
            print(f"Error: {error}")
    total = time.time()-initial
    print(f"\n\nTotal time = {total:.4f}")
    print(f"Average equation time = {total/80:.3f}")
    print(f"Succeded: {success} times")
    print(f"Failed: {fails} times")


if __name__ == "__main__":
    main()
