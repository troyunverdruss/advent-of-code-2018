from collections import deque


def solve_14a(target_length):
    recipes = deque([3, 7])
    elf_one = 0
    elf_two = 1

    while len(recipes) < target_length + 10:
        sum = recipes[elf_one] + recipes[elf_two]
        tens = sum // 10
        ones = sum % 10

        if tens != 0:
            recipes.append(tens)
        recipes.append(ones)

        elf_one = (elf_one + recipes[elf_one] + 1) % len(recipes)
        elf_two = (elf_two + recipes[elf_two] + 1) % len(recipes)

    result = ''
    for i in range(target_length, target_length + 10):
        result += str(recipes[i])

    return result


def solve_14b(target_length):
    target_group = []

    for d in list(str(target_length)):
        target_group.append(int(d))

    recipes = [3, 7]
    elf_one = 0
    elf_two = 1

    while True:
        sum = recipes[elf_one] + recipes[elf_two]
        tens = sum // 10
        ones = sum % 10

        if tens != 0:
            recipes.append(tens)
        recipes.append(ones)

        elf_one = (elf_one + recipes[elf_one] + 1) % len(recipes)
        elf_two = (elf_two + recipes[elf_two] + 1) % len(recipes)

        if target_group == recipes[-(len(target_group)):]:
            return len(recipes) - len(target_group)
        if tens != 0 and target_group == recipes[-(len(target_group)) - 1:-1]:
            return len(recipes) - len(target_group) - 1


if __name__ == '__main__':
    r = solve_14a(846601)
    print('Next 10 recipes: {}'.format(r))

    r = solve_14b(846601)
    print('Number of preceding recipes: {}'.format(r))
    # Next 10 recipes: 3811491411
    # Number of preceding recipes: 20408083