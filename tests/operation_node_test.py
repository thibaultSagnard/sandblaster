import unittest
from reverse_sandbox import operation_node
from copy import deepcopy
import struct
import random
import os

type_database = ["0x00", 0x00, 0, 42, 1, None, True, False]
TERMINAL_NODE_TYPE_ALLOW_database = [ True, False, None, 42, "hello", 0x42]
TERMINAL_NODE_TYPE_DENY_database = [ True, False, None, 42, "hello", 0x42]
filter_database = [ None, False, True, "regex", "-regex", "literal", "subpath", "", "hello\n", "-prefix", "hello_regex_world"]
filter_database2 = [ None, "regex", "-regex", "literal", "subpath", "", "hello\n", "-prefix", "hello_regex_world"]
# bool is not iterable
argument_database = [  "", " " "+hello", "hel\\.lo", "he\\\\llo", "hello\\\.", "]hell[o", "he\\|\\.o", "}hello${ world\n", "hello/^^^" ]
id_database = [ 0x1e, 30, 29, 31, "0x1e", None, True, False, 0xa0, 160, "0xa0", 0x1f, 31, "0x1f", 0x20, 32, "0x20", 0x81, 0, -1, -2, 1, 2, 42]
id_database2 = [ 0x1e, 30, 29, 31, 0xa0, 160]
operation_database = [ 0, 1, 42, "0x00", None, True, False]

Node2 = operation_node.OperationNode(42) # as is_terminal_node() exists for objects of class operationNode, match must be of this class
# for self.unmatch.terminal.is_deny() to exist, as is_deny() only exists for class TerminalNode...
Node0 = operation_node.TerminalNode()
Node2.terminal = Node0
Node2.raw = [21, 22, 23, 24]
Node3 = operation_node.OperationNode(42)
Node3.type = 1 # so is_terminal is true
Node3.terminal = Node0
Node3.raw = [30, 31, 32, 33, 34]
Node4 = operation_node.OperationNode(42) # same for unmatch
Node4.raw = [40, 41, 42, 43]
Node5 = operation_node.OperationNode(42)
Node5.type = 0
Node5.non_terminal = Node2
Node5.terminal = Node0
Node5.raw = [50, 51, 52, 53]
Node6 = operation_node.OperationNode(42)
Node6.type = 0
Node6.non_terminal = Node2
Node6_1 = operation_node.TerminalNode()
Node6_1.type = 1
Node6.terminal = Node6_1
num_regex = operation_node.num_regex
NNode = operation_node.NonTerminalNode()
NNode.parent = 42

node_database = [ Node0, Node2, Node3, Node4, Node5, Node6, NNode]
g_database = [{Node2: {"list": {Node3, Node4}, "decision": "admission", "type": set(["normal", "final"]), "reduce": None, "not": False}, Node3: {"list": set(), "decision": "None", "type": set(["normal"]), "reduce": None, "not": True}, Node4: {"list": {Node3}, "decision": "no admission", "type": set(["normal", "final"]), "reduce": None, "not": True} } ]
g_database2 = [ {Node2: {"list": {Node3, Node4}, "type": {"start", "final"}}, Node3: {"list": {Node2, Node4}, "type": {}}, Node4: {"list": {Node5}, "type": {"start"}}, Node5: {"list": {Node3, Node2}, "type": {"normal", "final"}} } ] + g_database
g_database3 = [ { Node2: {"list": {Node3, Node4}, "decision": None, "type": set(["normal"]), "reduce": None, "not": False }, Node2: {"list": {Node3}, "decision": "admission", "type": set(["normal"]), "reduce": None, "not": True }} ] + g_database2

Node10 = operation_node.OperationNode(42) # for is_non_terminal_allow
Node10.raw = [100, 101, 102, 103]
Node00 = operation_node.NonTerminalNode()
Node10.non_terminal = Node00
Node11 = operation_node.OperationNode(42) # for is_allow_deny
Node00.match = Node11
Node11.type = 0
Node11.raw = [104, 105, 106, 107, 108]
Node03 = operation_node.NonTerminalNode() # nothing
Node21 = operation_node.OperationNode(42) # nothing
Node21.raw = [200, 201, 202, 203]
Node22 = operation_node.OperationNode(42) # nothing
Node22.raw = [ 204, 205, 206, 207]
Node11.non_terminal = Node03
Node03.match = Node21
Node21.type = 1
Node03.unmatch = Node22
Node22.type = 1
Node04 = operation_node.TerminalNode()
Node21.terminal = Node04
Node04.type = 0
Node05 = operation_node.TerminalNode()
Node22.terminal = Node05
Node05.type = 1
Node12 = operation_node.OperationNode(42)
Node12.raw = [109, 110, 111, 112]
Node00.unmatch = Node12
Node12.type = 1
Node01 = operation_node.TerminalNode() # is allow()
Node12.terminal = Node01
Node12.non_terminal = Node03
Node03.type = 422
Node01.type = 0
Node02 = operation_node.TerminalNode() # is deny(), for default_node
Node02.type = 1

v1 = operation_node.ReducedVertice()
v2 = operation_node.ReducedVertice()
v3 = operation_node.ReducedVertice()
v4 = operation_node.ReducedVertice()
v5 = operation_node.ReducedVertice()
v1.value = [v2]
v2.value = [v4]
v3.value = v4
v4.value = "v4"
v5.value = "v5" # shouldn't be a vertice because when comparisons it would call the __eq__ function to compare v4 to other thing which is not a vertice, so error

vertice_database = [ v1, v2, v3 ]
lst_database = [ [], [v1], [v1, v4], [ v1, v2, v5 ] ]

v11 = operation_node.ReducedVertice()
v12 = operation_node.ReducedVertice()
v13 = operation_node.ReducedVertice()
v14 = operation_node.ReducedVertice()
v15 = operation_node.ReducedVertice()
v11.value = v15
v12.value = [v14]
v13.value = v15
v14.value = v15
v15.value = v14


def re_init():
    v1.value = [v2]
    v2.value = [v4]
    v3.value = v4
    v4.value = "v4"
    v5.value = "v5"
    v11 = operation_node.ReducedVertice()
    v12 = operation_node.ReducedVertice()
    v13 = operation_node.ReducedVertice()
    v14 = operation_node.ReducedVertice()
    v15 = operation_node.ReducedVertice()
    v11.value = v15
    v12.value = [v14]
    v13.value = v15
    v14.value = v15
    v15.value = v14


def reinit(node):
    Node10 = operation_node.OperationNode(42) # for is_non_terminal_allow
    Node10.raw = [100, 101, 102, 103]
    Node00 = operation_node.NonTerminalNode()
    Node10.non_terminal = Node00
    Node11 = operation_node.OperationNode(42) # for is_allow_deny
    Node00.match = Node11
    Node11.type = 0
    Node11.raw = [104, 105, 106, 107, 108]
    Node03 = operation_node.NonTerminalNode() # nothing
    Node21 = operation_node.OperationNode(42) # nothing
    Node21.raw = [200, 201, 202, 203]
    Node22 = operation_node.OperationNode(42) # nothing
    Node22.raw = [ 204, 205, 206, 207]
    Node11.non_terminal = Node03
    Node03.match = Node21
    Node21.type = 1
    Node03.unmatch = Node22
    Node22.type = 1
    Node04 = operation_node.TerminalNode()
    Node21.terminal = Node04
    Node04.type = 0
    Node05 = operation_node.TerminalNode()
    Node22.terminal = Node05
    Node05.type = 1
    Node12 = operation_node.OperationNode(42)
    Node12.raw = [109, 110, 111, 112]
    Node00.unmatch = Node12
    Node12.type = 1
    Node01 = operation_node.TerminalNode() # is allow()
    Node12.terminal = Node01
    Node12.non_terminal = Node03
    Node03.type = 422
    Node01.type = 0
    Node02 = operation_node.TerminalNode() # is deny(), for default_node
    Node02.type = 0
    node = Node10
    Node00.filter_id = 42
    Node00.argument_id = 43
    Node00.match_offset = 44
    Node00.unmatch_offset = 45
    Node03.filter_id = 42
    Node03.argument_id = 43
    Node03.match_offset = 44
    Node03.unmatch_offset = 45
    Node03.filter_id = 42
    Node03.argument_id = 43
    Node03.match_offset = 44
    Node03.unmatch_offset = 45
    return node

Node13 = operation_node.OperationNode(42)
Node13.type = 0
Node13.non_terminal = Node2
Node13.terminal = Node0
Node13.raw = [113, 114, 115, 116]
Node14 = operation_node.OperationNode(42)
Node14.type = 0
Node14.non_terminal = Node2

v21 = operation_node.ReducedVertice()
v21.value = "v21"
v22 = operation_node.ReducedVertice()
v22.value = "v22"
v23 = operation_node.ReducedVertice()
v23.value = "v23"
v24 = operation_node.ReducedVertice()
v24.value = "v24"

e1 = operation_node.ReducedEdge()
e2 = operation_node.ReducedEdge("start", "end")
e3 = operation_node.ReducedEdge(v21, None)
e4 = operation_node.ReducedEdge(v22, v23)
e5 = operation_node.ReducedEdge(v24, v23)

g1 = operation_node.ReducedGraph()
g1.vertices = [ v21, v22 ]
g1.edges = [ e3 ]
g2 = operation_node.ReducedGraph()
g2.vertices = [ v21, v22 ]
g2.edges = []
g3 = operation_node.ReducedGraph()
g3.vertices = [ v21, v22 ]
g3.edges = [ e3, e4, e5 ]
g4 = operation_node.ReducedGraph()
g4.vertices = [ v23 ]

graph_database = [ g1, g2, g3, g4 ]
edge_database = [ e1, e2, e3, e4, e5 ]
data_edge_database = [ (None, None), ("start", "end"), (v21, v22), (v21, None) ]
value_database = [ v21, "v21", "v22", None, "hello"]

def re_init_graph():
    g1.vertices = [ v21, v22 ]
    g1.edges = [ e3 ]
    g2.vertices = [ v21, v22 ]
    g2.edges = []
    g3.vertices = [ v21, v22 ]
    g3.edges = [ e3, e4, e5 ]
    g4.vertices = [ v23 ]
    v21.decision = "ok"
    v22.decision = "yes"
    v23.decision = "no"
    v24.decision = "admit"

class TerminalNode(unittest.TestCase):
    """Test the TerminalNode object
    """
    def test_object_exists(self):
        Node = operation_node.TerminalNode()
        self.assertEqual(Node.TERMINAL_NODE_TYPE_ALLOW, 0x00)
        self.assertEqual(Node.TERMINAL_NODE_TYPE_DENY, 0x01)
        self.assertEqual(Node.type, None)
        self.assertEqual(Node.flags, None)

    def __hash__(self):
        return hash((self.vertice, self.edges, self.final_vertices))

    def test__eq__(self):
        Node1 = operation_node.TerminalNode()
        Node2 = operation_node.TerminalNode()
        self.assertEqual(Node1, Node2)
        self.assertTrue(Node1.__eq__(Node2))
        Node1.TERMINAL_NODE_TYPE_ALLOW = 42
        Node1.TERMINAL_NODE_TYPE_DENY = 43
        Node2.TERMINAL_NODE_TYPE_ALLOW = 44
        Node2.TERMINAL_NODE_TYPE_DENY = 45
        self.assertTrue(Node2.__eq__(Node1))
        Node1.type = int 
        Node2.type = float
        self.assertFalse(Node1.__eq__(Node2))
        Node2.type = int
        self.assertTrue(Node1.__eq__(Node2))
        Node1.flags = 42
        Node2.flags = 43
        self.assertFalse(Node1.__eq__(Node2))
        Node2.flags = 42
        self.assertTrue(Node2.__eq__(Node1))

    def test__str__(self):
    	Node = operation_node.TerminalNode()
    	def test_str(self, Node):
    	    res = Node.__str__()
    	    if res == "allow":
    	        self.assertEqual(Node.type, Node.TERMINAL_NODE_TYPE_ALLOW)
    	    elif res == "deny":
    	        self.assertEqual(Node.type, Node.TERMINAL_NODE_TYPE_DENY)
    	    else:
    	        self.assertEqual(res, "unknown")

    	for type in type_database:
    	    Node.type = type
    	    test_str(self, Node)

    def test_is_allow(self):
        Node = operation_node.TerminalNode()
        for type in type_database:
            for term in TERMINAL_NODE_TYPE_ALLOW_database:
                Node.type = type
                Node.TERMINAL_NODE_TYPE_ALLOW = term
                res = Node.is_allow()
                if res:
                    self.assertTrue(Node.type == Node.TERMINAL_NODE_TYPE_ALLOW)
                else:
                    self.assertFalse(Node.type == Node.TERMINAL_NODE_TYPE_ALLOW)

    def test_is_deny(self):
        Node = operation_node.TerminalNode()
        for type in type_database:
            for term in TERMINAL_NODE_TYPE_DENY_database:
                Node.type = type
                Node.TERMINAL_NODE_TYPE_DENY_database = term
                res = Node.is_deny()
                if res:
                    self.assertTrue(Node.type == Node.TERMINAL_NODE_TYPE_DENY)
                else:
                    self.assertFalse(Node.type == Node.TERMINAL_NODE_TYPE_DENY)
    
