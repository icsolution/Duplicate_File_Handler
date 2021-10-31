import sys
import os
import hashlib

path = sort_option = None
search_results = {}
duplicate_results = {}


def main():
    search_path()
    show_results(search_results)
    check_duplicates(search_results, duplicate_results)
    delete_duplicates(duplicate_results)


def search_path():
    global path
    try:
        args = sys.argv
        path = args[1]
        os.system(
            "mv  module/root_folder/files/stage/src/reviewSlider.js module/root_folder/files/stage/src/reviewslider.js")
        os.system(
            "mv module/root_folder/files/stage/src/toggleMiniMenu.js module/root_folder/files/stage/src/toggleminimenu.js")
    except:
        print('Directory is not specified')
        quit()


def show_results(results):
    global path, sort_option
    file_type = input('\nEnter file format:\n')
    for root, dirs, files in os.walk(path):
        for file in files:
            if file_type in file:
                name = os.path.join(root, file)
                size = os.path.getsize(name)
                hash = get_file_hash(name)
                if size not in results:
                    results[size] = []
                    results[size].append([name, hash])
                else:
                    results[size].append([name, hash])
    results = sort_options(results)
    print()
    for size, files in results:
        print(f'{size} bytes')
        for file in files:
            print(file[0])
        print()


def get_file_hash(file):
    with open(file, 'rb') as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
        return file_hash


def sort_options(results):
    global sort_option
    if not sort_option:
        print('\nSize sorting options:\n1. Descending\n2. Ascending\n')
        sort_option = input('Enter a sorting option:\n')
    if sort_option == '1':
        return sorted(results.items(), reverse=True)
    elif sort_option == '2':
        return sorted(results.items())
    else:
        print('\nWrong option\n')
        sort_option = None
        sort_options(results)


def check_duplicates(results, duplicates):
    print('Check for duplicates?\n')
    option = input().lower()
    if option not in ['yes', 'no']:
        print('Wrong option')
        check_duplicates(results, duplicates)
    elif option == 'no':
        quit()
    else:
        print()
        for size, files in results.items():
            hash_files = [file[1] for file in files]
            if len(files) > 1:
                duplicates[size] = []
                for duplicate_hash in set(hash_files):
                    if hash_files.count(duplicate_hash) > 1:
                        duplicates[size].append(f'Hash: {duplicate_hash}')
                        for item in files:
                            if item[1] == duplicate_hash:
                                duplicates[size].append(item[0])
        duplicates = sort_options(duplicates)
        count = 1
        for size, files in duplicates:
            print(f'{size} bytes')
            index = 1
            for item in files:
                if 'Hash' in item:
                    print(item)
                else:
                    files[index] = f'{count}. {item}'
                    print(files[index])
                    count += 1
                    index += 1
            print()


def delete_duplicates(duplicates):
    print('Delete files?\n')
    option = input().lower()
    if option not in ['yes', 'no']:
        print('Wrong option')
        delete_duplicates(duplicates)
    elif option == 'no':
        quit()
    else:
        delete_files(duplicates)


def delete_files(duplicates):
    print('\nEnter file numbers to delete:')
    option = input().split()
    memory = complete = 0
    for target in option:
        for size, files in duplicates.items():
            for file in files:
                if target in file[0]:
                    complete += 1
                    memory += size
                    os.remove(file[3:])
                else:
                    pass
    if option and complete == len(option):
        print(f'\nTotal freed up space: {memory} bytes')
    else:
        print('\nWrong option')
        delete_files(duplicates)


if __name__ == '__main__':
    main()
