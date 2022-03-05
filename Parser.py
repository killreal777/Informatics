from ParserTools import LineAnalyzer
from FileTools import write_line_xml
from StringTools import delete_quotes

json_file = open("test.json", encoding="utf-8").read()
json_lines = json_file.splitlines()

xml_file = open("lab4_output.xml", 'w', encoding="utf-8")

analyzer = LineAnalyzer()


for line in json_lines:
    tabs, open_tag, close_tag, data = analyzer.analyze_line(line)
    if data:
        for i in data:
            write_line_xml(xml_file, tabs, open_tag, close_tag, delete_quotes(i))
    else:
        write_line_xml(xml_file, tabs, open_tag, close_tag, "")