class NonTerminalNode(unittest.TestCase):
    """Test the NonTerminalNode object
    """
    # the following functions have already been tested in NonTerminalNode_test.py : __eq__, simplify_list
    # str_debug() here is different of the function in NonterminalNode
    def test_object_exists(self):
        Node = operation_node.NonTerminalNode()
        self.assertEqual(Node.filter_id, None)
        self.assertEqual(Node.filter, None)
        self.assertEqual(Node.argument_id, None)
        self.assertEqual(Node.argument, None)
        self.assertEqual(Node.match_offset, None)
        self.assertEqual(Node.match, None)
        self.assertEqual(Node.unmatch_offset, None)
        self.assertEqual(Node.unmatch, None)

    def test_str_debug(self):
        Node = operation_node.NonTerminalNode()

        def op(s, Node):
            curr_filter = Node.filter
            regex_added = False
            prefix_added = False
            if len(s) == 0:
                s = ".+"
                if not regex_added:
                    regex_added = True
                    if Node.filter == "literal":
                        curr_filter = "regex"
                    else:
                        curr_filter += "-regex"
            else:
                if s[-4:] == "/^^^":
                    curr_filter = "subpath"
                    s = s[:-4]
                if '\\' in s or '|' in s or ('[' in s and ']' in s) or '+' in s:
                    if curr_filter == "subpath":
                        s = s + "/?"
                    if Node.filter == "literal":
                        curr_filter = "regex"
                    else:
                        curr_filter += "-regex"
                    s = s.replace('\\\\.', '[.]')
                    s = s.replace('\\.', '[.]')
                if "${" in s and "}" in s:
                    if not prefix_added:
                        prefix_added = True
                        curr_filter += "-prefix"
            return curr_filter, s

        def test_str(self, Node):
            res = Node.str_debug()
            if res == "(%02x %04x %04x %04x)" % (Node.filter_id, Node.argument_id, Node.match_offset, Node.unmatch_offset):
                self.assertFalse(Node.filter)
            elif res == "(%04x, %04x) (%s)" % (Node.match_offset, Node.unmatch_offset, Node.filter):
                self.assertTrue(Node.filter)
                self.assertFalse(Node.argument)
            elif type(Node.argument) is list:
                if res[:len("(require-any ")] == "(require-any ":
                    self.assertNotEqual(len(Node.argument), 1)
                    Node.argument = Node.simplify_list(Node.argument)
                    self.assertNotEqual(len(Node.argument), 1)
                    res = res[len("(require-any "):] # we supress this first part
                else:
                    self.assertEqual(res[0], '(')
                if res[-1] == ')':
                    self.assertEqual(len(Node.argument), 1)
                    res = res[:-1]
                else:
                    self.assertNotEqual(len(Node.argument), 1)
                res = res.split('\n')
                l = 0
                self.assertEqual(len(Node.argument), len(res))
                for s in Node.argument:
                    curr_filter, s = op(s, Node)
                    if res[l] == '(%04x, %04x) (%s #"%s")\n' % (Node.match_offset, Node.unmatch_offset, curr_filter, s):
                        self.assertIn("regex", curr_filter)
                    else:
                        self.assertEqual(res[l], '(%s "%s")\n' % (curr_filter, s))
                    l += 1

            else:
                s = Node.argument
                curr_filter = Node.filter
                if not "regex" in curr_filter:
                    if '\\' in s or '|' in s or ('[' in s and ']' in s) or '+' in s:
                        if Node.filter == "literal":
                            curr_filter = "regex"
                        else:
                            curr_filter += "-regex"
                        s = s.replace('\\\\.', '[.]')
                        s = s.replace('\\.', '[.]')
                if "${" in s and "}" in s:
                    if not "prefix" in curr_filter:
                        curr_filter += "-prefix"
                self.assertEqual(res, "(%04x, %04x) (%s %s)" % (Node.match_offset, Node.unmatch_offset, curr_filter, s))

        Node.filter_id = 42
        Node.argument_id = 43
        Node.match_offset = 44
        Node.unmatch_offset = 45
        for filter in filter_database2:
            Node.filter = filter
            for argument in argument_database:
                Node.argument = argument
                test_str(self, Node)

# the function __str__ is very similar to str_debug, the only possible differences are the return but the construction is the same
    def test__str__(self):
        Node = operation_node.NonTerminalNode()

        def op(s, Node):
            curr_filter = Node.filter
            regex_added = False
            prefix_added = False
            if len(s) == 0:
                s = ".+"
                if not regex_added:
                    regex_added = True
                    if Node.filter == "literal":
                        curr_filter = "regex"
                    else:
                        curr_filter += "-regex"
            else:
                if s[-4:] == "/^^^":
                    curr_filter = "subpath"
                    s = s[:-4]
                if '\\' in s or '|' in s or ('[' in s and ']' in s) or '+' in s:
                    if curr_filter == "subpath":
                        s = s + "/?"
                    if Node.filter == "literal":
                        curr_filter = "regex"
                    else:
                        curr_filter += "-regex"
                    s = s.replace('\\\\.', '[.]')
                    s = s.replace('\\.', '[.]')
                if "${" in s and "}" in s:
                    if not prefix_added:
                        prefix_added = True
                        curr_filter += "-prefix"
            return curr_filter, s

        def test_str(self, Node):
            res = Node.__str__()
            if res == "(%02x %04x %04x %04x)" % (Node.filter_id, Node.argument_id, Node.match_offset, Node.unmatch_offset):
                self.assertFalse(Node.filter)
            elif res == "(%s)" % (Node.filter):
                self.assertTrue(Node.filter)
                self.assertFalse(Node.argument)
            elif type(Node.argument) is list:
                if res[:len("(require-any ")] == "(require-any ":
                    self.assertNotEqual(len(Node.argument), 1)
                    Node.argument = Node.simplify_list(Node.argument)
                    self.assertNotEqual(len(Node.argument), 1)
                    res = res[len("(require-any "):] # we supress this first part
                else:
                    self.assertEqual(res[0], '(')
                if res[-1] == ')':
                    self.assertEqual(len(Node.argument), 1)
                    res = res[:-1]
                else:
                    self.assertNotEqual(len(Node.argument), 1)
                res = res.split('\n')
                l = 0
                self.assertEqual(len(Node.argument), len(res))
                for s in Node.argument:
                    curr_filter, s = op(s, Node)
                    if res[l] == '(%s #"%s")\n' % (curr_filter, s):
                        self.assertIn("regex", curr_filter)
                    else:
                        self.assertEqual(res[l], '(%s "%s")\n' % (curr_filter, s))
                    l += 1

            else:
                s = Node.argument
                curr_filter = Node.filter
                if not "regex" in curr_filter:
                    if '\\' in s or '|' in s or ('[' in s and ']' in s) or '+' in s:
                        if Node.filter == "literal":
                            curr_filter = "regex"
                        else:
                            curr_filter += "-regex"
                        s = s.replace('\\\\.', '[.]')
                        s = s.replace('\\.', '[.]')
                if "${" in s and "}" in s:
                    if not "prefix" in curr_filter:
                        curr_filter += "-prefix"
                self.assertEqual(res, "(%s %s)" % (curr_filter, s))

        Node.filter_id = 42
        Node.argument_id = 43
        Node.match_offset = 44
        Node.unmatch_offset = 45
        for filter in filter_database2:
            Node.filter = filter
            for argument in argument_database:
                Node.argument = argument
                test_str(self, Node)

    def test_str_not(self):
        Node = operation_node.NonTerminalNode()

        def op(s, Node):
            curr_filter = Node.filter
            regex_added = False
            prefix_added = False
            if len(s) == 0:
                s = ".+"
                if not regex_added:
                    regex_added = True
                    if Node.filter == "literal":
                        curr_filter = "regex"
                    else:
                        curr_filter += "-regex"
            else:
                if s[-4:] == "/^^^":
                    curr_filter = "subpath"
                    s = s[:-4]
                if '\\' in s or '|' in s or ('[' in s and ']' in s) or '+' in s:
                    if curr_filter == "subpath":
                        s = s + "/?"
                    if Node.filter == "literal":
                        curr_filter = "regex"
                    else:
                        curr_filter += "-regex"
                    s = s.replace('\\\\.', '[.]')
                    s = s.replace('\\.', '[.]')
                if "${" in s and "}" in s:
                    if not prefix_added:
                        prefix_added = True
                        curr_filter += "-prefix"
            return curr_filter, s

        def test_str(self, Node):
            res = Node.str_not()
            if res == "(%02x %04x %04x %04x)" % (Node.filter_id, Node.argument_id, Node.match_offset, Node.unmatch_offset):
                self.assertFalse(Node.filter)
            elif res == "(%s)" % (Node.filter):
                self.assertTrue(Node.filter)
                self.assertFalse(Node.argument)
            elif type(Node.argument) is list:
                if res[:len("(require-any ")] == "(require-any ":
                    self.assertNotEqual(len(Node.argument), 1)
                    Node.argument = Node.simplify_list(Node.argument)
                    self.assertNotEqual(len(Node.argument), 1)
                    res = res[len("(require-any "):] # we supress this first part
                else:
                    self.assertEqual(res[0], '(')
                if res[-1] == ')':
                    self.assertEqual(len(Node.argument), 1)
                    res = res[:-1]
                else:
                    self.assertNotEqual(len(Node.argument), 1)
                res = res.split('\n')
                l = 0
                self.assertEqual(len(Node.argument), len(res))
                for s in Node.argument:
                    curr_filter, s = op(s, Node)
                    if res[l] == '(require-not (%s #"%s"))\n' % (curr_filter, s):
                        self.assertIn("regex", curr_filter)
                    else:
                        self.assertEqual(res[l], '(require-not (%s "%s"))\n' % (curr_filter, s))
                    l += 1

            else:
                s = Node.argument
                curr_filter = Node.filter
                if not "regex" in curr_filter:
                    if '\\' in s or '|' in s or ('[' in s and ']' in s) or '+' in s:
                        if Node.filter == "literal":
                            curr_filter = "regex"
                        else:
                            curr_filter += "-regex"
                        s = s.replace('\\\\.', '[.]')
                        s = s.replace('\\.', '[.]')
                if "${" in s and "}" in s:
                    if not "prefix" in curr_filter:
                        curr_filter += "-prefix"
                self.assertEqual(res, "(%s %s)" % (curr_filter, s))

        Node.filter_id = 42
        Node.argument_id = 43
        Node.match_offset = 44
        Node.unmatch_offset = 45
        for filter in filter_database2:
            Node.filter = filter
            for argument in argument_database:
                Node.argument = argument
                test_str(self, Node)


    def test_values(self):
        Node = operation_node.NonTerminalNode()
        def test(self, Node):
            res = Node.values()
            if res == (Node.filter, Node.argument):
                self.assertTrue(Node.filter)
            else:
                self.assertFalse(Node.filter)
                self.assertEqual(res, ("%02x" % Node.filter_id, "%04x" % (Node.argument_id)))

        for filter in filter_database:
            Node.filter = filter
            for argument in argument_database:
                Node.argument = argument
                for id in id_database2:
                    Node.filter_id = id
                    for id2 in id_database2:
                        Node.argument_id = id2
                        test(self, Node)

    def test_is_entitlement_start(self):
        Node = operation_node.NonTerminalNode()
        def test(self, Node):
            res = Node.is_entitlement_start()
            if Node.filter_id == 0x1e or Node.filter_id == 0xa0:
                self.assertTrue(res)
            else:
                self.assertFalse(res)

        for id in id_database:
            Node.filter_id = id
            test(self, Node)

    def test_is_entitlement(self):
        Node = operation_node.NonTerminalNode()
        def test(self, Node):
            res = Node.is_entitlement()
            if Node.filter_id == 0x1e or Node.filter_id == 0x1f or Node.filter_id == 0x20 or Node.filter_id == 0xa0:
                self.assertTrue(res)
            else:
                self.assertFalse(res)

        for id in id_database:
            Node.filter_id = id
            test(self, Node)

    def test_is_last_regular_expression(self):
        Node = operation_node.NonTerminalNode()
        def test_is(self, Node):
            res = Node.is_last_regular_expression()
            if res:
                self.assertTrue(Node.filter_id == 0x81 and Node.argument_id == num_regex - 1) # num_regex is not defined
            else:
                self.assertFalse(Node.filter_id == 0x81 and Node.argument_id == num_regex - 1)

        for filter_id in id_database:
            Node.filter_id = filter_id
            for id in id_database:
                Node.argument_id = id
                test_is(self, Node)

    # convert_filter(self) has already been tested in NonTerminalNode_test, although we don't know either what is the function convert_fn

    # the following functions were defined also in NonTerminalNode but we didn't known here the functions is_deny() and is_allow(), as well as is_terminal() and is_non_terminal()
    
    def test_is_non_terminal_deny(self):
        Node = operation_node.NonTerminalNode()
        def test_is(self, Node):
            res = Node.is_non_terminal_deny()
            if res is not None:
                self.assertEqual(res, Node.unmatch.terminal.is_deny())
                self.assertTrue(Node.match.is_non_terminal() and Node.unmatch.is_terminal())
            else:
                self.assertFalse(Node.match.is_non_terminal() and Node.unmatch.is_terminal())
                self.assertEqual(res, None)

        for match in [Node2, Node3, Node4, Node5, Node6]:
            Node.match = match
            for unmatch in [Node2, Node3, Node4, Node5, Node6]:
                Node.unmatch = unmatch
                test_is(self, Node)

    def test_is_non_terminal_allow(self):
        Node = operation_node.NonTerminalNode()
        def test_is(self, Node):
            res = Node.is_non_terminal_allow()
            if res is not None:
                self.assertEqual(res, Node.unmatch.terminal.is_allow())
                self.assertTrue(Node.match.is_non_terminal() and Node.unmatch.is_terminal())
            else:
                self.assertFalse(Node.match.is_non_terminal() and Node.unmatch.is_terminal())
                self.assertEqual(res, None)

        for match in [Node2, Node3, Node4, Node5, Node6]:
            Node.match = match
            for unmatch in [Node2, Node3, Node4, Node5, Node6]:
                Node.unmatch = unmatch
                test_is(self, Node)

    def test_is_non_terminal_non_terminal(self):
        Node = operation_node.NonTerminalNode()
        def test_is(self, Node):
            res = Node.is_non_terminal_non_terminal()
            self.assertEqual(res, Node.match.is_non_terminal() and Node.unmatch.is_non_terminal())

        for match in [Node2, Node3, Node4, Node5, Node6]:
            Node.match = match
            for unmatch in [Node2, Node3, Node4, Node5, Node6]:
                Node.unmatch = unmatch
                test_is(self, Node)

    def test_is_allow_non_terminal(self):
        Node = operation_node.NonTerminalNode()
        def test_is(self, Node):
            res = Node.is_allow_non_terminal()
            if res is not None:
                self.assertEqual(res, Node.match.terminal.is_allow())
                self.assertTrue(Node.match.is_terminal() and Node.unmatch.is_non_terminal())
            else:
                self.assertFalse(Node.match.is_terminal() and Node.unmatch.is_non_terminal())
                self.assertEqual(res, None)

        for match in [Node2, Node3, Node4, Node5, Node6]:
            Node.match = match
            for unmatch in [Node2, Node3, Node4, Node5, Node6]:
                Node.unmatch = unmatch
                test_is(self, Node)

    def test_is_deny_non_terminal(self):
        Node = operation_node.NonTerminalNode()
        def test_is(self, Node):
            res = Node.is_deny_non_terminal()
            if res is not None:
                self.assertEqual(res, Node.match.terminal.is_deny())
                self.assertTrue(Node.match.is_terminal() and Node.unmatch.is_non_terminal())
            else:
                self.assertFalse(Node.match.is_terminal() and Node.unmatch.is_non_terminal())
                self.assertEqual(res, None)

        for match in [Node2, Node3, Node4, Node5, Node6]:
            Node.match = match
            for unmatch in [Node2, Node3, Node4, Node5, Node6]:
                Node.unmatch = unmatch
                test_is(self, Node)

    def test_is_deny_allow(self):
        Node = operation_node.NonTerminalNode()
        def test_is(self, Node):
            res = Node.is_deny_allow()
            if res is not None:
                self.assertEqual(res, Node.match.terminal.is_deny() and NNode.unmatch.terminal.is_allow() )
                self.assertTrue(Node.match.is_terminal() and Node.unmatch.is_terminal())
            else:
                self.assertFalse(Node.match.is_terminal() and Node.unmatch.is_terminal())
                self.assertEqual(res, None)

        for match in [Node2, Node3, Node4, Node5, Node6]:
            Node.match = match
            for unmatch in [Node2, Node3, Node4, Node5, Node6]:
                Node.unmatch = unmatch
                test_is(self, Node)
    
    def test_is_allow_deny(self):
        Node = operation_node.NonTerminalNode()
        def test_is(self, Node):
            res = Node.is_allow_deny()
            if res is not None:
                self.assertEqual(res, Node.match.terminal.is_allow() and NNode.unmatch.terminal.is_deny() )
                self.assertTrue(Node.match.is_terminal() and Node.unmatch.is_terminal())
            else:
                self.assertFalse(Node.match.is_terminal() and Node.unmatch.is_terminal())
                self.assertEqual(res, None)

        for match in [Node2, Node3, Node4, Node5, Node6]:
            Node.match = match
            for unmatch in [Node2, Node3, Node4, Node5, Node6]:
                Node.unmatch = unmatch
                test_is(self, Node)


