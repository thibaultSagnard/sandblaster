# coding=utf-8
"""This is the "sandbox_regex.py" test file
"""

import unittest
from reverse_sandbox import sandbox_regex
import math
import random
from copy import deepcopy


# the functions below are here to not be tested by the main()
# function used for test_fill_from_regex_list
def test_fill(self, graph, regex_list):
        old_graph = deepcopy(graph)
        b = False
        for idx, item in enumerate(regex_list):
            if 'start_node' in item and item['start_node'] == True and graph.start_node != None:
                b=True
                with self.assertRaises(Exception):
                    graph.fill_from_regex_list(regex_list)
                raise unittest.SkipTest('end because an exceptionError would be raised')
        if not b:
            graph.fill_from_regex_list(regex_list)
            node_list = graph.node_list
            """for node in node_list:
            self.assertIn(node, regex_list)
            """ # I don't knwow why these lignes don't work...
            for idx, item in enumerate(regex_list):
                self.assertEqual(node_list[idx].name, str(idx))
                self.assertEqual(len(node_list), len(regex_list))
                node = node_list[idx]
                self.assertIsNotNone(node)
                if node.type == node.TYPE_JUMP_BACKWARD: # the nodes were news because just created
                    self.assertEqual(item["type"], "jump_backward")
                elif node.type == node.TYPE_JUMP_FORWARD:
                    self.assertEqual(item["type"], "jump_forward")
                elif node.type == node.TYPE_END:
                    self.assertEqual(item["type"], "end")
                else:
                    self.assertEqual(node.type, node.TYPE_CHARACTER)
                    self.assertEqual(node.value, item["value"])
                if graph.start_node == node:
                    self.assertIn('start_node', item)
                    self.assertTrue(item['start_node'])
                if 'start_node' in item and item['start_node'] == True and graph.start_node!=None:
                    self.assertEqual(graph.start_node, old_graph.start_node)
                    self.assertRaises(Exception)

            self.assertEqual(len(node_list), len(regex_list))

            graph_dict = graph.graph_dict
            for idx, node in enumerate(node_list):
                if node.is_type_end():
                    self.assertEqual(graph_dict[node], [])
                elif node.is_type_character():
                    if graph_dict[node] != []:
                        self;assertEqual(len(graph_dict[node]), 1)
                        self.assertEqual(graph_dict[node][0], graph.get_node_for_idx(graph.get_next_idx_for_regex_item(regex_list, regex_list[idx])))
                elif node.is_type_jump_backward():
                    if graph_dict[node] != []:
                        self.assertEqual(len(graph_dict[node]), 1)
                        self.assertEqual(graph_dict[node][0], graph.get_node_for_idx(graph.get_re_index_for_pos(regex_list, regex_list[idx]["value"])) )
                elif node.test_is_type_jump_forward():
                    #self;assertGreater(len(graph_dict), idx+1)
                    next_idx1 = graph.get_next_idx_for_regex_item(regex_list, regex_list[idx])
                    next_idx2 = graph.get_re_index_for_pos(regex_list, regex_list[idx]["value"])
                    next1 = graph.get_node_for_idx(next_idx1)
                    next2 = graph.get_node_for_idx(next_idx2)
                    if next1:
                        self.assertIsIn(next1, graph_dict) # not possible to knwow the location
                    if next2:
                        self.assertIsIn(next2, graph_dict)

# function used in test_find_node_type_jump
def test_find(self, graph, current_node, node, backup_dict):
    bo = graph.find_node_type_jump(current_node, node, backup_dict)
    def find_nodee(graph, backup_dict, current_node, node):
        for next_node in backup_dict[current_node]:
            if graph.find_node_type_jump(next_node, node, backup_dict):
                return True
        return False
    a = find_nodee(graph, backup_dict, current_node, node)
    if not current_node.is_type_jump():
        self.assertFalse(bo)
    elif current_node == node:
        self.assertTrue(bo)
    elif not graph.graph_dict[current_node]:
        self.assertFalse(bo)
    elif a:
        self.assertTrue(bo)
    else:
        self.assertFalse(bo)

