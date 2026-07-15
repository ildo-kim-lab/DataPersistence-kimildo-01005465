def print_header(title):
    print()
    print("=" * 40)
    print(title)
    print("=" * 40)


def read_input(prompt):
    return input(prompt).strip()


def read_int(prompt):
    while True:
        value = read_input(prompt)
        if value.lstrip("-").isdigit():
            return int(value)
        print("숫자를 입력해주세요.")


def read_float(prompt):
    while True:
        value = read_input(prompt)
        try:
            return float(value)
        except ValueError:
            print("숫자를 입력해주세요.")
