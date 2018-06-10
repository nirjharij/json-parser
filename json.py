import re
import ast

class Token:
    STRING_BEGIN = STRING_END = '"'
    LIST_BEGIN = '['
    LIST_END = ']'
    LIST_DELIMITER = DICT_DELIMITER = ','
    DICT_SYMBOL = ':'
    DICT_BEGIN = '{'
    DICT_END = '}'
    WHITESPACE = ' '
    NEWLINE = '\n'

class ParserException(Exception):
    pass

def isdigit(s):
    return s in "01234567890"
    
def parse_string(string):
    number = []
    quotes_count = 0
    for s in string:
        if s == Token.STRING_END:
            quotes_count+=1
            if quotes_count == 2:
                break
        else:
            number.append(s)
    return "".join(number),string[(len(number)+quotes_count):]

def parse_number(string):
    number = []
    for s in string:
        if s in "01234567890":
            number.append(s)
        else:
            break
    return int("".join(number)), string[len(number):]

def parse_list(string,temp):
    
    # Approach 1 w/o recursion
    # key = []
    # word_count = 0
    # list_begin_count = 0
    # list_end_count = 0
    # for s in string:
    #     word_count += 1
    #     if s == Token.LIST_BEGIN: 
    #         list_begin_count += 1
    #     elif s == Token.LIST_END:
    #         list_end_count += 1
    #         if list_begin_count == list_end_count:
    #             key.append(s)
    #             break
    #     key.append(s)
    # return ast.literal_eval("".join(key)),string[word_count:]
    
    # Approach 2 with recursion

    if string[0] == Token.LIST_BEGIN:
        temp.append(string[0])
        parse_list(string[1:],temp)
    # import pdb;pdb.set_trace()
    else:
        for i in range(len(string)):
            temp.append(string[i])
            if string[i] == Token.LIST_END and temp.count('[') == temp.count(']'):
                return
    key = ast.literal_eval("".join(temp))
    value = string[len(temp):]
    return tuple((key,value))

def parse_dict(string,temp):
    # Approach 1 using regex
    # dict_data = re.findall(r"{.*}",string)
    # word_count = len(dict_data[0])
    # return ast.literal_eval(dict_data[0]),string[word_count:]

    #Approach 2 Using recursion
    if string[0] == Token.DICT_BEGIN:
        temp.append(string[0])
        parse_dict(string[1:],temp)
    # import pdb;pdb.set_trace()
    else:
        for i in range(len(string)):
            temp.append(string[i])
            if string[i] == Token.DICT_END and temp.count('{') == temp.count('}'):
                return
    key = ast.literal_eval("".join(temp))
    value = string[len(temp):]
    return tuple((key,value))

def parse(string):
    s = string[0]
    temp = []
    if s == Token.STRING_BEGIN:
        return parse_string(string)
    elif s == Token.LIST_BEGIN:
        return parse_list(string,temp)
    elif s == Token.DICT_BEGIN:
        return parse_dict(string,temp)
    elif isdigit(s):
        return parse_number(string)
    else:
        raise ParserException("Unknown Token: %s" % s)

assert parse('123') == (123, '') 
assert parse('123abc') == (123, 'abc')
assert parse('"123"abc') == ('123', 'abc')
assert parse('"abc"[123]') == ('abc', '[123]')
assert parse('[1,2,3]') == ([1,2,3], '')
assert parse('[1,2,3][abc]') == ([1,2,3], '[abc]')
assert parse('[[[]]]') == ([[[]]], '')
assert parse('[[],[[]]]') == ([[],[[]]], '')
assert parse('["a",123,["x","y"]]') == (["a", 123, ["x", "y"]], '')
assert parse('{"a":1}') == ({"a": 1}, '')
assert parse('{"a":1,"b":2}') == ({"a":1,"b":2},'')
assert parse('{}') == ({}, '')
assert parse('{}abc') == ({}, 'abc')
assert parse('{"a":[[[]]]}') == ({"a":[[[]]]}, '')
assert parse('{"a":1,"b":[1,2,3],"c":{"d":1}}') == ({"a":1,"b":[1,2,3],"c":{"d":1}}, '')