# functioon used in test_need_use_plus
def test_need(self, graph, initial_string, string_to_add):
        bo = graph.need_use_plus(initial_string, string_to_add)
        if not string_to_add.endswith("*"):
            self.assertFalse(bo)
        elif string_to_add.startswith("(") and string_to_add[-2:-1] == ")":
            if initial_string.endswith(string_to_add[1:-2]) == True:
                self.assertTrue(bo)
            if initial_string.endswith(string_to_add) == True:
                self.assertTrue(bo)
        else:
            if initial_string.endswith(string_to_add[:-1]) == True:
                self.assertTrue(bo)
            if initial_string.endswith(string_to_add) == True:
                self.assertTrue(bo)
            else:
                self.assertFalse(bo)




class Initialize(unittest.TestCase):
    """Test the Node object initialization
    """
    def test_object_exists(self):
        """Tests that the Node object can be created
        """
        node = sandbox_regex.Node(None, None, '')  # name and type could be anything ??
        node1 = sandbox_regex.Node("example", int, 42) # à tester !
        # pas besoin de __init__ !?
        self.assertIsNotNone(node)
        self.assertEqual(node.name, None)
        self.assertEqual(node.type, None)
        self.assertEqual(node.value, '')

    # __init__ works also without any arguments because None by default ?

    def test_set_name(self):
        node = sandbox_regex.Node()
        node.set_name("example")  #we take a random string
        self.assertEqual(node.name, "example")

    def test_set_type_jump_forward(self):
        node = sandbox_regex.Node()
        node.set_type_jump_forward()
        self.assertEqual(node.type, node.TYPE_JUMP_FORWARD)

    def test_set_type_jump_backward(self):
        node = sandbox_regex.Node()
        node.set_type_jump_backward()
        self.assertEqual(node.type, node.TYPE_JUMP_BACKWARD)

    def test_set_type_character(self):
        node = sandbox_regex.Node()
        node.set_type_character()
        self.assertEqual(node.type, node.TYPE_CHARACTER)

    def test_set_type_end(self):
        node = sandbox_regex.Node()
        node.set_type_end()
        self.assertEqual(node.type, node.TYPE_END)

    def test_is_type_end(self):
        node = sandbox_regex.Node()
        bo = node.is_type_end()
        if (node.type==node.TYPE_END):
            self.assertEqual(bo, True)
        else:
            self.assertEqual(bo, False)

    def test_is_type_jump(self):
    	node = sandbox_regex.Node()
        bo = node.is_type_jump()
        if (node.type==node.TYPE_JUMP_BACKWARD or node.type == node.TYPE_JUMP_FORWARD):
            self.assertEqual(bo, True)
        else:
            self.assertEqual(bo, False)

    def test_is_type_jump_backward(self):
    	node = sandbox_regex.Node()
    	bo = node.is_type_jump_backward()
        if (node.type == node.TYPE_JUMP_BACKWARD):
		    self.assertEqual(bo, True)
        else:
            self.assertEqual(bo, False)

    def test_is_type_jump_forward(self):
    	node = sandbox_regex.Node()
        bo = node.is_type_jump_backward()
        if (node.type == node.TYPE_JUMP_FORWARD):
            self.assertEqual(bo, True)
        else:
            self.assertEqual(bo, False)

    def test_is_type_character(self):
        node = sandbox_regex.Node()
        bo = node.is_type_jump_backward()
        if (node.type == node.TYPE_CHARACTER):
            self.assertEqual(bo, True)
        else:
            self.assertEqual(bo, False)

    def test_set_value(self):
        node = sandbox_regex.Node()
        node.set_value(42) # a random value
        self.assertEqual(node.value, 42)

    def test_set_flag_white(self):
        node = sandbox_regex.Node()
        node.set_flag_white()
        self.assertEqual(node.flag, node.FLAG_WHITE)

    def test_set_flag_grey(self):
        node = sandbox_regex.Node()
        node.set_flag_grey()
        self.assertEqual(node.flag, node.FLAG_GREY)

    def test_set_flag_black(self):
        node = sandbox_regex.Node()
        node.set_flag_black()
        self.assertEqual(node.flag, node.FLAG_BLACK)

    def test__str__(self):
        node = sandbox_regex.Node()
        a = node.__str__()
        if a == "(%s: jump backward)" % (node.name):
            self.assertEqual(node.type == node.TYPE_JUMP_BACKWARD)
        elif a == "(%s: jump forward)" % (node.name):
            self.assertEqual(node.type == node.TYPE_JUMP_FORWARD)
        elif a == "(%s: end)" % (node.name):
            self.assertEqual(node.type == node.TYPE_END)
        else:
            self.assertEqual(a, "(%s: %s)" % (node.name, node.value) )