class OperationNode(unittest.TestCase):
    
    """Test the OperationNode object
    """
    def test_object_exists(self):
        Node = operation_node.OperationNode(42)
        self.assertEqual(Node.OPERATION_NODE_TYPE_NON_TERMINAL, 0x00)
        self.assertEqual(Node.OPERATION_NODE_TYPE_TERMINAL, 0x01)
        self.assertEqual(Node.offset, 42)
        self.assertEqual(Node.raw, [])
        self.assertEqual(Node.type, None)
        self.assertEqual(Node.terminal, None)
        self.assertEqual(Node.non_terminal, None)

    def test_init_with_no_args(self):
        """Tests the initialisation with no arguments
        """
        with self.assertRaises(TypeError):
            operation_node.OperationNode()

    def test_is_terminal(self):
        Node = operation_node.OperationNode(42) # 42 is an exemple
        for type in type_database:
            Node.type = type
            for op in operation_database:
                Node.OPERATION_NODE_TYPE_TERMINAL = op
                res = Node.is_terminal()
                if type == op:
                    self.assertTrue(res)
                else:
                    self.assertFalse(res)

    def test_is_non_terminal(self):
        Node = operation_node.OperationNode(42) # 42 is an exemple
        for type in type_database:
            Node.type = type
            for op in operation_database:
                Node.OPERATION_NODE_TYPE_NON_TERMINAL = op
                res = Node.is_non_terminal()
                if type == op:
                    self.assertTrue(res)
                else:
                    self.assertFalse(res)

# some lines seem unseless in the function parse_terminal
    def test_parse_terminal(self):
        Node = operation_node.OperationNode(42)
        Node.raw = [42, 43, 44] # else there will be error 'index out of range'
        for ios_version in range (1, 15):
            Node.parse_terminal(ios_version)
            self.assertEqual(Node.terminal.parent, Node)
            self.assertEqual(Node.terminal.type, Node.raw[2 if ios_version <12 else 1] & 0x01)
            self.assertEqual(Node.terminal.flags, Node.raw[2 if ios_version <12 else 1] & 0xfe)

    def test_parse_non_terminal(self):
        Node = operation_node.OperationNode(42)
        Node.raw = [i for i in range (42, 52)] # for instance
        Node.parse_non_terminal()
        self.assertEqual(Node.non_terminal.parent, Node)
        self.assertEqual(Node.non_terminal.filter_id, Node.raw[1])
        self.assertEqual(Node.non_terminal.argument_id, Node.raw[2] + (Node.raw[3] << 8) )
        self.assertEqual(Node.non_terminal.match_offset, Node.raw[4] + (Node.raw[5] << 8) )
        self.assertEqual(Node.non_terminal.unmatch_offset, Node.raw[6] + (Node.raw[7] << 8) )

    def test_parse_raw(self):
        Node = operation_node.OperationNode(42)
        Node.raw = [i for i in range (42, 52)] # for instance
        for ios_version in range(1,15):
            Node.parse_raw(ios_version)
            if Node.terminal is not None:
                self.assertTrue(Node.is_terminal())
                self.assertIsNone(Node.non_terminal, None)
            elif Node.non_terminal is not None:
                self.assertFalse(Node.is_terminal())
                self.assertTrue(Node.is_non_terminal())
            else:
                self.assertFalse(Node.is_terminal())
                self.assertFalse(Node.is_non_terminal())

#  this function is difficult to test, as it can be a loop and we don't know what is convert_fn
# /!\ Node.non_terminal is a Node, and there are a lot of litte details like that that must be verified in order for the original function to work without errors
    def test_convert_filter(self):
    	Node = operation_node.OperationNode(42)
    	for term in [ NNode, Node2, Node3, Node4, Node5, Node6 ]: # defined at the beginning of the file, NNode is class NonTerminalNode, Node_n OperationNode, for some of them is_non_terminal is true
    	    Node.non_terminal = term
    	    for typee in type_database:
    	        Node.type = typee

                Node.filter_id = 43
                Node.argument_id = 44
                def convert_fn(self, convert_fn, f, regex_list, ios_major_version,keep_builtin_filters, global_vars, base_addr):
                    return 42, 43 # I don't know what is this function, I invented one
                f = None
                ios_major_version = 10
                keep_builtin_filters = "\n"
                global_vars = f
                regex_list = ["hello"]
                base_addr = 0.99 # these variables are chosen randomly
    	        Node.convert_filter( convert_fn, f, regex_list, ios_major_version, keep_builtin_filters, global_vars, base_addr)
    	        if Node.non_terminal.parent is not None and Node.non_terminal.filter is not None: # for the only term wich change filter, I have change the 'parent' to recognize it, and know that it has an object 'filter', but I don't know exactly how to test this function
    	            self.assertTrue(Node.is_non_terminal())
    	            Node.non_terminal.filter = None

    def test_str_debug(self):
        Node = operation_node.OperationNode(42) # must be an int here
        for typee in type_database:
            Node.type = typee
            res = Node.str_debug()
            if res == "(%02x) " % (Node.offset) + "terminal: " + str(Node.terminal):
                self.assertTrue(Node.is_terminal())
            elif res == "(%02x) " % (Node.offset) + "non-terminal: " + str(Node.non_terminal):
                self.assertFalse(Node.is_terminal())
                self.assertTrue(Node.is_non_terminal())
            else:
                self.assertFalse(Node.is_terminal())
                self.assertFalse(Node.is_non_terminal())
                self.assertEqual(res, "(%02x) " % (Node.offset) )

    def test__str__(self):
        Node = operation_node.OperationNode(42)
        Node.terminal = "hello"
        Node.non_terminal = "hi"
        for typee in type_database:
            Node.type = typee
            res = Node.__str__()
            if res == str(Node.terminal):
                self.assertTrue(Node.is_terminal())
            elif res == str(Node.non_terminal):
                self.assertTrue(Node.is_non_terminal())
                self.assertFalse(Node.is_terminal())
            else:
                self.assertEqual(res, "")
                self.assertFalse(Node.is_non_terminal())
                self.assertFalse(Node.is_terminal())

    def test_str_not(self):
        Node = operation_node.OperationNode(42)
        Node.terminal = "hello"
        Node.non_terminal = Node2 # must be of class OperationNode in order for the function to run without errors
        Node2.terminal = "hello2"
        Node2.non_terminal = "hi"
        for typee in type_database:
            Node.type = typee
            for type2 in ["0x00", 42, 1, None, True]: # I have supress the int 0 because it will be another loop, complicated and useless; and also False, beacuse False==0 return True !!!
                Node2.type = type2
                res = Node.str_not()
                if res == str(Node.terminal):
                    self.assertTrue(Node.is_terminal())
                elif res != "":
                    if res == str(Node.non_terminal.str_not()):                        
                        self.assertTrue(Node.is_non_terminal())
                        self.assertFalse(Node.is_terminal())
                    else:
                        self.assertTrue(1==2) # we musn't arrive here
                else:
                    self.assertEqual(res, "")
                    # self.assertFalse(Node.is_non_terminal()) can be True if loop
                    self.assertFalse(Node.is_terminal())

    def test_values(self):
        Node = operation_node.OperationNode(42)
        Node.non_terminal = Node2
        Node2.type = 1 # otherwise, Node2.non_terminal must also be of class OperationNode
        for typee in type_database:
            Node.type = typee
            res = Node.values()
            if Node.is_terminal():
                self.assertEqual(res, (None, None))
            else:
                self.assertEqual(res, Node.non_terminal.values())
    
    def test__eq__(self):
        Node = operation_node.OperationNode(42)
        def test_eq(Node, other):
            res = Node.__eq__(other)
            if res:
                self.assertEqual(Node.raw, other.raw)
            else:
                self.assertNotEqual(Node.raw, other.raw)

        Node.raw = [1, "hello", True]
        other = operation_node.OperationNode(43)
        test_eq(Node, other)
        self.assertFalse(Node.__eq__(other))
        other.OPERATION_NODE_TYPE_TERMINAL = 2
        other.OPERATION_NODE_TYPE_NON_TERMINAL = 3
        other.type = 5
        other.terminal = 6
        other.non_terminal = 7
        other.raw = [1, "hello", True]
        test_eq(Node, other)
        self.assertTrue(Node.__eq__(other))

    def test__hash__(self):
        Node = operation_node.OperationNode(42)
        Node.raw = [ 42, 43, 44, 45 ] # we need at least len()=4
        res = Node.__hash__()
        self.assertEqual(struct.pack('<I', res), ''.join([chr(v) for v in Node.raw[:4]]))

    def test_has_been_processed(self):
        processed_nodes = operation_node.processed_nodes
        for node in [Node0, Node01, Node02 ]:
            res = operation_node.has_been_processed(node)
            if node in processed_nodes:
                self.assertTrue(res)
            else:
                self.assertFalse(res)

    def test_build_operation_node(self):
        offset = random.randint(-100, 100) # for instance
        raw = [ random.randint(-100, 100) for i in range(10)] # for instance
        ios_version = random.randint(1, 15)
        node = operation_node.build_operation_node(raw, offset, ios_version)
        other = operation_node.OperationNode((offset - operation_node.operations_offset)/8)
        other.raw = raw
        other.parse_raw(ios_version)
        Node = operation_node.OperationNode(42)
        #self.assertTrue(Node.__eq__(other))
        self.assertTrue(other.__eq__(node))

