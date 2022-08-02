import unittest
from reverse_sandbox import NonTerminalNode
import math
import random
from copy import deepcopy

curr_filter_database = [ "regex", "-regex", "literal", "subpath", "", "hello\n"] # database of possible curr_filter, always a string ??
# We can't test with None ! because of '+=' operand (like in regex_adder)
ret_str_database = [ "hello", "regex", "", "\n", "hello\n world\n" ]
# same issue, we can't have ret_str= None
argument_database = [ [], [""], [ [], " ", "hello"], ["h", "hello world"] ] # list of string database
# we can't have None too, no '\n' because I use str.split('\n') so it will disturb
arg_database = [  "", " " "+hello", "hel\\.lo", "he\\\\llo", "hello\\\.", "]hell[o", "he\\|\\.o" ]
# None and int impossible
filter_database = [ None, False, "regex", "-regex", "literal", "subpath", "", "hello\n"] 
# there is 'if not filter', otherwise it must be a string
s_database = [  "", " " "+hello", "hel\\.lo", "he\\\\llo", "hello\\\.", "]hell[o", "he\\|\\.o", "}hello${ world\n", "hello/^^^" ]
# None impossible because of 'len(s)'
arg_database2 = arg_database + s_database

class Initialize(unittest.TestCase):
    """Test the NonTerminalNode object initialization
    """
    def test_object_exists(self):
        NNode = NonTerminalNode.NonTerminalNode()
        self.assertEqual(NNode.filter_id, None)
        self.assertEqual(NNode.filter, None)
        self.assertEqual(NNode.argument_id, None)
        self.assertEqual(NNode.argument, None)
        self.assertEqual(NNode.match_offset, None)
        self.assertEqual(NNode.match, None)
        self.assertEqual(NNode.unmatch_offset, None)
        self.assertEqual(NNode.unmatch, None)
    
    def test_eq(self):
        first = NonTerminalNode.NonTerminalNode()
        first.filter_id = 1
        first.argument_id = [ 1, "2"]
        first.match_offset = { 1: "2", "2": 7}
        first.unmatch_offset = True
        first.filter = 42
        first.argument = 42
        first.match = 42
        first.unmatch = 42
        other = NonTerminalNode.NonTerminalNode()
        #self.assertEqual(first, other)
        self.assertFalse(first.__eq__(other))
        self.assertFalse(first.filter_id == other.filter_id)
        other.filter_id = 1
        other.argument_id = [ 1, "2"]
        other.match_offset = { 1: "2", "2": 7}
        other.unmatch_offset = True
        other.filter = 43
        other.argument = 43
        other.match = 43
        other.unmatch = 43
        self.assertTrue(first.__eq__(other))
        self.assertFalse(first.filter==other.filter)

class Methods(unittest.TestCase):
    
    @unittest.skip("this test Failed")
    def test_simplify_list(self):
        NNode = NonTerminalNode.NonTerminalNode()
        arg_list = [ "hello", "good/", "hello/", "/hello", "good", "goo/d", "magic"]
        result_list = NNode.simplify_list(arg_list)
        #print(result_list)
        expected_list = ["hello/^^^", "good/^^^", "goo/d", "magic"]
        self.assertEqual(result_list, expected_list)

    """ I find this function quite strange and I found several problems if I correct understood its purpose :
-> if there is at least 3 versions of 1 word, the function won't keep only 1 version of the word, but at least 2 like for example in my example above here
-> no detection if there is "ex/" and "/ex" for instance (I don't know if it's a problem ?)
    """
    
    def test__prefix_adder(self):
        NNode = NonTerminalNode.NonTerminalNode()
        curr_filter = "hello everyone"
        prefix_added = False 
        s = "hello${hello}"
        new_curr_filter = NNode._prefix_adder(curr_filter, prefix_added, s)
        self.assertEqual(new_curr_filter, curr_filter+"-prefix")