class Methods(unittest.TestCase):

    def test__init__(self):
        graph = sandbox_regex.Graph()
        self.assertIsNotNone(graph)
        graph.__init__()
        self.assertEqual(graph.graph_dict, {})

    def test_add_node(self): #add_node ajoute un composant node: next_list
        graph = sandbox_regex.Graph()
        graph.add_node("example", None) # mandatory None ? need to add 'None' ?
        self.assertEqual(graph.graph_dict["example"], None)

    def test_has_node(self):
        graph1 = sandbox_regex.Graph() # which doesn't have an "example" node
        graph2 = sandbox_regex.Graph()
        graph2.graph_dict["example"] = [42] # has an "example" node
        self.assertTrue(graph2.has_node("example"))
        self.assertFalse(graph1.has_node("example"))

    def test_update_node(self):
        graph = sandbox_regex.Graph()
        graph.update_node("example", [1, "ex"])
        self.assertEqual(graph.graph_dict["example"], [1, "ex"])

    def test_add_new_next_to_node(self): 
        graph = sandbox_regex.Graph()
        node = sandbox_regex.Node()
        graph.graph_dict[node]=[]
        next = 42
        graph.add_new_next_to_node(node, next)
        self.assertEqual(graph.graph_dict[node][-1], next)

    def to_replace(self, word):#delete the ':' of a word
        word = word.replace(":", "")
        word = word.replace("(", "")
        word = word.replace(")", "")
        return word

    def str(self, graph):
        if graph.graph_dict=={}:
            raise unittest.SkipTest('end because graph_dict is empty')
        ret_string = graph.__str__()
        lignes = ret_string.split("\n") # table of lignes
        l = 2

        self.assertEqual(lignes[0], "")
        self.assertEqual(lignes[1], "-- Node graph --")
        li1 = lignes[l] # first real line after "Node graph"
        elements1 = li1.split(" ") # word by word
        name = elements1[0]
        name = self.to_replace(name)
        def find(graph, name):# return the index and the node of the name in graph_dict
            for index, node in enumerate(graph.graph_dict.keys()):
                if str(node.name) == name: # we consider here that the is 1 node for 1 name
                    return index, node
            return None, None
        index, node1 = find(graph, name)
        self.assertEqual(node1, graph.graph_dict.keys()[index] )
        if node1.value == None:
            n = 1
        else:
            n = 2
        for i in range (len(graph.graph_dict[node1])):
                self.assertEqual(str(graph.graph_dict[node1][i]), elements1[n])

        li2 = lignes[l+1]
        while ((li1 != "") and (li2 != "")): #before --Canonial graph-- we have a "\n"
            elements1 = li1.split(" ") #word by word
            elements2 = li2.split(" ")
            name1 = self.to_replace(elements1[0])
            n1, node1 = find(graph, name1)
            name2 = self.to_replace(elements2[0])
            n2, node2 = find(graph, name2)
            self.assertGreater(int(node2.name), int(node1.name))
            for i in range (len(graph.graph_dict[node2])):
                self.assertEqual(graph.graph_dict[node2][i], elements2[i+1])
            l += 1
            li1 = lignes[l]
            li2 = lignes[l+1]

        l += 3 # beginning of the second part of the string, exists
        li = lignes[l]
        elements = li.split(" ")
        n = 0 #index of canon_graph_dict.keys()
        while (l < len(lignes)-2 ): # because at the end there are 2 times "\n"
            i = 1 #index in elements[]
            if (elements[0]==">"):
                self.assertEqual(graph.canon_graph_dict.keys()[n], graph.start_state)
            elif (elements[0]=="#"):
                self.assertIn(graph.canon_graph_dict.keys()[n], graph.end_states)
            else: # there are 2 spaces, and when you split them at the beginning of the string, it makes 2 time ''
                self.assertEqual(elements[0], "")
                self.assertEqual(elements[1], "")
                i = 2
            state = self.to_replace(elements[i])
            self.assertEqual(state, str(graph.canon_graph_dict.keys()[n]))
            self.assertEqual(elements[i+1], str(graph.canon_graph_dict[int(state)]))
            l += 1
            n += 1
            li = lignes[l]
            elements = li.split(" ")
        self.assertEqual(lignes[l], "")

    def test__str__empty(self):
        graph = sandbox_regex.Graph()
        self.str(graph)
    def test__str__(self):
        graph = sandbox_regex.Graph()
        node1 = sandbox_regex.Node()
        node1.value = 10
        node1.name = 11 # must be int ?? for int(node.name) works
        # ! str(node1) = '(1111: )'
        node2 = sandbox_regex.Node()
        node2.name = 22
        node2.value = 2
        graph.graph_dict[node1] = [21] # must be a list
        node3 = sandbox_regex.Node()
        graph.graph_dict[node3] = []
        node3.name = 33
        graph.end_states.append(1)
        graph.canon_graph_dict = { 0: 39, 1: 40, 2: 41, 3: 42} # to test all the conditions, the keys must be numbers
        self.str(graph)

    def test_get_node_for_idx(self):
        graph = sandbox_regex.Graph()
        node1 = sandbox_regex.Node()
        node2 = sandbox_regex.Node()
        node3 = sandbox_regex.Node()
        graph.node_list = [node1, node2, node3]
        l = len(graph.node_list)
        if (l<=0):
            self.assertIsNone(graph.get_node_for_idx(-2))
            self.assertIsNone(graph.get_node_for_idx(2))
        if (l>0):
            self.assertIsNone(graph.get_node_for_idx(-1))
            self.assertIsNone(graph.get_node_for_idx(l))
            self.assertIsNone(graph.get_node_for_idx(l+1))
            self.assertEqual(graph.get_node_for_idx(l-1), node3)

    def test_get_re_index_for_pos(self):
        graph = sandbox_regex.Graph()
        regex_list = [{"smt": -2, "pos": 7}, {"smt": 2, "pos": 3}] # for instance if I have understand the format of the list
        self.assertEqual(graph.get_re_index_for_pos(regex_list, 3), 1)
        self.assertEqual(graph.get_re_index_for_pos(regex_list, 7), 0)
        self.assertEqual(graph.get_re_index_for_pos(regex_list, 2), 1)
        self.assertEqual(graph.get_re_index_for_pos(regex_list, 6), 0)
        self.assertEqual(graph.get_re_index_for_pos(regex_list, 0), -1) # for exemple 0 but we can choose any int different from 2 and 3

    def test_get_next_idx_for_regex_item(self):
        graph = sandbox_regex.Graph()
        regex_list = [{"smt": -2, "pos": 7}, {"smt": 2, "pos": 3}]
        regex_item = { "pos": 5, "nextpos": 3 } # for instance
        self.assertEqual(graph.get_next_idx_for_regex_item(regex_list, regex_item), 1)
        regex_item = { "pos": 5, "nextpos": 6 }
        self.assertEqual(graph.get_next_idx_for_regex_item(regex_list, regex_item), 0)
        regex_item = { "pos": 5, "nextpos": 42 } # get_re_index_for_pos will return '-1' -> raising exception
        with self.assertRaises(Exception):
            graph.get_next_idx_for_regex_item(regex_list, regex_item)
    
