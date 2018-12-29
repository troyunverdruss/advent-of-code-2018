class Group:
    def __init__(self, side, line, boost=0):
        self.side = side

        attribs, attack = line.split(';')
        units, hp, *type_mods = attribs.split()
        units = int(units)
        hp = int(hp)
        weak = []
        immune = []
        cur = None
        for w in type_mods:
            if w == "weak":
                cur = weak
            elif w == "immune":
                cur = immune
            else:
                cur.append(w)

        self.units = units
        self.hp = hp
        self.weak = weak
        self.immune = immune

        attack_amount, attack_type, initiative = attack.split()
        attack_amount = int(attack_amount)
        initiative = int(initiative)

        self.attack = attack_amount + boost
        self.attack_type = attack_type
        self.initiative = initiative

        self.attacker = None
        self.target = None

        print(self)

    def __str__(self):
        return '{} {} {} {} {} {} {} {}'.format(
            self.side,
            self.units,
            self.hp,
            self.weak,
            self.immune,
            self.attack,
            self.attack_type,
            self.initiative
        )

    def clear(self):
        self.attacker = None
        self.target = None

    def choose(self, groups):
        assert self.target is None
        cands = [group for group in groups
                 if group.side != self.side
                 and group.attacker is None
                 and self.damage_prio(group)[0] > 0]
        if cands:
            self.target = max(cands, key=lambda group: self.damage_prio(group))
            assert self.target.attacker is None
            self.target.attacker = self
            print('{} targets \n{}'.format(self, self.target))

    def effective_power(self):
        return self.units * self.attack

    def target_prio(self):
        return (-self.effective_power(), -self.initiative)

    def damage_prio(self, target):
        if target.units == 0:
            return (0, 0, 0)
        if self.attack_type in target.immune:
            return (0, 0, 0)
        mul = 1
        if self.attack_type in target.weak:
            mul = 2
        return (mul * self.units * self.attack, target.effective_power(), target.initiative)

    def do_attack(self, target):
        total_attack = self.damage_prio(target)[0]
        killed = total_attack // target.hp
        target.units = max(0, target.units - killed)

        print('Army {}:{}:{} attacks {}:{} and deals {} damage, killing {} units'.format(self.initiative, self.side, 0,
                                                                                      target.side, 1,
                                                                                      total_attack, killed))

                                                                                      # immune_system_input = """17 5390 weak radiation bludgeoning;4507 fire 2
# 989 1274 immune fire weak bludgeoning slashing;25 slashing 3"""
#
# infection_input = """801 4706 weak radiation;116 bludgeoning 1
# 4485 2961 immune radiation weak fire cold;12 slashing 4"""

immune_system_input = '''5711 6662 immune fire weak slashing;9 bludgeoning 14
2108 8185 weak radiation bludgeoning;36 slashing 13
1590 3940;24 cold 5
2546 6960;25 slashing 2
1084 3450 immune bludgeoning;27 slashing 11
265 8223 immune radiation bludgeoning cold;259 cold 12
6792 6242 immune slashing weak bludgeoning radiation;9 slashing 18
3336 12681 weak slashing;28 fire 6
752 5272 immune slashing weak bludgeoning radiation;69 radiation 4
96 7266 immune fire;738 bludgeoning 8'''

infection_input = '''1492 47899 weak fire slashing immune cold;56 bludgeoning 15
3065 39751 weak bludgeoning slashing;20 slashing 1
7971 35542 weak bludgeoning radiation;8 bludgeoning 10
585 5936 weak cold immune fire;17 slashing 17
2449 37159 immune cold;22 cold 7
8897 6420 immune bludgeoning slashing fire weak radiation;1 bludgeoning 19
329 31704 weak fire immune cold radiation;179 bludgeoning 16
6961 11069 weak fire;2 radiation 20
2837 29483 weak cold;20 bludgeoning 9
8714 7890;1 cold 3'''


def solve(boost):
    immune_system_groups = [Group(False, line, boost) for line in immune_system_input.split("\n")]
    infection_groups = [Group(True, line) for line in infection_input.split("\n")]

    groups = immune_system_groups + infection_groups

    old = (-1, -1)
    round = 0
    while True:
        round += 1
        groups = sorted(groups, key=lambda group: group.target_prio())
        for group in groups:
            group.clear()
        for group in groups:
            group.choose(groups)
        groups = sorted(groups, key=lambda group: -group.initiative)
        for group in groups:
            if group.target:
                group.do_attack(group.target)

        immune_system_units = sum(group.units for group in groups if group.side == False)
        infection_units = sum(group.units for group in groups if group.side == True)

        print('End of round: {} Imm: {}, Inf: {}'.format(round, immune_system_units, infection_units))

        if (immune_system_units, infection_units) == old:
            return (immune_system_units, infection_units)
        old = (immune_system_units, infection_units)


# star 1
print(solve(0)[1])

# star 2
for boost in range(1000000):
    ans = solve(boost)
    if ans[1] == 0:
        print(ans[0])
        break