# /!\ the file f must be enough long, len(f) >= 8*num_operation_nodes 
    def test_build_operation_nodes(self):
        def test_build(self, f, num_operation_nodes, ios_version):
            f.seek(0) # come back to the beginning of the file
            if ios_version <= 12:
                self.assertEqual(operation_node.operations_offset, 0)
            else:
                self.assertEqual(operation_node.operations_offset, f.tell())

            res = operation_node.build_operation_nodes(f, num_operation_nodes, ios_version)
            f.seek(0)
            for i in range(len(res)):
                self.assertEqual(res[i], operation_node.build_operation_node(struct.unpack("<8B", f.read(8)), f.tell(), ios_version))
                if res[i].is_non_terminal():
                    for j in range(len(res)):
                        if res[i].non_terminal.match == res[j]:
                            self.assertTrue(res[i].non_terminal.match_offset == res[j].offset)
                        if res[i].non_terminal.unmatch == res[j]:
                            self.assertTrue(res[i].non_terminal.unmatch_offset == res[j].offset)
            self.assertEqual(len(res), num_operation_nodes)

        myFile = open("File.txt", "w+")
        myFile.write("Hello everyone !\nNice to meet you.")
        myFile.close()
        myFile = open("File.txt", "r")
        for ios_version in range(1, 15):
            for num_operation_nodes in range(0, 3):
                test_build(self, myFile, num_operation_nodes, ios_version)
        myFile.close()
        os.remove("File.txt")

    def test_find_operation_node_by_offset(self):
        def test_find(self, operation_nodes, offset):
            res = operation_node.find_operation_node_by_offset(operation_nodes, offset)
            bo = False
            for node in operation_nodes:
                if node.offset == offset:
                    self.assertEqual(res, node)
                    bo = True
            if not bo:
                self.assertFalse(res)
        node1 = operation_node.OperationNode(24)
        node2 = operation_node.OperationNode(42)
        test_find(self, [node1, node2], 24)

    def test_ong_mark_not(self):
        node = operation_node.OperationNode(42)
        node.raw = [10, 11, 12, 13]
        NNode = operation_node.NonTerminalNode()
        node.non_terminal = NNode # only NonTerminalNode have 'match' object
        NNode.match = 42
        NNode.unmatch = 24
        old_match = deepcopy(NNode.match)
        old_unmatch = deepcopy(NNode.unmatch)
        g = {node: 42}
        g[node] = {"not": False}
        NNode.match_offset = 43
        NNode.match_offset = 34
        old_match_offset = deepcopy(NNode.match_offset)
        old_unmatch_offset = deepcopy(NNode.unmatch_offset)
        nodes_to_process = []

        operation_node.ong_mark_not(g, node, node.parent, nodes_to_process)
        self.assertTrue(g[node]["not"])
        self.assertEqual(node.non_terminal.match, old_unmatch)
        self.assertEqual(node.non_terminal.unmatch, old_match)
        self.assertEqual(node.non_terminal.match_offset, old_unmatch_offset)
        self.assertEqual(node.non_terminal.unmatch_offset, old_match_offset)

    def test_ong_end_path(self):
        g = {}
        node = operation_node.OperationNode(42)
        node.raw = [10, 11, 12, 13]
        NNode = operation_node.NonTerminalNode()
        node.non_terminal = NNode
        node2 = operation_node.OperationNode(43)
        NNode.match = node2 # only OperationNode have 'terminal' object
        node2.terminal = 422
        g[node] = {"type": {"hello"} }
        nodes_to_process = ""

        operation_node.ong_end_path(g, node, node.parent, nodes_to_process)
        self.assertEqual(g[node]["decision"], str(node.non_terminal.match.terminal) )
        self.assertEqual(g[node]["type"], {"hello", "final"})

    def test_ong_add_to_path(self):
        node = operation_node.OperationNode(42)
        node.raw = [10, 11, 12, 13, 14]
        NNode = operation_node.NonTerminalNode()
        node.non_terminal = NNode
        node2 = operation_node.OperationNode(43)
        node2.raw = [20, 21, 22, 23, 24]
        NNode.match = node2
        processed_nodes = operation_node.processed_nodes
        g = { node: { "list": {"hello"} } }
        nodes_to_process = { "hello2" }

        operation_node.ong_add_to_path(g, node, NNode.parent, nodes_to_process)
        if not operation_node.has_been_processed(node.non_terminal.match): # if node2 not in
            self.assertEqual( g[node]["list"], {"hello", node.non_terminal.match })
            self.assertEqual( nodes_to_process, {"hello2", (node, node.non_terminal.match)})
        else:
            self.assertEqual( g[node]["list"], {"hello" })
            self.assertEqual( nodes_to_process, {"hello2" })

    def test_ong_add_to_parent_path(self):
        node = operation_node.OperationNode(42)
        node.raw = [10, 11, 12, 13, 14]
        NNode = operation_node.NonTerminalNode()
        node.non_terminal = NNode
        node2 = operation_node.OperationNode(43)
        node2.raw = [20, 21, 22, 23, 24]
        NNode.unmatch = node2
        processed_nodes = operation_node.processed_nodes
        g = { node: { "list": {"hello"} } }
        nodes_to_process = { "hello2" }
        g[True] = { "list": {"hello"}}

        for parent_node in [ node, False, True ]:
            nodes_to_process = { "hello2" }
            operation_node.ong_add_to_parent_path(g, node, parent_node, nodes_to_process)
            if not operation_node.has_been_processed(node.non_terminal.unmatch):
                if parent_node:
                    self.assertEqual( g[parent_node]["list"], {"hello", node.non_terminal.unmatch })
                self.assertEqual( nodes_to_process, {"hello2", (parent_node, node.non_terminal.unmatch)})
            else:
                self.assertEqual( nodes_to_process, {"hello2" })

    
    def test_build_operation_node_graph(self):
    # here, we will analyse the nodes in the result.keys() of the function to see if they have the right to be in the return, and then analyse all the nodes and if they should have been in result.keys()
    # this function is complex so I will use 1 exemple to test the first part of the function, and others for the rest
        def test_build(self, node, default_node):
            copy_node = deepcopy(node) # because node will be modified in build_... through ong_mark_not()

            bo = operation_node.has_been_processed(node)
            res = operation_node.build_operation_node_graph(node, default_node)
            if node.is_terminal() or default_node.is_non_terminal() or bo:
                self.assertIsNone(res)
            else:
            	parent_node = None # we must began with that, however "start" will be add to g[node]["list"] and the fonction clean_... will run with start_nodes not empty
            	tab = {}
                def build(node, parent_node, res, tab, copy_node):
                    self.assertIn(node, res.keys())
                    if default_node.terminal.is_deny():
                        if node not in tab.keys():
                            tab[node] = 0 # this will count the number of objects that should be in g[node]["list"]
                                                       
                        if res[node]["not"]: # if True, node has got through ong_mark_not
                            if copy_node.non_terminal.is_non_terminal_allow(): # so node has got through ong_add_to_parent_path
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_deny())
                                self.assertIsNotNone(res[node]["decision"])
                                if not operation_node.has_been_processed(copy_node.non_terminal.unmatch):
                                    if parent_node:
                                        # self.assertTrue(copy_node.non_terminal.unmatch in res[parent_node]["list"]) # because the objects in ["list"] have been modified
                                        tab[parent_node] += 1
                                    build(node.non_terminal.unmatch, parent_node, res, tab, copy_node.non_terminal.match) # beware, match and unmatch have been inverted !
                            elif res[node]["decision"] is not None:
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_deny())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_allow())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_non_terminal())
                                self.assertFalse(copy_node.non_terminal.is_allow_non_terminal())
                                self.assertFalse(copy_node.non_terminal.is_deny_non_terminal())
                                self.assertTrue(copy_node.non_terminal.is_deny_allow())
                            else:
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_deny())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_allow())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_non_terminal())
                                self.assertFalse(copy_node.non_terminal.is_allow_non_terminal())
                                self.assertTrue(copy_node.non_terminal.is_deny_non_terminal())
                                self.assertTrue(res[node]["not"]) # the rest of the function has already been tested
                                # self.assertTrue(node.non_terminal.match in g[node]["list"])
                                tab[node] += 1
                                build(node.non_terminal.unmatch, node, res, tab, copy_node.non_terminal.match)
                        
                        elif res[node]["decision"] is not None: # through ong_end_path()
                            if copy_node.non_terminal.is_allow_non_terminal():
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_deny())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_allow())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_non_terminal())
                                if not operation_node.has_been_processed(copy_node.non_terminal.unmatch):
                                    if parent_node:
                                        # self.assertTrue(copy_node.non_terminal.unmatch in res[parent_node]["list"])
                                        tab[parent_node] += 1
                                    build(copy_node.non_terminal.unmatch, parent_node, res, tab, copy_node.non_terminal.unmatch)
                            else:
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_deny())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_allow())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_non_terminal())
                                self.assertFalse(copy_node.non_terminal.is_allow_non_terminal())
                                self.assertFalse(copy_node.non_terminal.is_deny_non_terminal())
                                self.assertFalse(copy_node.non_terminal.is_deny_allow())
                                self.assertTrue(copy_node.non_terminal.is_allow_deny())

                        else:
                            self.assertFalse(operation_node.has_been_processed(copy_node.non_terminal.match))
                            #if res[node]["not"] == False: # node has not passed in ong_mark_not
                            if copy_node.non_terminal.is_non_terminal_deny():
                                # self.assertEqual(tab[parent_node], len(res[parent_node]["list"])) # no more modification for the parent_node
                                # self.assertTrue(copy_node.non_terminal.match in res[node]["list"]) # g[node]["list"] can be modify by the function clean_...
                                tab[node] += 1
                                build(copy_node.non_terminal.match, node, res, tab, copy_node)
                            else:
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_deny())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_allow())
                                self.assertTrue(copy_node.non_terminal.is_non_terminal_non_terminal())
                                # self.assertTrue(copy_node.non_terminal.match in res[node]["list"])
                                tab[node] += 1
                                build(copy_node.non_terminal.match, node, res, tab, copy_node.non_terminal.match)
                                if not operation_node.has_been_processed(copy_node.non_terminal.unmatch):
                                    if parent_node: # if True, res[parent_node]["list"] can be modified, else not
                                        # self.assertTrue(copy_node.non_terminal.unmatch in res[parent_node]["list"]) # the rest of the function has already been tested in the test-function itself
                                        tab[parent_node] += 1
                                    build(copy_node.non_terminal.unmatch, parent_node, res, tab, copy_node.non_terminal.unmatch)
                                
                    elif default_node.terminal.is_allow():
                        if node not in tab.keys():
                            tab[node] = 0 # this will count the number of objects that should be in g[node]["list"]
                                                       
                        if res[node]["not"]: # if True, node has got through ong_mark_not
                            if copy_node.non_terminal.is_non_terminal_deny(): # so node has got through ong_add_to_parent_path
                                self.assertIsNotNone(res[node]["decision"])
                                if not operation_node.has_been_processed(copy_node.non_terminal.unmatch):
                                    if parent_node:
                                        tab[parent_node] += 1
                                    build(node.non_terminal.unmatch, parent_node, res, tab, copy_node.non_terminal.match) # beware, match and unmatch have been inverted !
                            elif res[node]["decision"] is not None: # through ong_end_path()
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_deny())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_allow())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_non_terminal())
                                self.assertFalse(copy_node.non_terminal.is_allow_non_terminal())
                                self.assertFalse(copy_node.non_terminal.is_deny_non_terminal())
                                self.assertFalse(copy_node.non_terminal.is_deny_allow())
                                self.assertTrue(copy_node.non_terminal.is_allow_deny())
                            else:
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_deny())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_allow())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_non_terminal())
                                self.assertTrue(copy_node.non_terminal.is_allow_non_terminal())
                                self.assertTrue(res[node]["not"]) # the rest of the function has already been tested
                                tab[node] += 1
                                build(node.non_terminal.unmatch, node, res, tab, copy_node.non_terminal.match)
                        
                        elif res[node]["decision"] is not None:
                            if copy_node.non_terminal.is_deny_non_terminal():
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_deny())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_allow())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_non_terminal())
                                self.assertFalse(copy_node.non_terminal.is_allow_non_terminal())
                                if not operation_node.has_been_processed(copy_node.non_terminal.unmatch):
                                    if parent_node:
                                        tab[parent_node] += 1
                                    build(copy_node.non_terminal.unmatch, parent_node, res, tab, copy_node.non_terminal.unmatch)
                            else:
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_deny())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_allow())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_non_terminal())
                                self.assertFalse(copy_node.non_terminal.is_allow_non_terminal())
                                self.assertFalse(copy_node.non_terminal.is_deny_non_terminal())
                                self.assertTrue(copy_node.non_terminal.is_deny_allow())

                        else:
                            self.assertFalse(operation_node.has_been_processed(copy_node.non_terminal.match))
                            if copy_node.non_terminal.is_non_terminal_allow():
                                tab[node] += 1
                                build(copy_node.non_terminal.match, node, res, tab, copy_node.non_terminal.match)
                            else:
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_deny())
                                self.assertFalse(copy_node.non_terminal.is_non_terminal_allow())
                                self.assertTrue(copy_node.non_terminal.is_non_terminal_non_terminal())
                                tab[node] += 1
                                build(copy_node.non_terminal.match, node, res, tab, copy_node.non_terminal.match)
                                if not operation_node.has_been_processed(copy_node.non_terminal.unmatch):
                                    if parent_node: # if True, res[parent_node]["list"] can be modified, else not
                                        tab[parent_node] += 1
                                    build(copy_node.non_terminal.unmatch, parent_node, res, tab, copy_node.non_terminal.unmatch)

                    else: # no change for g={}
                        self.assertEqual(res, {} )

                build(node, parent_node, res, tab, copy_node)
                # self.assertEqual(res, {})

        for node in [ Node10 ]:
            default_node = operation_node.OperationNode(42)
            default_node.terminal = Node02
            Node00.filter_id = 42
            Node00.argument_id = 43
            Node00.match_offset = 44
            Node00.unmatch_offset = 45
            Node03.filter_id = 42
            Node03.argument_id = 43
            Node03.match_offset = 44
            Node03.unmatch_offset = 45
            test_build(self, node, default_node)
            node = reinit(node) # because node has changed...
            Node02.type = 0
            test_build(self, node, default_node)
            Node02.type = 1
            


    # error on the logger_file...
    def test_print_operation_node_graph(self):
        for g in g_database:
            self.assertIsNone(operation_node.print_operation_node_graph(g))
            with open("logger.config", "r+") as log_file:
                lines = log_file.read().split('\n')
                for i in range(len(g.keys())):
                    b=1 # del lines[-1]

    def test_remove_edge_in_operation_node_graph(self):
        for g in g_database:
            for node_start in [Node2, Node3]:
                for node_end in [ Node2, Node3]:
                    if node_start in g.keys():
                        new_g = operation_node.remove_edge_in_operation_node_graph(g, node_start, node_end)
                        if node_end in g[node_start]["list"]:
                            self.assertEqual( new_g, g[node_start]["list"].remove(node_end) )

    @unittest.skip("error in the initial function: set changed size during iteration, fixed in 'remove_node_in_operation_node_graph_corr'")
    def test_remove_node_in_operation_node_graph(self):
        for g in g_database:
            for node_to_remove in [ Node2, Node3]:
            	if node_to_remove in g.keys():
                    g = operation_node.remove_node_in_operation_node_graph(g, node_to_remove)
                    self.assertNotIn(node_to_remove, g.keys())
                for n in g.keys():
                    self.assertNotIn(node_to_remove, g[n]["list"])

    def test__get_operation_node_graph_paths(self):
       
        def test_get(self, g, node, l, current_path, old_paths):
            msg = "getting path for " + node.str_debug() + "current_path: [ "
            current_path.append(node)
            for n in current_path:
                msg += n.str_debug() + ", "
            msg += "]"
            with open("logger.config", "r+") as log_file:
                # print(log_file)
                lines = log_file.read().split('\n')
                # self.assertEqual(msg, lines[l])
                # del lines[l]
            if "final" in g[node]["type"]:
                copy_path = list(current_path)
                old_paths.append(copy_path)
                #print("paths_int: ", old_paths)
            else:
                for next_node in g[node]["list"]:
                    test_get(self, g, next_node, l)
            del current_path[-1]
            return old_paths

        with open("logger.config", "r") as log_file:
            lines = log_file.read().split('\n')
            l = len(lines)
            # print(l)

        for g in g_database:
            for node in [Node2, Node3]:
                old_paths = deepcopy(operation_node.paths)
                old_current_path = deepcopy(operation_node.current_path)
                operation_node._get_operation_node_graph_paths(g, node)
                old_paths = test_get(self, g, node, l, old_current_path, old_paths)
                self.assertEqual(old_current_path, operation_node.current_path)
                self.assertEqual(operation_node.paths, old_paths )
                with open("logger.config", "r") as log_file:
                    lines = log_file.read().split('\n')
                    new_l = len(lines)
                    self.assertEqual(new_l, l)

    def test_get_operation_node_graph_paths(self):
        g_database = [{Node2: {"list": {Node3, Node4}, "decision": "admission", "type": set(["normal", "final"]), "reduce": None, "not": False}, Node3: {"list": set(), "decision": "None", "type": set(["normal"]), "reduce": None, "not": True}, Node4: {"list": {Node3}, "decision": "no admission", "type": set(["normal", "final"]), "reduce": None, "not": True} } ]
        for g in g_database:
            for start_node in [Node2, Node3]:
                new_paths = operation_node.get_operation_node_graph_paths(g, start_node)
                new_current = deepcopy(operation_node.current_path)
                operation_node.paths = []
                operation_node.current_path = []
                operation_node._get_operation_node_graph_paths(g, start_node)
                self.assertEqual(new_paths, operation_node.paths)
                self.assertEqual(new_current, operation_node.current_path)

    def test__remove_duplicate_node_edges(self):
        for g in g_database:
            for node in [Node2, Node3]:
                for start_list in [ [], [Node2], [Node3], [Node2, Node3] ]:
                    old_tab = deepcopy(operation_node.nodes_traversed_for_removal)
                    old_g = deepcopy(g)
                    operation_node._remove_duplicate_node_edges(old_g, node, start_list)
                    new_tab = operation_node.nodes_traversed_for_removal
                    for Node in new_tab:
                        if Node not in old_tab:
                            if Node != node:
                                self.assertNotIn(Node, start_list)
                            for n in list(old_g[Node]["list"]):
                                if n in start_list:
                                    self.assertNotIn(n, g[Node]["list"])
                                else:
                                    self.assertIn(n, new_tab)

    def test_remove_duplicate_node_edge(self):
        g_database = [{Node2: {"list": {Node3, Node4}, "decision": "admission", "type": set(["normal", "final"]), "reduce": None, "not": False}, Node3: {"list": set(), "decision": "None", "type": set(["normal"]), "reduce": None, "not": True}, Node4: {"list": {Node3}, "decision": "no admission", "type": set(["normal", "final"]), "reduce": None, "not": True} } ]
        for g in g_database:
            for start_list in [ [], [Node2], [Node3], [Node2, Node3] ]:
                operation_node.remove_duplicate_node_edges(g, start_list)
                # need to supress the lines in the logger_file ?
                for node in start_list:
                    self.assertIn(node, operation_node.nodes_traversed_for_removal)
                # no need to do more, it's a simple function

    def test_clean_edges_in_operation_node_graph(self):
        # the goal here is to look at g modified and assure that all the nodes that should have been removed have been removed
        # however, this fucntion calls many others fucntions, so it was very difficult to test if all the nodes that should be removed were removed

        def test_clean(self, g):
            new_g = operation_node.clean_edges_in_operation_node_graph(g)

            start_nodes = []
            final_nodes = []
            for node_iter in g.keys():
                if "start" in g[node_iter]["type"]:
                    start_nodes.append(node_iter)
                if "final" in g[node_iter]["type"]:
                    final_nodes.append(node_iter)

            for node_iter in g.keys():
                for snode in g[node_iter]["list"]:
                    if snode in start_nodes:
                        self.assertNotIn(snode, new_g[node_iter]["list"])

            for snode in start_nodes:
                for node_iter in g.keys():
                    operation_node.remove_edge_in_operation_node_graph(g, node_iter, snode) # we will modify g to continue to compare it to new_g
            
            for snode in start_nodes:
                nodes_bag = [ snode ]
                while True:
                    node = nodes_bag.pop()
                    operation_node.nodes_traversed_for_removal = []
                    operation_node.remove_duplicate_node_edges(g, g[node]["list"])
                    nodes_bag.extend(g[node]["list"])
                    if not nodes_bag:
                        break

            for snode in start_nodes:
                paths = operation_node.get_operation_node_graph_paths(g, snode)

                for i in range(0, len(paths)):
                    for j in range(i+1, len(paths)):
                        if len(paths[i]) == len(paths[j]):
                            continue
                        elif len(paths[i]) < len(paths[j]):
                            p = paths[i]
                            q = paths[j]
                        else:
                            p = paths[j]
                            q = paths[i]
                        if p[len(p)-1] == q[len(q)-1]:
                            for k in range(0, len(p)):
                                if p[len(p)-1-k] == q[len(q)-1-k]:
                                    continue
                                else:
                                    if q[len(q)-k] in g[q[len(q)-1-k]]["list"]:
                                        self.assertNotIn(Node, g[q[len(q)-1-k]]["list"])
                                        g = operation_node.remove_edge_in_operation_node_graph(g, q[len(q)-1-k], q[len(q)-k])
                                        break
            self.assertEqual(g, new_g)
        
        for g in g_database2:
            test_clean(self, g)

    def test_clean_nodes_in_operation_node_graph(self):
        for g in g_database3:
            new_g = deepcopy(g)
            (g, made_change) = operation_node.clean_nodes_in_operation_node_graph(g)
            node_list = list(new_g.keys())
            for node_iter in node_list:
                if "final" not in new_g[node_iter]["type"] and not new_g[node_iter]["list"]:
                    self.assertTrue(made_change)
                    new_g = operation_node.remove_node_in_operation_node_graph(new_g, node_iter)
            self.assertEqual(new_g, g)