# this test will FAIL because fill_from_regex_list() change start_node but there is an assertion on start_node==Node
    def test_fill_from_regex_list(self):
        graph = sandbox_regex.Graph()
        regex_list = [ {"type":"jump_backward", "value": 42, "start_node": True, "pos": 43}, {"type":"jump_forward", "value": 42, "start_node": False, "pos": 43}, {"type":"end", "value": 422, "start_node": False, "pos": 433}, {"type":"ty", "value": 422, "start_node": True, "pos": 433} ] # for instance
        test_fill(self, graph, regex_list) # test_fill is defined at the beginning of the file
        graph.start_node = 42
        test_fill(self, graph, regex_list) # en Exception must be raised
        # we have tested all the posibilities for node_list so also for graph_dict


# test_get_character_nodes(self): ERROR
# erreur on the example graph_dict, infinity all the iteration...
# you will find the function at the end of this file



    def test_find_node_type_jump(self):
        graph = sandbox_regex.Graph()
        current_node = sandbox_regex.Node()
        graph.graph_dict[current_node] = False
        node = sandbox_regex.Node()
        backup_dict = {}
        node1 = sandbox_regex.Node()
        node2 = sandbox_regex.Node()
        backup_dict[current_node]=[node1, node2] # for instance
        # the function test_find is at the beginning of the file
        test_find(self, graph, current_node, node, backup_dict) # current_node.is_type_jump() is false
        current_node.type = current_node.TYPE_JUMP_BACKWARD
        test_find(self, graph, current_node, current_node, backup_dict) # will succeed
        test_find(self, graph, current_node, node, backup_dict) # fail beacuse not self.graph_dict[current_node]
        graph.graph_dict[current_node] = True
        print(graph.graph_dict[current_node])
        test_find(self, graph, current_node, node, backup_dict) # fail
        backup_dict[node2] = [node]
        test_find(self, graph, current_node, node, backup_dict) # succeed
        node2.type = node2.TYPE_JUMP_BACKWARD
        print(graph.graph_dict[current_node])
        test_find(self, graph, current_node, node, backup_dict) # succeed

