import os
import sys
import random


def main(args):
    if len(args) != 1:
        print('Usage: python dataset_split.py <data_dir>')
        return
    data_path = args[0]
    SEED = 0
    random.seed(SEED)

    file_name = os.path.basename(data_path)
    dir_name = os.path.dirname(data_path)

    with open(data_path, 'r', encoding='utf-8') as fi:
        lines = fi.readlines()

    random.shuffle(lines)
    n_total = len(lines)
    n_train = int(n_total * 0.8)
    n_valid = int(n_total * 0.1)
    n_test = n_total - n_train - n_valid

    train_lines = lines[:n_train]
    valid_lines = lines[n_train:n_train + n_valid]
    test_lines = lines[n_train + n_valid:]

    assert len(train_lines) + len(valid_lines) + len(test_lines) == n_total
    assert len(train_lines) == n_train
    assert len(valid_lines) == n_valid
    assert len(test_lines) == n_test

    file_name = file_name.replace('filtered_', '')
    train_output = os.path.join(dir_name, 'train_' + file_name)
    valid_output = os.path.join(dir_name, 'valid_' + file_name)
    test_output = os.path.join(dir_name, 'test_' + file_name)

    with open(train_output, 'w', encoding='utf-8') as fo:
        fo.writelines(train_lines)
    with open(valid_output, 'w', encoding='utf-8') as fo:
        fo.writelines(valid_lines)
    with open(test_output, 'w', encoding='utf-8') as fo:
        fo.writelines(test_lines)

    print(f'Number of total data: {n_total}')
    print(f'Number of train data: {n_train}')
    print(f'Number of valid data: {n_valid}')
    print(f'Number of test data: {n_test}')


if __name__ == '__main__':
    main(sys.argv[1:])
