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
    for army in sorted(armies, key=lambda a: (a.effective_power(), a.initiative), reverse=True):
        # find target
        for enemy in sorted(
                filter(lambda a: a.type == army.get_enemy(), armies),
                key=lambda a: (a.potential_damage(army), a.effective_power(), a.initiative), reverse=True):

            if enemy.id in targets.values():
                continue

            print('Army {}:{} targets {}:{}'.format(army.type, army.display_id, enemy.type, enemy.display_id))
            targets[army.id] = enemy.id
            break

    # attack
    for army in sorted(armies, key=lambda a: a.initiative, reverse=True):
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
        print('Round {}'.format(round))
        run_round(armies, army_lookup)

        # Clean up dead armies
        for army in immune:
            if army.units <= 0:
                immune.remove(army)

        for army in infection:
            if army.units <= 0:
                infection.remove(army)

        if len(immune) <= 0 or len(infection) <= 0:
            break

    result = 0
    for army in armies:
        if army.units > 0:
            result += army.units

    return result


if __name__ == '__main__':
    armies = parse_input('input.txt')
    i = 0