# ERROR beacuse this function uses get_character_nodes which doesn't work...
    """
    def test_reduce(self):
    	graph = sandbox_regex.Graph()
        node1 = sandbox_regex.Node()
        node2 = sandbox_regex.Node()
        node3 = sandbox_regex.Node()
        node4 = sandbox_regex.Node()
        node5 = sandbox_regex.Node()
        node2.set_type_character() # by default it is not true, this won"t be del
        node3.set_type_jump_forward() # will be del
        node4.set_type_jump_backward()
        graph.start_node = node4 # so node4 will survive
        graph.graph_dict = { node1: [node5], node2: [node5], node3: [node5], node4: [node1] }
    	old_graph_dict = deepcopy(graph.graph_dict)

    	graph.reduce()
    	new_graph_dict = graph.graph_dict

    	def reduce_first(self):
    	    for node in self.graph_dict.keys():
                if node.is_type_character():
                    self.graph_dict[node] = self.get_character_nodes(node)
    	reduce_first(graph)
    	backup_dict = dict(graph.graph_dict)

    	for node in old_graph_dict.keys():
    	    if node not in new_graph_dict.keys():
    	        self.assertTrue(node.is_type_jump()) and self.assertFalse(graph.find_node_type_jump(graph.start_node, node, backup_dict))
    	    else:
    	        if node.is_type_character():
                    self.assertEqual(new_graph_dict[node], graph.get_character_nodes(node))
    	        else:
                    self.assertEqual(new_graph_dict[node], old_graph_dict[node])
    	            ( self.assertTrue(node.is_type_jump()) and self.assertTrue(graph.find_node_type_jump(graph.start_node, node, backup_dict)) ) or self.assertFalse(node.is_type_jump())

"""
    def get_edges(self):
        graph = sandbox_regex.Graph()
        node = sandbox_regex.Node()
        node1 = sandbox_regex.Node()
        node1.set_type_end()
        node2 = sandbox_regex.Node()
        graph.graph_dict[node] = [node1, node2]

        is_end_state, edges = graph.get_edges(node)
        indice = 0
        if is_end_state==False:
            for next in graph.graph_dict[node]: # for all of them
                self.assertFalse(next.is_type_end())
                self.assertEqual( edges[indice], (next.value, int(next.name)) )
                indice +=1
        else: # at least one is True
            bol = False
            indice = 0
            for next in graph_dict[node]:
                if next.is_type_end():
                    bol = True
                    self.assertNotIn((next.value(), int(next.name())))
                else:
                    self.assertEqual(edges[indice], (next.value, int(next.name)) )
                    indice +=1
            self.assertTrue(bol)

        # finally for my example:
        self.assertTrue(is_end_state)
        self.assertEqual(edges, [(node2.value, int(node2.name))])

    def test_convert_to_canonical(self):
        graph = sandbox_regex.Graph()
        node1 = sandbox_regex.Node()
        node1.name = 1
        node2 = sandbox_regex.Node()
        node2.name = 2
        node3 = sandbox_regex.Node()
        node3.name = 3
        node4 = sandbox_regex.Node()
        node1.set_type_end()
        node4.set_type_end()
        node4.name = "0"
        graph.graph_dict = { node1: 1, node2: [node3, node4] }
        old_graph_dict = deepcopy (graph.graph_dict)
        number_canon_list = len(graph.canon_graph_dict) # number of elements in canon_graph_dict

        def find_name_in_list(name, List):
            for node in List:
                if node.name == name:
                    return node
            return None

        graph.convert_to_canonical()
        for node in graph.graph_dict.keys():
            if node.name=="0":
                self.assertEqual(graph.start_state, -1)
                self.assertIn((node.value, 0), graph.canon_graph_dict)
                number_canon_list += 1
            if node.is_type_end():
                old_node = find_name_in_list(node.name, old_graph_dict)
                for node in old_graph_dict:
                    print(node)
                print(node)
		print("old", old_node)
                self.assertEqual(node, old_node)
            else:
                is_end_state, edges = graph.get_edges(node)
                self.assertEqual(graph.canon_graph_dict[int(node.name)], edges)
                number_canon_list += 1
                if is_end_state==True:
                    self.assertIn(int(node.name), graph.end_states)
        self.assertEqual(number_canon_list, len(graph.canon_graph_dict))

                  
    def test_need_use_plus(self):
        graph = sandbox_regex.Graph()
        string_to_add = "hello"
        initial_string = "blabla"
        self.assertFalse(graph.need_use_plus(initial_string, string_to_add))
        test_need(self, graph, initial_string, string_to_add) # test_need is defined at the beginning of the file
        string_to_add = "(hello)*"
        self.assertFalse(graph.need_use_plus(initial_string, string_to_add))
        test_need(self, graph, initial_string, string_to_add)
        initial_string = "blabla hello"
        self.assertTrue(graph.need_use_plus(initial_string, string_to_add))
        test_need(self, graph, initial_string, string_to_add)
        initial_string = "blabla hello"
        self.assertTrue(graph.need_use_plus(initial_string, string_to_add))
        test_need(self, graph, initial_string, string_to_add)
        string_to_add = "hello*"
        initial_string = "blabla hello*"
        self.assertTrue(graph.need_use_plus(initial_string, string_to_add))
        test_need(self, graph, initial_string, string_to_add)

    def test_unify_two_strings(self):
    	graph = sandbox_regex.Graph()
    	s1 = "hello sir and madam, welcome" # exemples to cover all the case
    	s2 = "hello ladies, welcome"
    	s11 = "hello sir"
    	s12 = "hello madam and sir"
    	s21 = "hello"
    	s22 = "hello"
    	s31 = "hello ssir"
    	s32 = "hello sir"
    	def unify(s1, s2):
            word = graph.unify_two_strings(s1, s2)
            def position(word, charact): # find the position of a character in a word
                pos = -1
                while (pos+1)<len(word) and word[pos+1]!=charact:
                    pos +=1
                return pos+1
            if '?' in word: # begin+end=s1 or s2
                self.assertIsNot(s1, s2)
                if '(' in word:
                    begin = position(word, '(')
                    w_begin = word[:begin]
                    end = position(word, ')')
                    w_end = word[(end+2):]
                    if len(s1)>len(s2):
                        self.assertEqual(w_begin+word[begin+1:end]+w_end, s1)
                        self.assertEqual(word_begin+word_end, s2)
                    else:
                        self.assertEqual(w_begin+word[(begin+1):end]+w_end, s2)
                        self.assertEqual(w_begin+w_end, s1)
                else: # len(s2)=1
                    i = position(word, '?')
                    if len(s1)>len(s2):
                        self.assertEqual(word[:i]+word[i+1:], s1) and self.assertEqual(word[:i-1]+word[i+1:], s2)
                    else:
                        self.assertEqual(word[:i]+word[i+1:], s2) and self.assertEqual(word[:i-1]+word[i+1:], s1)
            elif '|' in word: # s1 != s2 and word!=s1,s2
                self.assertNotIn(s1, s2) and self.assertNotIn(s2, s1)
                begin = position(word, '(')
                w_begin = word[:begin]
                end = position(word, ')')
                w_end = word[(end+1):]
                middle = position(word, '|')
                r_s1 = word[(begin+1):middle]
                r_s2 = word[(middle+1):end]
                self.assertEqual(w_begin+r_s1+w_end, s1)
                self.assertEqual(w_begin+r_s2+w_end, s2)
            else: # s1=s2
                self.assertEqual(s1, s2)
                self.assertEqual(word, s1)
        unify(s1, s2)
        unify(s11, s12)
        unify(s21, s22)
        unify(s31, s32)

    def test_unify_strings(self):
    	graph = sandbox_regex.Graph()
    	s1 = "hello sir and madam, welcome" # exemples to cover all the case
    	s2 = "hello ladies, welcome"
    	s11 = "hello sir"
    	s12 = "hello madam and sir"
    	s21 = "hello"
        string_list = [s1, s2, s11, s12, s21] # for instance
        a = graph.unify_strings(string_list)
        if a==None:
            self.assertIsNot(string_list)
        elif len(string_list)==1:
            self.assertEqual(string_list[0], a)
        else:
            self.assertIsInstance(a, str) # the function unify_two_strings has already been verified
        self.assertEqual(graph.unify_strings(string_list), "hello( (((sir and madam|ladies), welcome|sir)|madam and sir))?")

    def test_remove_state(self):
        state_to_remove = sandbox_regex.Node()
        node = sandbox_regex.Node()
        node2 = sandbox_regex.Node()
        graph = sandbox_regex.Graph()
        graph.canon_graph_dict[state_to_remove]=[("Ah", node), ("A", state_to_remove), ("Ah", state_to_remove)]
        graph.canon_graph_dict[node] = [("Oh", state_to_remove), ("Ohh", node2)]
        old_canon = deepcopy (graph.canon_graph_dict)

        itself_string = ""
        for (next_string, next_state) in graph.canon_graph_dict[state_to_remove]:
            if next_state == state_to_remove:
                if len(next_string) > 1:
                    itself_string = "(%s)*" % next_string
                else:
                    itself_string = "%s*" % next_string
        
        # self.assertEqual(graph.canon_graph_dict, old_canon)
        graph.remove_state(state_to_remove)
        new_canon = graph.canon_graph_dict
        # self.assertIn(state_to_remove, old_canon.keys()) # I don't know why this ligne didn't work
        self.assertNotIn(state_to_remove, new_canon.keys())
        self.assertEqual(len(old_canon.keys()), len(new_canon.keys())+1)
        for state in new_canon.keys():
            print(state)
            print(old_canon)
            self.assertIn(state, old_canon.keys())
            print(old_canon[state])
            s_list = old_canon[state]
            i_o = 0 # number of tuple passed in s_list
            i_n = 0 # number in new list
            remove_list = [] # list with all the couple removed from s_list
            for (next_string, next_state) in s_list:
                if s_list[i_o]==new_canon[state][i_n]: # no change
                    self.assertNotEqual(next_state, state_to_remove)
                    i_o += 1
                    i_n += 1
                else:
                    self.assertEqual(next_state, state_to_remove)
                    self.assertIsNot((next_string, next_state), new_canon[state])
                    i_o += 1
                    remove_list.append(next_string, next_state)

            index = 0 # index of the remove couple
            for (next_sting, next_state) in new_canon[state]:
                if (next_string, next_state) not in s_list: # those which have been append
                    (old_string, old_state) = remove_list[index]
                    to_strings = {}
                    for state2 in new_canon.keys():
                        to_strings[state2] = []
                        if state2 == state_to_remove:
                            continue
                        for (iter_to_string, iter_to_state) in old_canon[state_to_remove]:
                            if iter_to_state == state2:
                                to_strings[state2].append(iter_to_string)
                        to_string = unified_to_string[state2]
                        if (next_string, next_state)==(old_string + "+" + to_string, state2):
                            self.assertTrue(graph.need_use_plus(next_string, itself_string))
                        else:
                            self.assertEqual( (next_string, next_state)==(old_string + itself_string + to_string, state2) )
                index += 1

    def test_simplify(self):
        graph = sandbox_regex.Graph()
        old_graph_dict = deepcopy(graph.graph_dict)
        graph.simplify()
        for state in old_graph_dict.keys():
            if state not in grap.graph_dict:
                self.assertNotEqual(state, graph.start_state)
                self.assertNotIn(state, graph.end_states)
            else:
                self.assertEqual(state, graph.start_state) or self.assertIn(state, graph.end_states)
                
    def test_combine_start_end_nodes(self):
        graph = sandbox_regex.Graph()
        node = sandbox_regex.Node()
        graph.start_state = node
        node1 = sandbox_regex.node()
        node2 = sandbox_regex.node()
        node3 = sandbox_regex.node()
        graph.canon_graph_dict[node] = [ ("node1", node1), ("node2", node2), ("node3", node3) ]
        graph.end_states = [ node2, node3 ]
        graph.canon_graph_dict[node3] = [("node1", node1), ("node", node3), ("node*", node3)]
        # graph.need_use_plus("node3", "node") = False # must be
        # graph.need_use_plus("node3", "node*") = True # must be
        # so we must have at the end :
        final_strings = [ ("node2", None), ("node3node1", None), ("node3node", None), ("node3+", None) ]
        tab = [x[0] for x in final_strings]
        unified_regex = graph.unify_strings(tab)
        result = graph.combine_start_end_nodes(graph)
        self.assertEqual(result, unified_regex)


