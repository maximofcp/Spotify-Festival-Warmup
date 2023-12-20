def chunks(lst: list, n: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def read_file(filename: str = 'festivals_.txt'):
    with open(f'data/{filename}') as f:
        return f.readlines()