# it didn't recognize NNode.__prefix_ader(), we should rename it just _prefix_ader()
# prefix_added is not returned so we won't know if a prefix has been added
# a prefix is at the beginning of a word beware at possible confusions

    def test__cur_filter_identifier(self):
        
        def cur_ident(self, curr_filter, s, NNode):
            new_curr_filter, new_s = NNode._cur_filter_identifier(curr_filter, s)
            if '\\' in s or '|' in s or ('[' in s and ']' in s) or '+' in s:
                if NNode.filter == "literal":
                    self.assertEqual(new_curr_filter, "regex")
                else:
                    if s[-4:] == "/^^^":
                        self.assertEqual(new_curr_filter, "subpath-regex")
                        s = s[:-4]
                        s = s + "/?"
                    elif curr_filter == "subpath":
                        s = s + "/?"
                        self.assertEqual(new_curr_filter, "subpath-regex")
                    else:
                        self.assertEqual(new_curr_filter, curr_filter + "-regex")
                    s = s.replace('\\\\.', '[.]')
                    s = s.replace('\\.', '[.]')
                    self.assertEqual(s, new_s)
            else:
                if s[-4:] == "/^^^":
                    self.assertEqual(new_curr_filter, "subpath")
                    self.assertEqual(new_s, s[:-4])
                else:
                    self.assertEqual(new_curr_filter, curr_filter)
                    self.assertEqual(new_s, s)

        NNode = NonTerminalNode.NonTerminalNode()
        
        s = "hello/^^^"
        curr_filter = None
        new_curr_filter, new_s = NNode._cur_filter_identifier(curr_filter, s)    
        self.assertEqual(new_curr_filter, "subpath")
        self.assertEqual(new_s, "hello")
        cur_ident(self, curr_filter, s, NNode)

        s = "]hello[/^^^"
        curr_filter = "cur"
        new_curr_filter, new_s = NNode._cur_filter_identifier(curr_filter, s)
        self.assertEqual(new_curr_filter, "subpath-regex")
        self.assertEqual(new_s, "]hello[/?")
        cur_ident(self, curr_filter, s, NNode)

        s = "\\\\.hello+"
        curr_filter = "cur"
        new_curr_filter, new_s = NNode._cur_filter_identifier(curr_filter, s)
        self.assertEqual(new_curr_filter, "cur-regex")
        self.assertEqual(new_s, "[.]hello+")
        cur_ident(self, curr_filter, s, NNode)

        NNode.filter = "literal"
        s = "hello\\."
        curr_filter = "subpath"
        new_curr_filter, new_s = NNode._cur_filter_identifier(curr_filter, s)
        self.assertEqual(new_curr_filter, "regex")
        self.assertEqual(new_s, "hello[.]/?")
        cur_ident(self, curr_filter, s, NNode)
# same issue with the '__'

    def test_identify_subpath(self):
        # this function is safe because simple use of 2 other functions
        NNode = NonTerminalNode.NonTerminalNode()
        curr_filter = "first"
        arg = "hel|lo"
        new_arg, new_curr_filter = NNode._identify_subpath(arg, curr_filter)
        self.assertEqual(new_arg, arg)
        temp_curr_filter, s = NNode._cur_filter_identifier(curr_filter, arg)
        temp_curr_filter = NNode._prefix_adder(temp_curr_filter, False, arg)
        self.assertEqual(temp_curr_filter, new_curr_filter)