if __name__ == '__main__':
    unittest.main()

""" 
def is_here(caract, graph, node): #used for the function following
        if (caract in graph.graph_dict[node]) and (caract.is_type_character() or caract.is_type_end()):
            return True
        elif (caract in graph.graph_dict.keys()):
            for next in graph.graph_dict[caract]:
                if ((is_here(next, graph, caract))==True):
                    return True
        else:
            return False
            
    def test_get_character_nodes(self):
        graph = sandbox_regex.Graph()
        one = sandbox_regex.Node()
        two = sandbox_regex.Node()
        three = sandbox_regex.Node()
        graph.graph_dict = {one: [three, two], "pos": [one, two], two: [one], three: [one]}
        node_list = graph.get_character_nodes("pos") #"pos" is an exemple
        for node in graph.graph_dict.keys():
            for elem in graph.graph_dict[node]:
                if elem in node_list:
                    self.assertIsTrue(is_here(elem, graph, "pos"))
                else:
                    self.assertIsFalse(is_here(elem, graph, "pos"))
  """  

"""def test_init_with_no_args(self):
#Tests the initialisation with no arguments
        with self.assertRaises(TypeError): # suceed if an exception is raised -> vérifier que c'est impossible d'appeler la fonction sans argument, en fait si c'est possible puisque les arguments sont données None par défaut ?
            sandbox_regex.Node()
    """
