from collections import deque


def solve_14(target_length):
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


if __name__ == '__main__':
    r = solve_14(846601)
    print('Next 10 recipes: {}'.format(r))