class ReducedVertice(unittest.TestCase):
    
    """Test the ReducedVertice object
    """
    def test_var_exists(self):
        vertice = operation_node.ReducedVertice()
        # vertice.__init__()
        self.assertIsNotNone(vertice)
        self.assertEqual(vertice.TYPE_SINGLE, "single")
        self.assertEqual(vertice.TYPE_START, "start")
        self.assertEqual(vertice.TYPE_REQUIRE_ANY, "require-any")
        self.assertEqual(vertice.TYPE_REQUIRE_ALL, "require-all")
        self.assertEqual(vertice.TYPE_REQUIRE_ENTITLEMENT, "require-entitlement")
        self.assertEqual(vertice.type, vertice.TYPE_SINGLE)
        self.assertEqual(vertice.is_not, False)
        self.assertEqual(vertice.value, None)
        self.assertEqual(vertice.decision, None)

    def test_set_value(self):
        vertice = operation_node.ReducedVertice()
        for value in [None, True, False, 42, 4.2, "hello"]:
            vertice.set_value(value)
            self.assertEqual(vertice.value, value)

    def test_set_type(self):
        vertice = operation_node.ReducedVertice()
        for type in [None, True, False, 42, 4.2, "hello", int]:
            vertice.set_type(type)
            self.assertEqual(vertice.type, type)

    def test__replace_in_list(self):
        v1 = operation_node.ReducedVertice()
        v2 = operation_node.ReducedVertice()
        v3 = operation_node.ReducedVertice()
        v3.value = [ v2 ]
        lst = [ v1, v2, v3 ]
        old = v2
        new = operation_node.ReducedVertice()
        a = v1._replace_in_list_corr(lst, old, new)
        replace_occurred = operation_node.replace_occurred
        self.assertEqual(replace_occurred, True)
        self.assertEqual(v3.value, [ new ] ) # still equal to [v2, []]
        self.assertEqual(lst, [v1, new, v3] )
        self.assertEqual(a, [v1, new, v3] )
        self.assertTrue(replace_occurred)
    
    def test_replace_in_list(self):
        for v in vertice_database:
            re_init() # re-initialize the values of v1, v2...
            old = v2
            new = operation_node.ReducedVertice()
            old_v = deepcopy(v)
            v.value = old_v.replace_in_list(old, new) # beware, with deepcopy, old_v and v are different !!!!
            if isinstance(old_v.value, list):
                self.assertEqual( v.value, old_v._replace_in_list_corr(old_v.value, old, new) )
            else:
                self.assertEqual(v.value, old_v.value)

    def test__replace_sublist_in_list(self):
        vertice = operation_node.ReducedVertice()
        for lst in lst_database: # [ [v1], [v1, v4], [ v1, v2, v5 ] ]
            #lst[0].value = v2
            for old in [ [], [v1], [v4], [ v1, v2, v3 ] ]:
                old_lst = deepcopy(lst)
                #print(old_lst[0].value==v2, lst[0].value==v2)
                #self.assertTrue(val.value==lst[0].value)
                #self.assertTrue(vertice.lst__eq__(lst, [v1]))
                #print("value", old_lst[0].value, lst[0].value)
                #print("vs", old_lst[0], lst[0])
                self.assertTrue(vertice.lst__eq__(old_lst, lst)) # I have add the function lst__eq__() in the original file
                new = operation_node.ReducedVertice()
                new.value = "new" # to recognize it
                vertice._replace_sublist_in_list(lst, old, new)
                all_found = True
                for v in old:
                    if v not in old_lst:
                        all_found = False
                        break
                if all_found:
                    self.assertEqual(len(lst), len(old_lst)-len(old)+1)
                    for v in old:
                        self.assertNotIn(v, lst) # beware, this calls __eq__ function...
                        self.assertIn(v, old_lst)
                    self.assertEqual(new, lst[-1])
                    self.assertTrue(operation_node.replace_occurred)
                else:
                    for i, v in enumerate(old_lst):
                        if isinstance(v.value, list):
                            vertice._replace_sublist_in_list(v.value, old, new)
                            self.assertEqual(v.value, lst[i].value)
                        else:
                            break
                    self.assertTrue(vertice.lst__eq__(old_lst, lst))

    def test_replace_sublist_in_list(self):
        vertice = operation_node.ReducedVertice()
        for value in lst_database:
            vertice.value = value
            #print(vertice.value[0]._eq_(v1))
            #print("0")
            for old in [ [], [v1], [v4], [v1, v2, v3] ]:
                #print("1")
                new = operation_node.ReducedVertice()
                new.value = "new"
                old_vertice = deepcopy(vertice)
                vertice.replace_sublist_in_list(old, new)
                if isinstance(old_vertice.value, list):
                    old_vertice._replace_sublist_in_list(old_vertice.value, old, new)
                    #print("ols", old_vertice.value[1].value)
                #print(vertice.value, old_vertice.value)
                self.assertTrue(vertice.__eq__(old_vertice)) # first I have said self.assertEqual(vertice, old_vertice) while creating an __eq__ function, but it would have called it when I call v1.type == v2.type for example...

    def test_set_decision(self):
        vertice = operation_node.ReducedVertice()
        for decision in [ 42, [], None, "agree", 3.7, v1 ]:
            vertice.set_decision(decision)
            self.assertEqual(vertice.decision, decision)

    def test_set_type_single(self):
        vertice = operation_node.ReducedVertice()
        vertice.set_type_single()
        self.assertEqual(vertice.type, vertice.TYPE_SINGLE)

    def test_set_type_start(self):
        vertice = operation_node.ReducedVertice()
        vertice.set_type_single()
        self.assertEqual(vertice.type, vertice.TYPE_SINGLE)

    def test_set_type_require_entitlement(self):
        vertice = operation_node.ReducedVertice()
        vertice.set_type_require_entitlement()
        self.assertEqual(vertice.type, vertice.TYPE_REQUIRE_ENTITLEMENT)

    def test_set_type_require_any(self):
        vertice = operation_node.ReducedVertice()
        vertice.set_type_require_any()
        self.assertEqual(vertice.type, vertice.TYPE_REQUIRE_ANY)

    def test_set_type_require_all(self):
        vertice = operation_node.ReducedVertice()
        vertice.set_type_require_all()
        self.assertEqual(vertice.type, vertice.TYPE_REQUIRE_ALL)
    
    def test_set_integrated_vertice(self):
        vertice = operation_node.ReducedVertice()
        for value in [ [1, 2], "he", (42, 43) ]:
            vertice.value = value
            (n, i) = vertice.value
            for integrated_vertice in [ 42, [], None, "agree", 3.7, v1 ]:
                #(n, i) = vertice.value # very strange because if we place it here, i would be integrated_vertice, like the function set_integrated_vertice have already been executed, pbl of parallelism execution ?
                #print("n= ", n, "i= ", i)
                vertice.set_integrated_vertice(integrated_vertice)
                self.assertEqual(vertice.value, (n, integrated_vertice))
    
    def test_is_type_single(self):
        vertice = operation_node.ReducedVertice()
        for typee in [ 42, [], None, "agree", 3.7, v1, "single", "start", "require-any", "require-all", "require-entitlement" ]:
            vertice.type = typee
            bo = vertice.is_type_single()
            if vertice.type==vertice.TYPE_SINGLE:
                self.assertTrue(bo)
            else:
                self.assertFalse(bo)

    def test_is_type_start(self):
        vertice = operation_node.ReducedVertice()
        for typee in [ 42, [], None, "agree", 3.7, v1, "single", "start", "require-any", "require-all", "require-entitlement" ]:
            vertice.type = typee
            bo = vertice.is_type_start()
            if vertice.type==vertice.TYPE_START:
                self.assertTrue(bo)
            else:
                self.assertFalse(bo)
    
    def test_is_type_require_entitlement(self):
        vertice = operation_node.ReducedVertice()
        for typee in [ 42, [], None, "agree", 3.7, v1, "single", "start", "require-any", "require-all", "require-entitlement" ]:
            vertice.type = typee
            bo = vertice.is_type_require_entitlement()
            if vertice.type==vertice.TYPE_REQUIRE_ENTITLEMENT:
                self.assertTrue(bo)
            else:
                self.assertFalse(bo)

    def test_is_type_require_all(self):
        vertice = operation_node.ReducedVertice()
        for typee in [ 42, [], None, "agree", 3.7, v1, "single", "start", "require-any", "require-all", "require-entitlement" ]:
            vertice.type = typee
            bo = vertice.is_type_require_all()
            if vertice.type==vertice.TYPE_REQUIRE_ALL:
                self.assertTrue(bo)
            else:
                self.assertFalse(bo)

    def test_is_type_require_any(self):
        vertice = operation_node.ReducedVertice()
        for typee in [ 42, [], None, "agree", 3.7, v1, "single", "start", "require-any", "require-all", "require-entitlement" ]:
            vertice.type = typee
            bo = vertice.is_type_require_any()
            if vertice.type==vertice.TYPE_REQUIRE_ANY:
                self.assertTrue(bo)
            else:
                self.assertFalse(bo)
    
    def test_recursive_str(self):
        def test(self, vertice, level, recursive_is_not):
            res = vertice.recursive_str(level, recursive_is_not)
            if vertice.is_type_single():
                if vertice.is_not and not recursive_is_not:
                    if "(require-any" in str(vertice.value):
                        self.assertEqual(res, vertice.value.str_not())
                    else:
                        self.assertEqual(res, "(require-not " + str(vertice.value) + ")")
                else:
                    self.assertEqual(res, str(vertice.value))
            elif vertice.is_type_require_entitlement():
                (n,i) = vertice.value
                if i is None:
                    if vertice.is_not:
                        self.assertEqual(res, "(require-not " + str(n.value) + ")")
                    else:
                        self.assertEqual(res, str(n.value))
                else:
                    if vertice.is_not:
                        self.assertEqual(res, "(require-not " + str(n.value)[:-1] + " " + i.recursive_str(level, vertice.is_not) + ")" + ")")
                    else:
                        self.assertEqual(res, str(n.value)[:-1] + " " + i.recursive_str(level, vertice.is_not) + ")" )
            else:
                i = 0 # index of position in res
                if level == 1:
                    self.assertEqual( res[:14], "\n" + 13*' ')
                    i += 14
                self.assertEqual(res[i:(i+1+len(vertice.type))], "(" + vertice.type )
                i += (1+len(vertice.type))
                level += 1
                for j, v in enumerate(vertice.value):
                    if j == 0:
                        self.assertEqual( res[i:i+1+len(v.recursive_str(level, recursive_is_not))], " " + v.recursive_str(level, recursive_is_not) )
                        i += 1+len(v.recursive_str(level, recursive_is_not))
                    else:
                        self.assertEqual(res[i:i+1+13*level+len(v.recursive_str(level, recursive_is_not))], "\n" + 13*level*' ' + v.recursive_str(level, recursive_is_not) )
                        i += 1+13*level + len(v.recursive_str(level, recursive_is_not))
                self.assertEqual(res[-1], ")")
                self.assertEqual(i+1, len(res))

        for vertice in vertice_database:
            re_init()
            nodee = operation_node.OperationNode(42)
            nodee.type = "(require-any"
            nodee.OPERATION_NODE_TYPE_TERMINAL = "(require-any"
            nodee.terminal = "(require-any"
            for value in [ "hello" , 42, None, [1, 2], nodee ]:
                vertice.value = value
                vertice.set_type_single() # all conditions here in the part 'if self.is_type_single()'
                for is_not in [ False, True, None, 1, [1], "hello" ]:
                    vertice.is_not = is_not
                    test(self, vertice, 0, False) # no need to play on the value of 'recursive_is_not', we can just play on 'is_not', and level is not used in this part
            ver1 = operation_node.ReducedVertice()
            ver1.value = "ver1"
            ver2 = operation_node.ReducedVertice()
            ver2.value = "ver2"
            for value in [ [ver2, ver1], (ver2, ver1), (ver2, None) ]: # here (n,i)=vertice.value with n an instance of RV (ReducedVertice) and i same if not None
                vertice.value = value
                vertice.set_type_require_entitlement()
                for is_not in [ False, True, None, 1, [1], "hello" ]:
                    vertice.is_not = is_not
                    test(self, vertice, 0, False) # same comments than before
            for value in [ [ver2, ver1] ] + [  [v1], [v1, v4], [ v1, v2, v5 ] ]: # here we will test the condition 'else' of the function, we need lists of RV
                v2.set_type_single()
                vertice.value = value
                v1.value = [v2] # change of the value to avoid vertice=vertice.value, vertice stays as it was 
                v2.value = [v4]
                vertice.type="42" # for be in 'else' + must be a string
                v4.set_type_single() # to stop the loop
                for level in [ -1, 0, 1, 2 ] :
                    test(self, vertice, level, False) # same comments than before

    def test_recursive_str_debug(self):
        def test(self, vertice, level, recursive_is_not):
            res = vertice.recursive_str_debug(level, recursive_is_not)
            if vertice.is_type_single():
                if vertice.is_not and not recursive_is_not:
                    self.assertEqual(res, "(require-not " + vertice.value.str_debug() + ")") # str_debug() is defined in the classes RV (ReducedVertice), RE (ReducedEdge), NTN (NonTerminalNode) and OP (OperationNode)
                else:
                    self.assertEqual(res, vertice.value.str_debug())
            elif vertice.is_type_require_entitlement():
                (n, i) = vertice.value
                if i is None:
                    if vertice.is_not:
                        self.assertEqual(res, "(require-not " + n.value.str_debug() + ")")
                    else:
                        self.assertEqual(res, n.value.str_debug())
                else:
                    if vertice.is_not:
                        self.assertEqual(res, "(require-not " + n.value.str_debug()[:-1] + " " + i.recursive_str_debug(level, vertice.is_not) + ")" + ")")
                    else:
                        self.assertEqual(res, n.value.str_debug()[:-1] + " " + i.recursive_str_debug(level, vertice.is_not) + ")")
            else:
                i = 0 # index of position in res
                if level == 1:
                    self.assertEqual( res[:14], "\n" + 13*' ')
                    i += 14
                self.assertEqual(res[i:(i+1+len(vertice.type))], "(" + vertice.type )
                i += (1+len(vertice.type))
                level += 1
                for j, v in enumerate(vertice.value):
                    if j == 0:
                        self.assertEqual( res[i:i+1+len(v.recursive_str_debug(level, recursive_is_not))], " " + v.recursive_str_debug(level, recursive_is_not) )
                        i += 1+len(v.recursive_str_debug(level, recursive_is_not))
                    else:
                        self.assertEqual(res[i:i+1+13*level+len(v.recursive_str_debug(level, recursive_is_not))], "\n" + 13*level*' ' + v.recursive_str_debug(level, recursive_is_not) )
                        i += 1+13*level + len(v.recursive_str_debug(level, recursive_is_not))
                self.assertEqual(res[-1], ")")
                self.assertEqual(i+1, len(res))

        for vertice in vertice_database:
            re_init()
            nodee1 = operation_node.OperationNode(42)
            nodee2  = operation_node.NonTerminalNode()
            nodee2.filter_id = 42
            nodee2.argument_id = 43
            nodee2.match_offset = 44
            nodee2.unmatch_offset = 45
            for value in [ nodee1, nodee2 ]: # value must have a str_debug function
                vertice.value = value
                vertice.set_type_single() # all conditions here in the part 'if self.is_type_single()'
                for is_not in [ False, True, None, 1, [1], "hello" ]:
                    vertice.is_not = is_not
                    test(self, vertice, 0, False) # no need to play on the value of 'recursive_is_not', we can just play on 'is_not', and level is not used in this part
            ver1 = operation_node.ReducedVertice()
            ver1.value = nodee1
            ver2 = operation_node.ReducedVertice()
            ver2.value = nodee2
            for value in [ [ver2, ver1], (ver2, ver1), (ver2, None) ]: # here (n,i)=vertice.value with n an instance of RV (ReducedVertice) and i same if not None
                vertice.value = value
                vertice.set_type_require_entitlement()
                for is_not in [ False, True, None, 1, [1], "hello" ]:
                    vertice.is_not = is_not
                    test(self, vertice, 0, False) # same comments than before
            for value in [ [ver2, ver1] ] + [  [v11], [v11, v14], [ v11, v12 ] ]: # here we will test the condition 'else' of the function, we need lists of RV
                ver2.set_type_single()
                v11.set_type_single()
                v15.value = nodee1
                v14.set_type_single()
                v15.set_type_single()
                vertice.value = value
                vertice.type="42" # for be in 'else' + must be a string
                v12.type = "43"
                ver1.is_not = False # to stop
                ver2.is_not = False # to stop
                for level in [ -1, 0, 1, 2 ] :
                    test(self, vertice, level, False) # same comments than before

    def test_recursive_xml_str(self):
        def test(self, vertice, level, recursive_is_not):
            res = vertice.recursive_xml_str(level, recursive_is_not)
            if vertice.is_type_single():
                if vertice.is_not and not recursive_is_not:
                    (name, argument) = vertice.value.values()
                    if argument == None:
                        self.assertEqual(res, level*"\t" + "<require type=\"require-not\">\n" + (level+1)*"\t" + "<filter name=\"" + str(name) + "\" />\n" + level*"\t" + "</require>\n")
                    else:
                        arg = str(argument).replace('&', '&amp;').replace('"', '&quot;').replace('\'', '&apos;').replace('<', '&lt;').replace('>', '&gt;')
                        self.assertEqual(res, level*"\t" + "<require type=\"require-not\">\n" + (level+1)*"\t" + "<filter name=\"" + str(name) + "\" argument=\"" + arg + "\" />\n" + level*"\t" + "</require>\n")
                else:
                    (name, argument) = vertice.value.values()
                    if argument == None:
                        self.assertEqual(res, level*"\t" + "<filter name=\"" + str(name) + "\" />\n" )
                    else:
                        arg = str(argument).replace('&', '&amp;').replace('"', '&quot;').replace('\'', '&apos;').replace('<', '&lt;').replace('>', '&gt;')
                        self.assertEqual(res, level*"\t" + "<filter name=\"" + str(name) + "\" argument=\"" + arg + "\" />\n")
            elif vertice.is_type_require_entitlement():
                (n, i) = vertice.value
                if vertice.is_not:
                    if i == None:
                        level +=1
                        _tmp = str(n.value)[21:-1].replace('&', '&amp;').replace('"', '&quot;').replace('\'', '&apos;').replace('<', '&lt;').replace('>', '&gt;')
                        self.assertEqual(res, (level-1)*"\t" + "<require type=\"require-not\">\n" + level*"\t" + "<require type=\"require-entitlement\"" + " value=\"" + _tmp + "\" />\n" + (level-1)*"\t" + "</require>\n" )
                    else:
                        level +=1
                        _tmp = str(n.value)[21:-1].replace('&', '&amp;').replace('"', '&quot;').replace('\'', '&apos;').replace('<', '&lt;').replace('>', '&gt;')
                        self.assertEqual(res, (level-1)*"\t" + "<require type=\"require-not\">\n" + level*"\t" + "<require type=\"require-entitlement\"" + " value=\"" + _tmp + "\">\n" + i.recursive_xml_str(level+1, vertice.is_not) + level*"\t" + "</require>\n" + (level-1)*"\t" + "</require>\n" )
                else:
                    if i == None:
                        _tmp = str(n.value)[21:-1].replace('&', '&amp;').replace('"', '&quot;').replace('\'', '&apos;').replace('<', '&lt;').replace('>', '&gt;')
                        self.assertEqual(res, " value=\"" + _tmp + "\" />\n" )
                    else:
                        _tmp = str(n.value)[21:-1].replace('&', '&amp;').replace('"', '&quot;').replace('\'', '&apos;').replace('<', '&lt;').replace('>', '&gt;')
                        self.assertEqual(res, " value=\"" + _tmp + "\">\n" + i.recursive_xml_str(level+1, vertice.is_not) + level*"\t" + "</require>\n" )
            else:
                index = 0 # index in the word 'res'
                n = len(level*"\t" + "<require type=\"" + vertice.type + "\">\n")
                self.assertEqual(res[:n], level*"\t" + "<require type=\"" + vertice.type + "\">\n")
                index += n
                for i, v in enumerate(vertice.value):
                    a = v.recursive_xml_str(level+1, recursive_is_not)
                    n = len(a)
                    self.assertEqual(res[index:(index+n)], a)
                    index += n
                n = len(level*"\t" + "</require>\n")
                self.assertEqual(res[index:index+n], level*"\t" + "</require>\n")
                self.assertEqual(index+n, len(res))


        
        vertice = operation_node.ReducedVertice()
        vertice.is_not = "ok"
        ntn = operation_node.NonTerminalNode()
        vertice.value = ntn # the function values() is defined for NTN and ON
        vertice.set_type_single()
        ntn.filter_id = 42
        ntn.argument_id = 43
        test(self, vertice, 2, False) # go to 'if' then 'else' of the part 'type_single' of recursive_xml_str
        test(self, vertice, 7, True) # go to 'else' then 'else' of the part 'type_single' of recursive_xml_str
        op = operation_node.OperationNode(42)
        op.type = 1 # so is_terminal, so values() will return (None, None)
        vertice.value = op
        test(self, vertice, -1, False) # go to 'if' then 'if' of the part 'type_single' of recursive_xml_str
        test(self, vertice, -3, True) # go to 'else' then 'if' of the part 'type_single' of recursive_xml_str
        
        vertice.set_type_require_entitlement()
        for value in [ (v11, None), [v12, v13] ]:
            v13.set_type_single()
            v13.value = ntn
            v11.value = "v11, &amp, &quot, &apos, &lt, &gt"
            v12.value = "v12, &amp\n &quot\t &apos\', &lt, &gt"
            vertice.value = value
            test(self, vertice, 5, None)

        vertice.type = "ver" # to go to the 'else' condition
        for value in [ [], [v11] , [v12, v13, v14] ]:
            vertice.value = value
            v11.value = op
            v12.value = ntn
            v12.set_type_single()
            v14.set_type_require_entitlement()
            v14.value = (v11, v13)
            test(self, vertice, 2, False)

    def test__str__(self):
        vertice = operation_node.ReducedVertice()
        vertice.value = "he"
        res = vertice.__str__()
        self.assertEqual(res, vertice.recursive_str(1, False))

    def test_str_debug(self):
        vertice = operation_node.ReducedVertice()
        ntn = operation_node.NonTerminalNode()
        ntn.filter_id = 42
        ntn.argument_id = 43
        ntn.match_offset = 44
        ntn.unmatch_offset = 45
        vertice.value = ntn
        res = vertice.str_debug()
        self.assertEqual(res, vertice.recursive_str_debug(1, False))

    def test_str_simple(self):
        vertice = operation_node.ReducedVertice()
        ntn = operation_node.NonTerminalNode()
        ntn.filter_id = 42
        ntn.argument_id = 43
        ntn.match_offset = 44
        ntn.unmatch_offset = 45
        vertice.value = ntn
        res = vertice.str_simple()
        self.assertEqual(res, vertice.value.str_debug())
        vertice.set_type_require_any()
        self.assertEqual(vertice.str_simple(), "require-any")
        vertice.set_type_require_all()
        self.assertEqual(vertice.str_simple(), "require-all")
        vertice.set_type_require_entitlement()
        self.assertEqual(vertice.str_simple(), vertice.value.str_debug()[1:-1])
        vertice.set_type_start()
        self.assertEqual(vertice.str_simple(), "start")
        vertice.type = 42 # for 'else'
        self.assertEqual(vertice.str_simple(), "unknown-type")

    def test_str_print_debug(self):
        vertice = operation_node.ReducedVertice()
        ntn = operation_node.NonTerminalNode()
        ntn.filter_id = 42
        ntn.argument_id = 43
        ntn.match_offset = 44
        ntn.unmatch_offset = 45
        vertice.value = ntn
        res = vertice.str_print_debug()
        self.assertEqual(res, (vertice.value.str_debug(), None))
        vertice.set_type_require_any()
        self.assertEqual(vertice.str_print_debug(), ("(require-any", ")"))
        vertice.set_type_require_all()
        self.assertEqual(vertice.str_print_debug(), ("(require-all", ")"))
        vertice.set_type_require_entitlement()
        self.assertEqual(vertice.str_print_debug(), (vertice.value.str_debug()[:-1], ")"))
        vertice.set_type_start()
        self.assertEqual(vertice.str_print_debug(), (None, None))
        vertice.type = 42 # for 'else'
        self.assertEqual(vertice.str_print_debug(), ("unknown-type", None))

    def test_str_print(self):
        vertice = operation_node.ReducedVertice()
        ntn = operation_node.NonTerminalNode()
        ntn.filter_id = 42
        ntn.argument_id = 43
        ntn.match_offset = 44
        ntn.unmatch_offset = 45
        vertice.value = ntn
        res = vertice.str_print()
        self.assertEqual(res, (str(vertice.value), None))
        vertice.set_type_require_any()
        self.assertEqual(vertice.str_print(), ("(require-any", ")"))
        vertice.set_type_require_all()
        self.assertEqual(vertice.str_print(), ("(require-all", ")"))
        vertice.set_type_require_entitlement()
        self.assertEqual(vertice.str_print(), (str(vertice.value)[:-1], ")"))
        vertice.set_type_start()
        self.assertEqual(vertice.str_print(), (None, None))
        vertice.type = 42 # for 'else'
        self.assertEqual(vertice.str_print(), ("unknown-type", None))

    def test_str_print_not(self):
        vertice = operation_node.ReducedVertice()
        def test(self, vertice):
            res = vertice.str_print_not()
            if res == "" :
                self.assertFalse(vertice.is_type_single() and vertice.is_not)
            else:
                self.assertTrue(vertice.is_type_single() and vertice.is_not)
                if res == vertice.value.str_not():
                    self.assertIn("(require-any", str(vertice.value))
                else:
                    self.assertNotIn("(require-any", str(vertice.value))
                    self.assertEqual(res, "(require-not " + str(vertice.value) + ")")
        
        op = operation_node.OperationNode(42)
        op.type = 1
        op.terminal = "(require-any"
        vertice.value = op
        for typee in [ vertice.TYPE_SINGLE, "(require-any" ]:
            vertice.type = typee
            for is_not in [ "hello", 42, True, False, None]:
                vertice.is_not = is_not
                test(self, vertice)

    def test_xml_str(self):
        vertice = operation_node.ReducedVertice()
        vertice.is_not = "ok"
        ntn = operation_node.NonTerminalNode()
        vertice.value = ntn
        ntn.filter_id = 42
        ntn.argument_id = 43
        self.assertEqual(vertice.xml_str(), vertice.recursive_xml_str(3, False))




