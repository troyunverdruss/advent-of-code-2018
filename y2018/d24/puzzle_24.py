import sys

sys.path.append('/Users/troy/Documents/code/advent-of-code')
from helpers.helpers import read_raw_entries
import re


class ArmyGroup:
    def __init__(self, id, display_id, type, units, hp, weak_to, immune_to, attack_strength, attack_type, initiative):
        self.id = id
        self.display_id = display_id
        self.type = type
        self.units = int(units)
        self.hp = int(hp)
        self.weak_to = weak_to
        self.immune_to = immune_to
        self.attack_strength = int(attack_strength)
        self.attack_type = attack_type
        self.initiative = int(initiative)

    def __str__(self):
        return '{} {} {} {} {} {} {} {}'.format(
            self.type,
            self.units,
            self.hp,
            self.weak_to,
            self.immune_to,
            self.attack_strength,
            self.attack_type,
            self.initiative
        )

    def __eq__(self, other):
        return self.id == other.id and self.display_id == other.display_id \
               and self.type == other.type and self.units == other.units \
               and self.hp == other.hp and self.weak_to == other.weak_to \
               and self.immune_to == other.immune_to and self.attack_strength == other.attack_strength \
               and self.attack_type == other.attack_type and self.initiative == other.initiative

    def effective_power(self):
        return self.units * self.attack_strength

    def get_enemy(self):
        if self.type == 'imm':
            return 'inf'
        return 'imm'

    def targeting_priority(self):
        return -self.effective_power(), -self.initiative

    def attack_priority(self):
        return -self.initiative

    def damage_priority(self, other):
        if other.units == 0:
            return 0, 0, 0
        if self.get_enemy() != other.type:
            return 0, 0, 0
        if self.attack_type in other.immune_to:
            return 0, 0, 0

        if self.attack_type in other.weak_to:
            damage = self.effective_power() * 2
        else:
            damage = self.effective_power()

        return damage, other.effective_power(), other.initiative

    def select_target(self, targets, others):
        sorted_targets = sorted(filter(lambda o: self.damage_priority(o)[0] > 0, others),
                                key=lambda o: self.damage_priority(o),
                                reverse=True)
        for a in sorted_targets:
            if a.id in targets.values():
                continue

            targets[self.id] = a.id
            break

    def attack(self, other):
        if self.units <= 0:
            return

        damage = self.damage_priority(other)[0]

        units_killed = damage // other.hp
        other.units = max(0, other.units - units_killed)


def run_round(armies, army_lookup):
    targets = {}

    # selection
    for army in sorted(armies, key=lambda a: a.targeting_priority()):
        army.select_target(targets, armies)

    # attack
    for army in sorted(armies, key=lambda a: a.attack_priority()):
        if army.id in targets:
            army.attack(army_lookup[targets[army.id]])


def solve_24(armies, boost=0):
    army_lookup = {}
    for army in armies:
        army_lookup[army.id] = army
        if army.type == 'imm':
            army.attack_strength += boost

    round = 0
    immune = list(filter(lambda a: a.type == 'imm', armies))
    infection = list(filter(lambda a: a.type == 'inf', armies))

    stalemate_count = 0
    imm_units = 0
    inf_units = 0
    last_total_units = sum(map(lambda a: a.units, armies))
    while len(immune) > 0 and len(infection) > 0:
        round += 1
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

        if len(immune) <= 0 or len(infection) <= 0:
            break

        if imm_units != 0 and inf_units != 0 and imm_units + inf_units == last_total_units:
            print('Stalemate with boost {}. Imm {} Inf {}'.format(boost, imm_units, inf_units))
            stalemate_count += 1
        else:
            stalemate_count = 0
        last_total_units = imm_units + inf_units

        if stalemate_count > 2:
            break

    print('Final counts: imm: {} inf: {}'.format(imm_units, inf_units))

    result = 0
    for army in armies:
        if army.units > 0:
            result += army.units

    immune_system_wins = False
    if len(immune) > 0 and len(infection) == 0:
        immune_system_wins = True

    return result, immune_system_wins


def parse_input(entries):
    pattern = re.compile(
        r'(\d+) units each with (\d+) hit points(.*)with an attack that does (\d+) (\w+) damage at initiative (\d+)')

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

            special = parse_special(special_details)
            a = ArmyGroup(id, display_id, current_army, units, hp, special['weak'], special['immune'], attack_strength,
                          attack_type, initiative)

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
        special = special.replace('(', '')
        special = special.replace(')', '')
        matcher = pattern.match(special)

        if matcher:
            for s in matcher.group(2).split(','):
                results[matcher.group(1)].append(s.strip())

    return results


if __name__ == '__main__':
    entries = read_raw_entries(__file__, 'input.txt')
    armies = parse_input(entries)
    units, immune_system_wins = solve_24(armies)
    print('Surviving units: {}'.format(units))
    if immune_system_wins:
        print('Immune system wins!')
    else:
        print('Immune system loses :(')

    boost = 0
    while not immune_system_wins:
        boost += 1
        armies = parse_input(entries)
        units, immune_system_wins = solve_24(armies, boost)

    print('Immune system wins with boost: {}, leaving: {} units'.format(boost, units))
