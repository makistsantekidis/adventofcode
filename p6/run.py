from collections import defaultdict

if __name__ == '__main__':
    with open('inputs.txt') as f:
        inputs = f.read()
    orbit_defs = inputs.splitlines(keepends=False)

    orbitmap = defaultdict(list)
    reverse_map = dict()
    for orbit in orbit_defs:
        a, b = orbit.split(')')
        orbitmap[a].append(b)
        reverse_map[b] = a


    # def recursive_count(planet, count):
    #     if planet in orbitmap:
    #         return sum([recursive_count(pl, count + 1) for pl in orbitmap[planet]], count)
    #     else:
    #         return count
    #
    #
    # print(recursive_count('COM', 0))
    def cost_dict(planet):
        me_dict = dict()
        planet
        cost = 1
        while planet != 'COM':
            orbit_pl = reverse_map[planet]
            me_dict[orbit_pl] = cost
            cost += 1
            planet = orbit_pl
        return me_dict


    you_dict = cost_dict('YOU')
    san_dict = cost_dict('SAN')
    for k in you_dict.keys():
        if k in san_dict:
            break
    print(you_dict[k], san_dict[k])