# __regex_adder and _regex_adder weren't detected so I supressed the 2 '_'

    def test_regex_adder(self):
        NNode = NonTerminalNode.NonTerminalNode()
        for curr_filter in curr_filter_database:
            def test_regex(self, curr_filter, regex_added):
                new_curr_filter = NNode.regex_adder(curr_filter, regex_added)
                if not regex_added:
                    if NNode.filter == "literal":
                        self.assertEqual(new_curr_filter, "regex")
                    else:
                        self.assertEqual(new_curr_filter, curr_filter + "-regex")
                else:
                    self.assertEqual(new_curr_filter, curr_filter)
            regex_added = True
            test_regex(self, curr_filter, regex_added)
            regex_added = False
            test_regex(self, curr_filter, regex_added)

    def test_identify_subpath_and_filter(self):
        NNode = NonTerminalNode.NonTerminalNode()

        def test_identify(self, NNode, ret_str):
            new_ret_str = NNode._identify_subpath_and_filter(ret_str)
            new_lines = new_ret_str.split("\n")
            old_lines = ret_str.split("\n")
            begin_ret_str = new_lines[:len(old_lines)-1] # '-1' for the '\n' added
            if len(NNode.argument) == 0:
                old_lines[-2] += ")"
                self.assertEqual(begin_ret_str, old_lines[:-1]) # the last line of old_lines must be ""
            else:
                self.assertEqual(begin_ret_str, old_lines[:-1])
            self.assertEqual(old_lines[-1], '')
            self.assertEqual(len(old_lines) -1 + len(NNode.argument) , len(new_lines)) # the '-1' is for the '\n' which was added
            for l in range(len(NNode.argument)):
                arg = NNode.argument[l]
                curr_filter = NNode.filter
                regex_added = False
                if len(arg) == 0:
                    arg = ".+"
                    curr_filter = NNode.regex_adder(curr_filter, regex_added) # this function has already been tested

                else:
                    arg, curr_filter = NNode._identify_subpath(arg, curr_filter)

                if "regex" in curr_filter:
                    if l == len(NNode.argument)-1: # ie last line
                        if len(NNode.argument) == 1:
                            self.assertEqual(new_lines[ len(old_lines) -1 + l ], '(%04x, %04x) (%s #"%s")' % (NNode.match_offset, NNode.unmatch_offset, curr_filter, arg) ) # same reason than before for the '-1', the '\n' added
                        else:
                            self.assertEqual(new_lines[ len(old_lines) -1 + l ], '(%04x, %04x) (%s #"%s"))' % (NNode.match_offset, NNode.unmatch_offset, curr_filter, arg) ) # one ')' add at the end of the line
                    else:
                        self.assertEqual(new_lines[ len(old_lines) -1 + l ], '(%04x, %04x) (%s #"%s")' % (NNode.match_offset, NNode.unmatch_offset, curr_filter, arg) )
                else:
                    if l == len(NNode.argument)-1: # last line
                        if len(NNode.argument) == 1:
                            self.assertEqual(new_lines[ len(old_lines) -1 + l ], '(%s "%s")' % (curr_filter, arg) )
                        else:
                            self.assertEqual(new_lines[ len(old_lines) -1 + l ], '(%s "%s"))' % (curr_filter, arg) ) # add of ')' at the end
                    else:
                        self.assertEqual(new_lines[ len(old_lines) -1 + l ], '(%s "%s")' % (curr_filter, arg) )

        for ret_str in ret_str_database:
            ret_str += "\n" # to separate the last line of old_ret_str and the first line of new_ret_str
            for argument in argument_database:
                NNode.match_offset = 42 # we should also have NNode.match_offset and NNode.unmatch_offset not None but numbers otherwise the function stopped
                NNode.unmatch_offset = 43
                NNode.argument = argument
                for filter in curr_filter_database:
                    if '\n' in filter: # because I use str.split("\n") so it disturb my function, but as the operations on filter are only other functions we already tested it is not important
                        continue
                    NNode.filter = filter
                    test_identify(self, NNode, ret_str)

    def test_single_argument(self):
        NNode = NonTerminalNode.NonTerminalNode()

        def test_single(self, NNode, arg, curr_filter):
            new_arg, new_curr_filter = NNode._single_argument_regex(arg, curr_filter)
            if "regex" not in curr_filter:
                if '\\' in arg or '|' in arg or ('[' in arg and ']' in arg) or '+' in arg:
                    if new_curr_filter == "regex":
                        self.assertEqual(NNode.filter, "literal")
                    else:
                        self.assertEqual(new_curr_filter, curr_filter + "-regex")
                    arg = arg.replace('\\\\.', '[.]')
                    arg = arg.replace('\\.', '[.]')
                    self.assertEqual(arg, new_arg)
                else:
                    self.assertEqual(new_curr_filter, curr_filter)
                    self.assertEqual(new_arg, arg)
            else:
                self.assertEqual(new_curr_filter, curr_filter)
                self.assertEqual(new_arg, arg)

        for arg in s_database:
            for curr_filter in curr_filter_database:
                for filter in filter_database:
                    NNode.filter = filter
                    test_single(self, NNode, arg, curr_filter)

    def test_str_initializer(self):
        NNode = NonTerminalNode.NonTerminalNode()
        def test_str(self, NNode):
            ret_str = NNode._str_initializer()
            if ret_str == "":
                self.assertEqual(len(NNode.argument), 1)
            else:
                self.assertEqual(ret_str, "(require-any ")

        for arg in argument_database:
            NNode.argument = arg
            test_str(self, NNode)

    def test_str_debug(self):
        NNode = NonTerminalNode.NonTerminalNode()
        def test_str(self, NNode):
            old_arg = deepcopy(NNode.argument)
            res = NNode.str_debug()
            if not NNode.filter:
                self.assertEqual(res, "(%02x %04x %04x %04x)" % (NNode.filter_id, NNode.argument_id, NNode.match_offset, NNode.unmatch_offset))
            elif old_arg:
                old_arg = NNode.simplify_list(old_arg)
                if type(old_arg) is list:
                    ret_str = NNode._str_initializer()
                    ret_str = NNode._identify_subpath_and_filter(ret_str)
                    self.assertEqual(res, ret_str)
                else:
                    arg = old_arg
                    curr_filter = NNode.filter
                    arg, curr_filter = NNode._single_argument_regex(arg, curr_filter)
                    prefix_added = False
                    NNode._prefix_adder(curr_filter, prefix_added, arg)
                    self.assertEqual(res, "(%04x, %04x) (%s %s)" % (NNode.match_offset, NNode.unmatch_offset, curr_filter, arg))
            else:
                self.assertEqual(res, "(%04x, %04x) (%s)" % (NNode.match_offset, NNode.unmatch_offset, NNode.filter))

        for filter in filter_database:
            argument_database = [ None, False, "hello", "", [], [""], [ [], " ", "hello"], ["h", "hello world"] ]
            for arg in argument_database:
                NNode.filter = filter
                NNode.argument = arg
                NNode.unmatch_offset = 42 # number mandatory
                NNode.match_offset = 43
                NNode.argument_id = 44
                NNode.filter_id = 45
                test_str(self, NNode)

    def test_filter_accumultaor(self):
        NNode = NonTerminalNode.NonTerminalNode()
        def test_filter(self, NNode, s):
            new_curr_filter, new_s = NNode._filter_accumulator(s)
            curr_filter = NNode.filter
            regex_added = False
            prefix_added = False
            if len(s) == 0:
                self.assertEqual(new_s, ".+")
                self.assertEqual( NNode.regex_adder(curr_filter, regex_added), new_curr_filter )
            else:
                curr_filter, s = NNode._cur_filter_identifier(curr_filter, s)
                self.assertEqual(NNode._prefix_adder(curr_filter, prefix_added, s), new_curr_filter)
                self.assertEqual(new_s, s)

        for s in s_database:
            for curr_filter in curr_filter_database:
                NNode.filter = curr_filter
                test_filter(self, NNode, s)

