#!/usr/bin/env python3

"""
i18n
~~~~

A tool for internationalization in iOS projects.

Usage:
    1. Open terminal.
    2. Change directory to your project's root.
    3. Run 'path/i18n.py'.
    4. Run 'path/i18n.py -h' for more usage.

    'path' is the path from project's root to this script file.
"""

import os
import re
import config
from argparse import ArgumentParser
from subprocess import call
from utils import console
from utils import file_assistant


def _should_skip_line(line, commented=False):
    return line == '\n' or line.startswith('//') or commented


def _check_localiztion_format_files(file_paths):
    is_good_format = True
    for path in file_paths:
        is_good_format = _check_localiztion_format(path) and is_good_format
    if not is_good_format:
        console.print_fail('Checking localizable file failed.')
        exit(1)


def _check_localiztion_format(file_path):
    is_good_format = True
    with open(file_path, 'r') as source_file:
        commented = False
        for index, line in enumerate(source_file):
            if line.startswith('/*'):
                commented = True
                continue
            if '*/' in line:
                commented = False
                continue
            if _should_skip_line(line, commented):
                continue
            if not re.match(config.LOCALIZABLE_FORMAT_RE, line):
                console.print_warning('Error format in file:\n{}, line: {}'
                                      .format(file_path, index + 1))
                is_good_format = False
    return is_good_format


def _remove_duplicate_strings_files(file_paths):
    for path in file_paths:
        _remove_duplicate_strings(path)


def _remove_duplicate_strings(file_path):
    keys = []
    lines = []
    with open(file_path, 'r') as source_file:
        commented = False
        for line in source_file:
            if line.startswith('/*'):
                commented = True
                keys.append('')
                lines.append(line)
                continue
            if '*/' in line:
                commented = False
                keys.append('')
                lines.append(line)
                continue
            if _should_skip_line(line, commented):
                keys.append('')
                lines.append(line)
            else:
                matchs = re.findall(config.KEY, line)
                if matchs:
                    key = matchs[0]
                    if key not in keys:
                        keys.append(key)
                        lines.append(line)
                    else:
                        index = keys.index(key)
                        lines[index] = line
                        print('Duplicate key found in file:\n'
                              '%s line: %s' % (file_path, key))
    with open(file_path, 'w') as source_file:
        source_file.writelines(lines)


def _add_new_strings(old_files, new_files):
    new_string_paths = file_assistant.get_paths(
        new_files, names=config.LOCALIZABLE_FILE_NAMES)
    _check_localiztion_format_files(new_string_paths)
    _remove_duplicate_strings_files(new_string_paths)
    for path in new_string_paths:
        language = path.split('/')[-2]
        for old_path in old_files:
            if language in old_path:
                with open(old_path, 'a') as old_file:
                    with open(path, 'r') as new_file:
                        for line in new_file:
                            old_file.write(line)
    console.print_bold('%d localizable strings files added.'
                       % len(new_string_paths))


def _get_project_path(args):
    if args.path is None:
        return os.getcwd()
    else:
        return args.path


def _get_target_path(args):
    if args.output is None:
        return os.path.join(os.getcwd(), config.DEFAULT_TARGET_PATH)
    else:
        target_path = args.output
        try:
            target = open(target_path, 'w')
            target.close()
        except OSError:
            console.print_fail('Error: Invalid file path %s' % target_path)
            exit(1)
        return target_path


def _get_source_file_paths(path):
    source_file_paths = file_assistant.get_paths(
        path,
        types=config.SEARCH_TYPES,
        exclusive_paths=config.SOURCE_FILE_EXCLUSIVE_PATHS)
    if not source_file_paths:
        console.print_fail(
            'No source file found!\n'
            'Please change your current directory to project\'s root.')
        exit(1)
    return source_file_paths


def _get_localization_paths(path):
    localization_paths = file_assistant.get_paths(
        os.path.join(path, config.LOCALIZABLE_FILE_PATH),
        names=config.LOCALIZABLE_FILE_NAMES,
        types=config.LOCALIZABLE_FILE_TYPES,
        exclusive_paths=config.LOCALIZABLE_FILE_EXCLUSIVE_PATHS)
    if not localization_paths:
        console.print_fail('No localization file found!')
        exit(1)
    return localization_paths


def _get_all_localization_strings(path):
    all_localization_strings = set()
    for path in path:
        with open(path, 'r') as source_file:
            for line in source_file:
                strings = re.findall(config.LOCALIZABLE_RE, line)
                for string in strings:
                    name = string.replace(
                        config.SUFFIX,
                        '')
                    all_localization_strings.add(name)
    return all_localization_strings


def _find_unlocalized_strings(strings, paths):
    unlocalized_strings = set()
    for name in strings:
        for path in paths:
            if file_assistant.file_contains(path, name):
                continue
            else:
                print('{} not localized in {}'.format(name, path))
                break
        else:
            continue
        unlocalized_strings.add(name)
    return unlocalized_strings


def _generate_unlocalized_strings_file(strings, path):
    with open(path, 'w') as target:
        for name in sorted(strings):
            target.write('{0} = {0};\n'.format(name))
    call(['open', path])
    print('%d unlocalized strings found.' % len(strings))
    console.print_bold('Generated strings in path: %s' % path)


def _get_args():
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--integrate",
        help="integrate new localizable strings",
        type=str)
    parser.add_argument(
        "-o",
        "--output",
        help="set output file path",
        type=str)
    parser.add_argument(
        "-p",
        "--path",
        help="set project path",
        type=str)
    parser.add_argument(
        "-r",
        "--remove",
        help="remove duplicate localizable strings",
        action='store_true')
    return parser.parse_args()


def main():
    args = _get_args()

    project_path = _get_project_path(args)
    print('Current directory: ' + project_path)

    print('Checking localizable files...')
    localization_paths = _get_localization_paths(project_path)
    _check_localiztion_format_files(localization_paths)

    if args.remove:
        print('Removing duplicate localizable strings...')
        _remove_duplicate_strings_files(localization_paths)

    if args.integrate is not None:
        print('Adding new localizable strings...')
        _add_new_strings(localization_paths, args.integrate)
        exit(0)

    print('Finding unlocalized strings...')
    source_file_paths = _get_source_file_paths(project_path)
    all_localization_strings = _get_all_localization_strings(source_file_paths)
    unlocalized_strings = _find_unlocalized_strings(all_localization_strings,
                                                    localization_paths)

    if not unlocalized_strings:
        console.print_bold('No unlocalized string found.')
    else:
        target_path = _get_target_path(args)
        _generate_unlocalized_strings_file(unlocalized_strings, target_path)


if __name__ == "__main__":
    main()
