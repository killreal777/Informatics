def search_in_unquoted_area(line, symbol):
    double_quote_opened = False
    single_quote_opened = False
    match_indexes = []
    for i in range(len(line)):
        if line[i] == '"':
            double_quote_opened = not double_quote_opened
        if line[i] == "'":
            single_quote_opened = not single_quote_opened
        if line[i] == symbol and not double_quote_opened and not single_quote_opened:
            match_indexes.append(i)
    return match_indexes


def unquoted_area(line):
    double_quote_opened = False
    single_quote_opened = False
    output_string = ""
    for i in range(len(line)):
        if line[i] == '"':
            double_quote_opened = not double_quote_opened
        elif line[i] == "'":
            single_quote_opened = not single_quote_opened
        elif not double_quote_opened and not single_quote_opened:
            output_string += line[i]
    return output_string


def split_by_first_unquoted_symbol(line, symbol):
    index = search_in_unquoted_area(line, symbol)[0]
    return line[:index], line[index+1:]


def split_by_unquoted_symbol(line, symbol):
    separated_line = []
    if search_in_unquoted_area(line, symbol):
        while search_in_unquoted_area(line, symbol):
            part, line = split_by_first_unquoted_symbol(line, symbol)
            separated_line.append(part)
    else:
        separated_line = [line]
    return separated_line


def delete_symbol(string, index):
    if index < len(string) - 1:
        return string[0: index] + string[index + 1: len(string)]
    else:
        return string[:-1]


def delete_unquoted_spaces(line):
    for i in search_in_unquoted_area(line, " ")[::-1]:
        line = delete_symbol(line, i)
    return line


def delete_unquoted_brackets(line):
    for bracket in ['[', ']', '{', '}']:
        for i in search_in_unquoted_area(line, bracket)[::-1]:
            line = delete_symbol(line, i)
    return line


def delete_quotes(line):
    if line:
        if line[0] in ['"', "'"]:
            line = line[1:]
        if line[-1] in ['"', "'"]:
            line = line[:-1]
        return line
