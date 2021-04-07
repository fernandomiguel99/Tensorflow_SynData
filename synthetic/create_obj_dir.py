#!/usr/bin/python
#!coding: utf-8
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=
        'Create directories for all object classes in a .txt to put the images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Example usage:
    python {0} -i /home/user/example/classes.txt -o /home/user/example/objects/'''.format(__file__))
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        help=
        'Path to the .txt file with all the classes, one per line.'
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        help=
        'Path to the directory where all the other directories will be created.'
    )

    args = parser.parse_args()
    indirectory = args.input
    outdirectory = args.output

    # read txt into a list, splitting by newlines
    data = [
        l.rstrip('\n').strip()
        for l in open(indirectory, 'r', encoding='utf-8-sig')
    ]

    data = [l for l in data if len(l) > 0]

    for cl in data:
        os.makedirs(os.path.join(outdirectory,cl))
