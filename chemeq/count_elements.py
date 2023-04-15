import re


def count_elements(compound, elements):
    '''counts the number of appearances of a list of elements in a compound

     param compound: type str. Chemical compound.
     param elements: list[str], symbols for all chemical elements
     return: compound without witout prefix (molar value),
              prefix (molar value) or 1 if not present,
              elements count per one molecule.
     rtype: str, int, list[int]

     examples
     --------
         >>> count_elements("H2O",['H','O'])
         ('H2O', 1, [2, 1])
         >>> count_elements("3Cu(CO3)(OH)2",['C', 'Cu', 'H', 'O'])
         ('Cu(CO3)(OH)2', 3, [1, 1, 2, 5])
     '''
    original_comp = compound
    subindexes = [0 for _ in range(len(elements))]
    # find if a compound begins with a number
    coeff = re.findall(r"^[0-9]+(?=[A-Z]|\()", compound)
    if len(coeff):
        trim = len(coeff[0])
        compound = compound[trim:]
        coeff = int(coeff[0])
    else:
        trim = 0
        coeff = 1

    # find groups that are between parentheses and separate them into subgroups
    # iterate over each subgroup of the compound
    pattern = re.compile(r"(\()([A-Z]+[a-z]*[0-9]*)+(\))[0-9]*")
    subgroups = [x.group() for x in pattern.finditer(compound)]
    for subgroup in subgroups:
        compound = compound.replace(subgroup, "")
    if len(compound):
        subgroups = [compound] + subgroups
    subgroups = [x.replace("(", "") for x in subgroups]
    for subgroup in subgroups:
        group_sub_ix = 1
        if subgroup.find(")") > 0:
            subgroup, remain = subgroup.split(")")
            if len(remain):
                group_sub_ix = int(remain)
        '''find the element that is followed by 0 or more numbers and
        without retrieval not followed by lowercase to avoid false positive
        of single letters elements with two letter elements that begin with
        the same letter'''
        # add whitespace to comply with the regex in case of no sub index
        subgroup += " "
        for k, el in enumerate(elements):
            # Find uppercases followed or not by a number and (do not include)
            # not followed by lowercase letters,
            pattern = re.compile(f'{el}' + '{1}[0-9]*(?=[^a-z])')
            matches = list(pattern.finditer(subgroup))
            for m in matches:
                # if match is not followed by numbers add 1
                # if is add that number"
                if len(m.group()[len(el):]):
                    subindexes[k] += group_sub_ix*int(m.group()[len(el):])
                else:
                    subindexes[k] += group_sub_ix
    return(original_comp[trim:], coeff, subindexes)