class ReducedEdge(unittest.TestCase):
    
    """Test the ReducedEdge object
    """
    def test__init__(self):
        edge = operation_node.ReducedEdge()
        self.assertEqual(edge.start, None)
        self.assertEqual(edge.end, None)
        edge = operation_node.ReducedEdge("start", "end")
        self.assertEqual(edge.start, "start")
        self.assertEqual(edge.end, "end")

    def test_str_debug(self):
        edge = operation_node.ReducedEdge()
        vertice = operation_node.ReducedVertice()
        ntn = operation_node.NonTerminalNode()
        ntn.filter_id = 42
        ntn.argument_id = 43
        ntn.match_offset = 44
        ntn.unmatch_offset = 45
        vertice.value = ntn
        edge.start = vertice # I choose ReducedVertice objects but str_debug is also defined fot other classes
        edge.end = vertice

        res = edge.str_debug()
        self.assertEqual(res, edge.start.str_debug() + " -> " + edge.end.str_debug() )

    def test_str_simple(self):
        edge = operation_node.ReducedEdge()
        vertice = operation_node.ReducedVertice()
        ntn = operation_node.NonTerminalNode()
        ntn.filter_id = 42
        ntn.argument_id = 43
        ntn.match_offset = 44
        ntn.unmatch_offset = 45
        vertice.value = ntn
        edge.start = vertice # I choose ReducedVertice objects but str_simple is also defined fot other classes
        edge.end = vertice

        res = edge.str_simple()
        self.assertEqual(res, "%s -----> %s" % (edge.start.str_simple(), edge.end.str_simple()) )

    def test__str__(self):
        edge = operation_node.ReducedEdge("end", "start")
        self.assertEqual(str(edge), str(edge.start) + " -> " + str(edge.end))


