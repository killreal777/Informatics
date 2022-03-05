from StringTools import *


class TagStack:
    def __init__(self):
        self.__tags = ["root"]
        self.__maintain_levels = []
        self.__level = 0

    def push(self, tag):
        self.__tags.append(tag)

    def pop(self):
        return self.__tags.pop(-1)

    def open(self):
        self.__level += 1
        return self.__tags[-1]

    def close(self):
        self.__level -= 1
        return self.__tags[-1]

    def get_level(self):
        return self.__level

    def set_maintain_level(self):
        self.__maintain_levels.append(self.__level)

    def remove_maintain_level(self):
        self.__maintain_levels.pop()

    def is_level_maintains(self):
        if self.__maintain_levels:
            return self.__level == self.__maintain_levels[-1]
        return False

    def test(self):
        print(self.__tags)


class LevelInformation:
    def __init__(self):
        self.__tabs = 0
        self.__open_tag = ""
        self.__close_tag = ""

    def update(self, tabs, open_tag, close_tag):
        self.__tabs = tabs
        self.__open_tag = open_tag
        self.__close_tag = close_tag

    def set_tabs(self, tabs):
        self.__tabs = tabs

    def add_tab(self):
        self.__tabs += 1

    def delete_tab(self):
        self.__tabs -= 1

    def set_open_tag(self, open_tag):
        self.__open_tag = open_tag

    def set_close_tag(self, close_tag):
        self.__close_tag = close_tag

    def values(self):
        return self.__tabs, self.__open_tag, self.__close_tag

    def clean(self):
        self.__tabs = 0
        self.__open_tag = ""
        self.__close_tag = ""


class LineAnalyzer:
    def __init__(self):
        self.__tag_stack = TagStack()
        self.__level_information = LevelInformation()
        self.c = 0

    def analyze_brackets(self, line):
        line = unquoted_area(line)

        if '{' in line:
            self.__level_information.set_open_tag(self.__tag_stack.open())

        elif '}' in line:
            self.__level_information.set_close_tag(self.__tag_stack.close())
            self.__level_information.set_tabs(self.__tag_stack.get_level())
            if not self.__tag_stack.is_level_maintains():
                self.__tag_stack.pop()
            self.__level_information.set_tabs(self.__tag_stack.get_level())

        elif ('[' in line) and (']' in line):
            self.__level_information.set_open_tag(self.__tag_stack.open())
            self.__level_information.set_close_tag(self.__tag_stack.close())
            self.__tag_stack.pop()

        elif '[' in line:
            self.__tag_stack.set_maintain_level()

        elif ']' in line:
            self.__tag_stack.remove_maintain_level()
            self.__tag_stack.pop()

        else:
            self.__level_information.set_open_tag(self.__tag_stack.open())
            self.__level_information.set_close_tag(self.__tag_stack.close())
            self.__tag_stack.pop()

    def __extract_tag(self, line):
        if search_in_unquoted_area(line, ':'):
            tag, line = split_by_first_unquoted_symbol(line, ':')
            self.__tag_stack.push(delete_quotes(tag))
        return line

    def analyze_line(self, line):
        self.__level_information.set_tabs(self.__tag_stack.get_level())    # tabs amount = previous tags amount
        line = delete_unquoted_spaces(line)
        line = self.__extract_tag(line)
        self.analyze_brackets(line)
        data = split_by_unquoted_symbol(delete_unquoted_brackets(line), ',')
        tab, open_tag, close_tag = self.__level_information.values()
        print(self.c, 'tab='+str(tab), 'open_tag='+open_tag, 'close_tag='+close_tag, 'data='+str(data))
        self.c += 1
        self.__level_information.clean()
        return tab, open_tag, close_tag, data