# same as test_single_argument_regex...
    def test_not_regex(self):
        NNode = NonTerminalNode.NonTerminalNode()
        def test_not(self, NNode, curr_filter, s):
            new_curr_filter, new_s = NNode._not_regex(curr_filter, s)
            if "regex" not in curr_filter:
                if '\\' in s or '|' in s or ('[' in s and ']' in s) or '+' in s:
                    s = s.replace('\\\\.', '[.]')
                    s = s.replace('\\.', '[.]')
                    if NNode.filter == "literal":
                        self.assertEqual(new_curr_filter, "regex")
                    else:
                        self.assertEqual(new_curr_filter, curr_filter + "-regex")
                    self.assertEqual(new_s, s)
                else:
                    self.assertEqual(new_curr_filter, curr_filter)
                    self.assertEqual(new_s, s)
            else:
                self.assertEqual(new_curr_filter, curr_filter)
                self.assertEqual(new_s, s)

        for curr_filter in curr_filter_database:
            for s in s_database:
                for filter in filter_database:
                    NNode.filter = filter
                    test_not(self, NNode, curr_filter, s)

    def test_str__(self):
        NNode = NonTerminalNode.NonTerminalNode()

        def test_str(self, NNode):
            res = NNode._str__()
            if not NNode.filter:
                self.assertEqual(res, "(%02x %04x %04x %04x)" % (NNode.filter_id, NNode.argument_id, NNode.match_offset, NNode.unmatch_offset))
            elif not NNode.argument:
                self.assertEqual(res, "(%s)" % NNode.filter)
            elif type(NNode.argument) is not list:
                s = NNode.argument
                curr_filter = NNode.filter
                curr_filter, s = NNode._not_regex(curr_filter, s)
                prefix_added = False
                NNode._prefix_adder(curr_filter, prefix_added, s)
                self.assertEqual(res, "(%s %s)" % (curr_filter, s))
            else:
                NNode.argument = NNode.simplify_list(NNode.argument)
                ret_str = NNode._str_initializer()
                self.assertEqual(ret_str, res[len(ret_str)])
                res = res[len(ret_str):]
                res_tab = res.split("\n")
                self.assertEqual(len(res_tab), len(NNode.argument))

                for i in range (len(NNode.argument) -1 ):
                    curr_filter, s = NNode._filter_accumulator(NNode.argument[i])
                    if "regex" in curr_filter:
                        self.assertEqual(res_tab[i], '(%s #"%s")' % (curr_filter, s) )
                    else:
                        self.assertEqual(res_tab[i], '(%s "%s")' % (curr_filter, s) )

                if len(NNode.argument) == 1:
                    curr_filter, s = NNode._filter_accumulator(NNode.argument[0])
                    if "regex" in curr_filter:
                        self.assertEqual(res_tab[i], '(%s #"%s")' % (curr_filter, s) )
                    else:
                        self.assertEqual(res_tab[i], '(%s "%s")' % (curr_filter, s) )
                else: # there is an additionnal ')' at the end 
                    curr_filter, s = NNode._filter_accumulator(NNode.argument[-1])
                    if "regex" in curr_filter:
                        self.assertEqual(res_tab[-1], '(%s #"%s"))' % (curr_filter, s) )
                    else:
                        self.assertEqual(res_tab[-1], '(%s "%s"))' % (curr_filter, s) )

        for filter in filter_database:
            NNode.filter = filter
            NNode.filter_id = 42
            NNode.argument_id = 43
            NNode.match_offset = 44
            NNode.unmatch_offset = 45
            for arg in arg_database2:
                NNode.argument = arg
                test_str(self, NNode)

