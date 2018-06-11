# json-parser

A json parser that can parse arbitrary json string with the following limitations:

    - json primitives can be types: number, string
    - json data structures - list and dict which can be arbitrary nested
    - It does not support whitespaces between tokens.
    - It does not support escape codes in strings.
    
Examples of the correct parse for some json strings:

'123' - 123 (number)

'"123"' - "123" (string)

'[1,2,"a"]' - [1,2,"a"] (python list)

How does the parser work?

The driver function and the starting point of this parser is the parse function. Parse function looks at the first character of its 
input and simply calls the corresponding functions. The semantics of the parse function and other parse_<type> functions are as
follows:

- input is string
- output is a two element array where:
    - first element is the data structure for the parsed input string
    - second element is a string which is the part of the input string which has not been parsed

To give you a few example:
parse('123abc') = (123, "abc")
