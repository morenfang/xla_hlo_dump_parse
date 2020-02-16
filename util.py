import os
import re


def list_all_files(dir):
    return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]


def not_empty_line(line):
    if len(line) > 1:  # \n is one char
        return True
    else:
        return False


def find_between_quotes(string):
    return re.findall('"([^"]*)"', string)


def find_between_brace(string):
    return re.findall(r'\{.*?\}', string)


def find_between_brackets(string, lhs_bracket, rhs_bracket):
    begin_idx = string.find(lhs_bracket) + 1
    end_idx = string.rfind(rhs_bracket)

    if begin_idx == -1 or end_idx == -1 or begin_idx >= end_idx:
        return ''
    else:
        return string[begin_idx:end_idx]


def findall_in_string(keyword, string, delimeter=' '):
    sub_strings = string.split(delimeter)
    results = [re.search(keyword, sub_string) for sub_string in sub_strings]
    return [item.string for item in results if item is not None]


def find_assignment_rhs(string):
    pos = string.find('=')
    string = string[pos+1:]
    string = string.strip(',')
    return string


def find_assignment_lhs(string):
    pos = string.find('=')
    string = string[:pos-1]
    string = string.split()
    return string[-1]


def split_by_comma_space(string):
    return re.split(r"[,]\s+(?=[^()]*(?:\(|$))", string)


def split_by_space(string):
    return re.split(r"\s+(?=[^()]*(?:\(|$))", string)

def is_sub_module(line):
    return

def is_main_module(line):
    return line.startswith('ENTRY')


if __name__ == '__main__':
    flist = list_all_files('./data')
    for f in flist:
        print(f)