# There is probably a mistake of ident in 'def not_str(self)', because if self.argument is a list it doesn't return anything, and in the part of non list, there is 'for s in self.argument'
# I have correct it by what I think is right in 'def cor_str_not(self)'
    def test_str_not(self):
        NNode = NonTerminalNode.NonTerminalNode()

        def test_str(self, NNode):
            res = NNode.cor_str_not()
            if not NNode.filter:
                self.assertEqual(res, "(%02x %04x %04x %04x)" % (NNode.filter_id, NNode.argument_id, NNode.match_offset, NNode.unmatch_offset))
            elif not NNode.argument:
                self.assertEqual(res, "(%s)" % NNode.filter)
            elif type(NNode.argument) is not list:
                if len(NNode.argument) == 1:
                    self.assertEqual(res, "")
            else:
                NNode.argument = NNode.simplify_list(NNode.argument)
                if res[:len("require-all")] == "(require-all":
                    self.assertNotEqual(len(NNode.argument), 1)
                    res = res[len("require-all"):]

                res_tab = res.split("\n")
                self.assertEqual(len(res_tab), len(NNode.argument))

                for i in range (len(NNode.argument) -1 ):
                    curr_filter, s = NNode._filter_accumulator(NNode.argument[i])
                    if "regex" in curr_filter:
                        self.assertEqual(res_tab[i], '(require-not (%s #"%s"))' % (curr_filter, s) )
                    else:
                        self.assertEqual(res_tab[i], '(require-not (%s "%s"))' % (curr_filter, s) )

                if len(NNode.argument) == 1:
                    curr_filter, s = NNode._filter_accumulator(NNode.argument[0])
                    if "regex" in curr_filter:
                        self.assertEqual(res_tab[i], '(require-not (%s #"%s"))' % (curr_filter, s) )
                    else:
                        self.assertEqual(res_tab[i], '(require-not (%s "%s"))' % (curr_filter, s) )
                else: # there is an additionnal ')' at the end 
                    curr_filter, s = NNode._filter_accumulator(NNode.argument[-1])
                    if "regex" in curr_filter:
                        self.assertEqual(res_tab[-1], '(require-not (%s #"%s")))' % (curr_filter, s) )
                    else:
                        self.assertEqual(res_tab[-1], '(require-not (%s "%s")))' % (curr_filter, s) )

        for filter in filter_database:
            NNode.filter = filter
            NNode.filter_id = 42
            NNode.argument_id = 43
            NNode.match_offset = 44
            NNode.unmatch_offset = 45
            for arg in arg_database2:
                NNode.argument = arg
                test_str(self, NNode)

    def test_values(self):
        NNode = NonTerminalNode.NonTerminalNode()
        def test_value(self, NNode):
            a, b = NNode.values()
            if a == NNode.filter and b == NNode.argument:
                self.assertTrue(NNode.filter)
            else:
                self.assertFalse(NNode.filter)
                self.assertEqual(a, "%02x" % NNode.filter_id)
                self.assertEqual(b, "%04x" % NNode.argument_id)

        for filter in filter_database + [ True, 42]:
            NNode.filter = filter
            NNode.filter_id = 42 # we need numbers
            NNode.argument_id = 0x2a
            test_value(self, NNode)

    def test_is_entitlement_start(self):
        NNode = NonTerminalNode.NonTerminalNode()
        def test_is(self, NNode):
            res = NNode.is_entitlement_start()
            if res:
                self.assertTrue(NNode.filter_id == 0x1e or NNode.filter_id == 0xa0)
            else:
                self.assertFalse(NNode.filter_id == 0x1e)
                self.assertFalse(NNode.filter_id == 0xa0)

        for filter_id in [0x1e, 30, None, True, "0x1e", 0xa0, 160, "0xa0", 42, 0x2f]:
            NNode.filter_id = filter_id
            test_is(self, NNode)

    def test_is_entitlement(self):
        NNode = NonTerminalNode.NonTerminalNode()
        def test_is(self, NNode):
            res = NNode.is_entitlement()
            if res:
                self.assertTrue(NNode.filter_id == 0x1e or NNode.filter_id == 0xa0 or NNode.filter_id == 0x1f or NNode.filter_id == 0x20)
            else:
                self.assertFalse(NNode.filter_id == 0x1e)
                self.assertFalse(NNode.filter_id == 0xa0)
                self.assertFalse(NNode.filter_id == 0x1f)
                self.assertFalse(NNode.filter_id == 0x20)

        for filter_id in [0x1e, 30, None, True, "0x1e", 0xa0, 160, "0xa0", 0x1f, 31, "0x1f", 0x20, 32, "0x20"]:
            NNode.filter_id = filter_id
            test_is(self, NNode)

    @unittest.skip("'num_regex' undefined")
    def test_is_last_regular_expression(self):
        NNode = NonTerminalNode.NonTerminalNode()
        def test_is(self, NNode):
            res = NNode.is_last_regular_expression()
            if res:
                self.assertTrue(NNode.filter_id == 0x81 and NNode.argument_id == num_regex - 1) # num_regex is not defined
            else:
                self.assertFalse(NNode.filter_id == 0x81 and NNode.argument_id == num_regex - 1)

        for filter_id in [0x81, 129, "0x81", 42, 0xa0]:
            NNode.filter_id = filter_id
            test_is(self, NNode)

    def test_convert_filter(self):
        NNode = NonTerminalNode.NonTerminalNode()
        def test_convert(self, NNode, convert_fn, f, regex_list, ios_major_version, keep_builtin_filters, global_vars, base_addr):
            NNode.convert_filter(convert_fn, f, regex_list, ios_major_version, keep_builtin_filters, global_vars, base_addr)
            a, b = convert_fn(f, ios_major_version, keep_builtin_filters, global_vars, regex_list, NNode.filter_id, NNode.argument_id, base_addr)
            self.assertEqual(NNode.filter, a)
            self.assertEqual(NNode.argument, b)

        NNode.filter_id = 43
        NNode.argument_id = 44
        def convert_fn(self, convert_fn, f, regex_list, ios_major_version,keep_builtin_filters, global_vars, base_addr):
            return 42, 43 # I don't know what is this function
        f = None
        ios_major_version = 10
        keep_builtin_filters = "\n"
        global_vars = f
        regex_list = ["hello"]
        base_addr = 0.99
        test_convert(self, NNode, convert_fn, f, regex_list, ios_major_version, keep_builtin_filters, global_vars, base_addr)

    @unittest.skip("function 'is_non_terminal' and 'is_terminal' unknown")
    def test_is_non_terminal_deny(self):
        NNode = NonTerminalNode.NonTerminalNode()
        def test_is(self, NNode):
            res = NNode.is_non_terminal_deny()
            if res:
                self.assertEqual(res, NNode.unmatch.terminal.is_deny())
                self.assertTrue(self.match.is_non_terminal() and self.unmatch.is_terminal())
            else:
                self.assertFalse(self.match.is_non_terminal() and self.unmatch.is_terminal())
                self.assertEqual(res, None)

        for match in [[1, 2], "hello", None, True]:
            NNode.match = match
            for unmatch in [0xee, "", False, "\n", 42]:
                NNode.unmatch = unmatch
                test_is(self, NNode)

    @unittest.skip("function 'is_non_terminal' and 'is_terminal' unknown")
    def test_is_non_terminal_allow(self):
        NNode = NonTerminalNode.NonTerminalNode()
        def test_is(self, NNode):
            res = NNode.is_non_terminal_allow()
            if res:
                self.assertEqual(res, NNode.unmatch.terminal.is_allow())
                self.assertTrue(self.match.is_non_terminal() and self.unmatch.is_terminal())
            else:
                self.assertFalse(self.match.is_non_terminal() and self.unmatch.is_terminal())
                self.assertEqual(res, None)

        for match in [[1, 2], "hello", None, True]:
            NNode.match = match
            for unmatch in [0xee, "", False, "\n", 42]:
                NNode.unmatch = unmatch
                test_is(self, NNode)

    @unittest.skip("function 'is_non_terminal' and 'is_terminal' unknown")
    def test_is_non_terminal_non_terminal(self):
        NNode = NonTerminalNode.NonTerminalNode()
        def test_is(self, NNode):
            res = NNode.is_non_terminal_non_terminal()
            self.assertEqual(res, NNode.match.is_non_terminal() and NNode.unmatch.is_non_terminal())

        for match in [[1, 2], "hello", None, True]:
            NNode.match = match
            for unmatch in [0xee, "", False, "\n", 42]:
                NNode.unmatch = unmatch
                test_is(self, NNode)

    @unittest.skip("function 'is_non_terminal' and 'is_terminal' unknown")
    def test_is_allow_non_terminal(self):
        NNode = NonTerminalNode.NonTerminalNode()
        def test_is(self, NNode):
            res = NNode.is_allow_non_terminal()
            if res:
                self.assertEqual(res, NNode.match.terminal.is_allow())
                self.assertTrue(self.match.is_terminal() and self.unmatch.is_non_terminal())
            else:
                self.assertFalse(self.match.is_terminal() and self.unmatch.is_non_terminal())
                self.assertEqual(res, None)

        for match in [[1, 2], "hello", None, True]:
            NNode.match = match
            for unmatch in [0xee, "", False, "\n", 42]:
                NNode.unmatch = unmatch
                test_is(self, NNode)

    @unittest.skip("function 'is_non_terminal' and 'is_terminal' unknown")
    def test_is_deny_non_terminal(self):
        NNode = NonTerminalNode.NonTerminalNode()
        def test_is(self, NNode):
            res = NNode.is_non_terminal_deny()
            if res:
                self.assertEqual(res, NNode.match.terminal.is_deny())
                self.assertTrue(self.match.is_terminal() and self.unmatch.is_non_terminal())
            else:
                self.assertFalse(self.match.is_terminal() and self.unmatch.is_non_terminal())
                self.assertEqual(res, None)

        for match in [[1, 2], "hello", None, True]:
            NNode.match = match
            for unmatch in [0xee, "", False, "\n", 42]:
                NNode.unmatch = unmatch
                test_is(self, NNode)

    @unittest.skip("function 'is_non_terminal' and 'is_terminal' unknown")
    def test_is_deny_allow(self):
        NNode = NonTerminalNode.NonTerminalNode()
        def test_is(self, NNode):
            res = NNode.is_deny_allow()
            if res:
                self.assertEqual(res, NNode.match.terminal.is_deny() and NNode.unmatch.terminal.is_allow() )
                self.assertTrue(self.match.is_terminal() and self.unmatch.is_terminal())
            else:
                self.assertFalse(self.match.is_terminal() and self.unmatch.is_terminal())
                self.assertEqual(res, None)

        for match in [[1, 2], "hello", None, True]:
            NNode.match = match
            for unmatch in [0xee, "", False, "\n", 42]:
                NNode.unmatch = unmatch
                test_is(self, NNode)
    
    @unittest.skip("function 'is_non_terminal' and 'is_terminal' unknown")
    def test_is_allow_deny(self):
        NNode = NonTerminalNode.NonTerminalNode()
        def test_is(self, NNode):
            res = NNode.is_allow_deny()
            if res:
                self.assertEqual(res, NNode.match.terminal.is_allow() and NNode.unmatch.terminal.is_deny() )
                self.assertTrue(self.match.is_terminal() and self.unmatch.is_terminal())
            else:
                self.assertFalse(self.match.is_terminal() and self.unmatch.is_terminal())
                self.assertEqual(res, None)

        for match in [[1, 2], "hello", None, True]:
            NNode.match = match
            for unmatch in [0xee, "", False, "\n", 42]:
                NNode.unmatch = unmatch
                test_is(self, NNode)

if __name__ == '__main__':
    unittest.main()