class ReducedGraph(unittest.TestCase):
    """ Test the ReducedGraph object"""
    def test__init__(self):
        graph = operation_node.ReducedGraph()
        self.assertEqual(graph.vertices, [])
        self.assertEqual(graph.edges, [])
        self.assertEqual(graph.final_vertices, [])
        self.assertEqual(graph.reduce_changes_occurred, False)

    def test_add_vertice(self):
        graph = operation_node.ReducedGraph()
        vertice = operation_node.ReducedVertice()
        v11 = operation_node.ReducedVertice() # if we use v11 of the past, it raises an error I don't understand...
        v12 = operation_node.ReducedVertice()
        v13 = operation_node.ReducedVertice()
        for vertices in [ [], [v11, v12, v13] ]:
            graph.vertices = vertices
            ver = deepcopy(vertices)
            v = operation_node.ReducedVertice()
            v.value = "v"
            graph.add_vertice(v)
            self.assertTrue(vertice.lst__eq__(graph.vertices, ver + [v]) )

    def test_add_edge(self):
        graph = operation_node.ReducedGraph()
        edge = operation_node.ReducedEdge()
        for edges in [ [], [e1, e2] ]:
            graph.edges = edges
            e = deepcopy(edges)
            v = operation_node.ReducedEdge()
            v.start = "re"
            graph.add_edge(v) # /!\ this add v to edges also !!
            self.assertTrue(edge.lst_eq_(graph.edges, e + [v]) )

    def test_add_edge_by_vertices(self):
        graph = operation_node.ReducedGraph()
        edge = operation_node.ReducedEdge()
        edge1 = [e1, e2]
        graph.edges = edge1
        ed1 = deepcopy(edge1)
        v_start = "start"
        v_end = "end"
        graph.add_edge_by_vertices(v_start, v_end)
        self.assertTrue(edge.lst_eq_(graph.edges[:-1], ed1 ) )
        edge2 = graph.edges[-1]
        e = operation_node.ReducedEdge(v_start, v_end)
        self.assertTrue(edge2==e)

    def test_set_final_vertices(self):
        def test(self, graph):
            graph.set_final_vertices()
            for v in graph.final_vertices:
                for e in graph.edges:
                    self.assertFalse(e.start==v)
            for v in graph.vertices:
                bo = True
                for e in graph.edges:
                    if e.start==v:
                        self.assertNotIn(v, graph.final_vertices)
                        bo = False
                        break
                if bo:
                    self.assertIn(v, graph.final_vertices)

        for graph in graph_database:
            test(self, graph)

    def test_contains_vertice(self):
        for graph in graph_database:
            for v in [v21, v22, v23]:
                res = graph.contains_vertice(v)
                if v in graph.vertices:
                    self.assertTrue(res)
                else:
                    self.assertFalse(res)

    def test_contains_edge(self):
        for graph in graph_database:
            for e in edge_database:
                res = graph.contains_edge(e)
                if e in graph.edges:
                    self.assertTrue(res)
                else:
                    self.assertFalse(res)

    def test_contains_edge_by_vertices(self):
        for graph in graph_database:
            for (v_start, v_end) in data_edge_database:
                res = graph.contains_edge_by_vertices(v_start, v_end)
                bo = False
                for e in graph.edges:
                    if e.start == v_start and e.end == v_end:
                        bo = True
                        self.assertTrue(res)
                        break
                if not bo:
                    self.assertFalse(res)

    def test_get_vertice_by_value(self):
        for graph in graph_database:
            for value in value_database:
                bo = False
                res = graph.get_vertice_by_value(value)
                for v in graph.vertices:
                    if v.is_type_single() and v.value==value:
                        self.assertEqual(res, v)
                        bo = True
                        break
                if not bo:
                    self.assertIsNone(res)

    def test_get_edge_by_vertices(self):
        for graph in graph_database:
            for (v_start, v_end) in data_edge_database:
                bo = False
                res = graph.get_edge_by_vertices(v_start, v_end)
                for e in graph.edges:
                    if e.start==v_start and e.end==v_end:
                        self.assertEqual(res, e)
                        bo = True
                        break
                if not bo:
                    self.assertIsNone(res)

    def test_remove_vertice(self):
        for graph in graph_database:
            for v in [v21, v22, v23]:
                old_edges = deepcopy(graph.edges)
                old_vertices = deepcopy(graph.vertices)
                graph.remove_vertice(v)
                for e in old_edges:
                    if e in graph.edges:
                        self.assertFalse(e.start==v or e.end==v)
                    else:
                        self.assertTrue(e.start==v or e.end==v)
                for ver in old_vertices:
                    if ver==v:
                        self.assertNotIn(ver, graph.vertices)
                    else:
                        self.assertIn(ver, graph.vertices)

    def test_remove_vertice_update_decision(self):
        re_init_graph()
        for graph in graph_database:
            for v in [v21, v22, v23]:
                re_init_graph()
                old_edges = deepcopy(graph.edges)
                old_vertices = deepcopy(graph.vertices)
                graph.remove_vertice_update_decision(v)
                for e in old_edges:
                    if e in graph.edges:
                        self.assertFalse(e.start==v or e.end==v)
                    else:
                        if e.end==v:
                            # self.assertEqual(e.start.decision, v.decision) # not true, because e.start is not changed because it is a deepcopy, I don't know how to verify that the object 'decision' have been changed...
                        else:
                            self.assertEqual(e.start, v)
                l = 0 # number of vertices that should be in graph.vertices
                for ver in old_vertices:
                    if ver==v:
                        self.assertNotIn(ver, graph.vertices)
                    else:
                        l += 1 
                        # self.assertIn(ver, graph.vertices) # not equal anymore because their decision could have been changed...
                self.assertEqual(l, len(graph.vertices))

    def test_remove_edge(self):
        for graph in graph_database:
            for edge in edge_database:
                re_init_graph()
                old_edges = deepcopy(graph.edges)
                graph.remove_edge(edge)
                for e in old_edges:
                    if e==edge:
                        self.assertNotIn(e, graph.edges)
                    else:
                        self.assertIn(e, graph.edges)

    def test_remove_edge_by_vertices(self):
        for graph in graph_database:
            for (v_start, v_end) in data_edge_database:
                re_init_graph()
                graph.remove_edge_by_vertices(v_start, v_end)
                for e in graph.edges:
                    self.assertFalse(e.start==v_start and e.end==v_end)

    def test_replace_vertice_in_edge_start(self):
        for graph in graph_database:
            for (old, new) in [(None, v21), ("start", v22), (v21, v22)]:
                re_init_graph()
                v24.value = [v21, v22]
                old_replace_occurred = deepcopy(operation_node.replace_occurred)
                old_graph = deepcopy(graph)
                graph.replace_vertice_in_edge_start( old, new)
                for i,e in enumerate (old_graph.edges):
                    if e.start==old:
                        self.assertEqual(graph.edges[i].start, new)
                        self.assertTrue(operation_node.replace_occurred)
                    else:
                        if isinstance(e.start.value, list):
                            for j, ee in enumerate(e.start.value):
                                if ee==old:
                                    self.assertEqual(graph.edges[i].start.value[j], new)
                            if operation_node.replace_occurred:
                                self.assertEqual(graph.edges[i].start.decision, new.decision)
    def test_replace_vertice_in_edge_end(self):
        for graph in graph_database:
            for (old, new) in [(None, v21), ("end", v22), (v21, v22)]:
                re_init_graph()
                v23.value = [v21, v22]
                old_replace_occurred = deepcopy(operation_node.replace_occurred)
                old_graph = deepcopy(graph)
                graph.replace_vertice_in_edge_end( old, new)
                for i,e in enumerate (old_graph.edges):
                    if e.end==old:
                        self.assertEqual(graph.edges[i].end, new)
                        self.assertTrue(operation_node.replace_occurred)
                    else:
                        if isinstance(e.end.value, list):
                            for j, ee in enumerate(e.end.value):
                                if ee==old:
                                    self.assertEqual(graph.edges[i].end.value[j], new)
                            if operation_node.replace_occurred:
                                self.assertEqual(graph.edges[i].end.decision, new.decision)



if __name__ == '__main__':
    unittest.main()