from collections import defaultdict
import numpy as np

if __name__ == '__main__':
    inputs = open('inputs.txt').read()
    recipes = inputs.splitlines()
    elements = set()
    recipe_dict = dict()
    for rec in recipes:
        recin, recout = rec.split(' => ')
        recout_nb, recout_el = recout.split(' ')
        recipe_dict[recout_el] = (int(recout_nb), [rcomp.split(' ') for rcomp in recin.split(', ')])
        for recin_comp in recin.split(', '):
            elements.add(recin_comp.split(' ')[1])
        elements.add(recout.split(' ')[1])
    requirements = defaultdict(lambda: 0)
    requirements['FUEL'] = 2509120 # bruteforced this by hand. Shameful.
    done_flag = False
    while list(requirements.keys()) != ['ORE']:
        for rkey, rval in list(requirements.items()):
            if rkey == 'ORE' or rval <= 0:
                continue
            recipe = recipe_dict[rkey]
            mult = 1
            if rval > recipe[0]:
                mult = np.ceil(rval / recipe[0])
            for nb_comp, comp in recipe[1]:
                requirements[comp] += int(nb_comp) * mult
            requirements[rkey] -= mult * recipe[0]
        ore_flag = False
        for key, val in list(requirements.items()):
            if val == 0:
                del requirements[key]
            if key != 'ORE' and val > 0:
                ore_flag = True
        if 'ORE' in requirements and not ore_flag:
            break

    print(requirements['ORE'])
