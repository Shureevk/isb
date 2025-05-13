import random


def generate_random_binary_sequence(length=128):
    return "".join(random.choice("01") for _ in range(length))


if __name__ == "__main__":
    sequence = generate_random_binary_sequence()
    print("Случайная 128-битная бинарная последовательность:", sequence)

    with open("python_sequence.txt", "w") as f:
        f.write(sequence)
    print("Последовательность сохранена в файл python_sequence.txt")
