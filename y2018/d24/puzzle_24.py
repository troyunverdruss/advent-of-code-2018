from helpers.helpers import read_raw_entries
import re


class ArmyGroup:
    def __init__(self, id, display_id, type, units, hp, attack_strength, attack_type, initiative):
        self.id = id
        self.display_id = display_id
        self.type = type
        self.units = int(units)
        self.hp = int(hp)
        self.weak_to = []
        self.immune_to = []
        self.attack_strength = int(attack_strength)
        self.attack_type = attack_type
        self.initiative = int(initiative)

    def effective_power(self):
        return self.units * self.attack_strength

    def get_enemy(self):
        if self.type == 'imm':
            return 'inf'
        return 'imm'

    def potential_damage(self, other):
        if other.attack_type in self.immune_to:
            return 0
        if other.attack_type in self.weak_to:
            return other.effective_power() * 2
        return other.effective_power()

    def attack(self, other):
        if self.units <= 0:
            print('Group was killed, not attacking. {}:{}'.format(self.type, self.display_id))
            return

        damage = other.potential_damage(self)

        units_killed = damage // other.hp
        other.units -= units_killed
        print('Army {}:{} attacks {}:{} and deals {} damage, killing {} units'.format(self.type, self.display_id, other.type, other.display_id, damage, units_killed))


def parse_input(input):
    entries = read_raw_entries(input)

    pattern = re.compile(
        r'(\d+) units each with (\d+) hit points \((.*)\) with an attack that does (\d+) (\w+) damage at initiative (\d+)')

    results = []

    current_army = None
    id = 0
    display_id = 0
    for entry in entries:
        if entry.startswith('Immune System'):
            current_army = 'imm'
            display_id = 1
        elif entry.startswith('Infection'):
            current_army = 'inf'
            display_id = 1

        matcher = pattern.match(entry)
        if matcher:
            units = matcher.group(1)
            hp = matcher.group(2)
            special_details = matcher.group(3)
            attack_strength = matcher.group(4)
            attack_type = matcher.group(5)
            initiative = matcher.group(6)

            a = ArmyGroup(id, display_id, current_army, units, hp, attack_strength, attack_type, initiative)
            special = parse_special(special_details)
            a.immune_to = special['immune']
            a.weak_to = special['weak']

            results.append(a)
            id += 1
            display_id += 1

    return results


def parse_special(special_str):
    results = {
        'immune': [],
        'weak': []
    }
    pattern = re.compile(r'\s*(immune|weak) to (.*)')

    for special in special_str.split(';'):
        matcher = pattern.match(special)

        if matcher:
            for s in matcher.group(2).split(','):
                results[matcher.group(1)].append(s.strip())

    return results


def run_round(armies, army_lookup):
    for army in armies:
        print('Army {}:{} has {} units'.format(army.type, army.display_id, army.units))

    targets = {}
    target_selection_order = sorted(filter(lambda a: a.units > 0, armies), key=lambda a: (a.effective_power(), a.initiative), reverse=True)
    print('Target selection order:')
    for a in target_selection_order:
        print('{}:{} {}, {}'.format(a.type, a.display_id, a.effective_power(), a.initiative))

    for army in target_selection_order:
        # find target
        potential_targets = sorted(filter(lambda a: a.type == army.get_enemy() and a.units > 0, armies),
                   key=lambda a: (a.potential_damage(army), a.effective_power(), a.initiative), reverse=True)

        print('')
        print('Potential targets:')
        for a in potential_targets:
            print('{}:{} would deal {} damage to {}:{} [{}, {}]'.format(army.type, army.display_id, a.potential_damage(army), a.type, a.display_id, a.effective_power(), a.initiative))

        for enemy in potential_targets:

            if enemy.id in targets.values() or enemy.potential_damage(army) == 0:
                continue

            print('Army {}:{} [{}, {}] targets {}:{} [{}, {}, {}]'.format(army.type, army.display_id, army.effective_power(), army.initiative, enemy.type, enemy.display_id, enemy.potential_damage(army), enemy.effective_power(), enemy.initiative))
            targets[army.id] = enemy.id
            break

    # attack
    print('')
    for army in sorted(armies, key=lambda a: a.initiative, reverse=True):
        if army.id in targets:
            army.attack(army_lookup[targets[army.id]])


def solve_24(armies):
    army_lookup = {}
    for army in armies:
        army_lookup[army.id] = army

    round = 0
    immune = list(filter(lambda a: a.type == 'imm', armies))
    infection = list(filter(lambda a: a.type == 'inf', armies))

    while len(immune) > 0 and len(infection) > 0:
        round += 1
        print('')
        print('Round {}'.format(round))
        run_round(armies, army_lookup)

        # Clean up dead armies
        imm_units = 0
        for army in immune:
            if army.units <= 0:
                immune.remove(army)
            else:
                imm_units += army.units

        inf_units = 0
        for army in infection:
            if army.units <= 0:
                infection.remove(army)
            else:
                inf_units += army.units

        print('End of round: {} Imm: {}, Inf: {}'.format(round, imm_units, inf_units))
        if len(immune) <= 0 or len(infection) <= 0:
            break

    result = 0
    for army in armies:
        if army.units > 0:
            result += army.units

    return result


if __name__ == '__main__':
    armies = parse_input('input.txt')
    units = solve_24(armies)
    print('Surviving units: {}'.format(units))

    # 32167 too low
    # 32179 too low
    # 38008 -> maybe?

# Possible correct data
# End of round: 1 Imm: 24188, Inf: 43250
# End of round: 2 Imm: 24096, Inf: 43201
# End of round: 3 Imm: 24003, Inf: 43155
# End of round: 4 Imm: 23910, Inf: 43109
# End of round: 5 Imm: 23818, Inf: 43064
# End of round: 6 Imm: 23726, Inf: 43019
# End of round: 7 Imm: 23634, Inf: 42975
# End of round: 8 Imm: 23542, Inf: 42931
# End of round: 9 Imm: 23450, Inf: 42887
# End of round: 10 Imm: 23359, Inf: 42844