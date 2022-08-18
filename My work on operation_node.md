ong_mark_not() : parent_node & nodes_to_process not unsed but in the parameters
same in ong_end_path() + g not returned, I don't know how but g is modified when the function is called, even if it is not defined as a global variable

we have to defined every time self.raw because I don't know why but it called the function hash
beware, 
/!!!!!!!!\ : it is extremely dangerous to base the __eq__function only on node.raw, because if 2 nodes are different but have the same raw, the computer will make them equal at all the points, for example when I tried to print g[Node2] it print g[Node3] but it was false !!!

+ I didn't know exactly with what to test 'parent_node' beacuse of the line 'if parent_node', because if we attempt to put an unkown node to parent_node, it passes 'if parent_node', but raises an error after because it exists not g

in remove_node_in_operation_node_graph():
why remove nodes from g[node_to_remove]["list"] and after remove g[node_to_remove] ?
error : set changed size during iteration; we must create a copy (I tried to make a function_corr)
so I added also 'from copy import deepcopy' at the beginning

test_get_operation_node_graph_paths:
where is the logger file ??

remove_duplicate_node_edges : need to actualize g each time 

clean_nodes_in_operation_node_graph : logger and warnings on the terminal, was it the goal ?

ReducedVertice():

_replace_in_list : doesn't return anything, so we don't keep the changes in mind + pbl of iteration of return ? if we want to change more than 1 vertice. I write after a proposition of correction
replace_in_list : I have replaced _replace_in_list by _replace_in_list_corr

add of __eq__ and lst__eq__() to evaluate the equality of  lists of ReducedVertice()

beware, using the same database in the tests implies that when you modified some values, you modified them in the other functions and it can raise errors -> re-init() function that I used at the beginning of all test function

recursive_str : very difficult to test all possibilities, beacuse when you pass a condition, some objects must have some caracteristics which can be very difficult to have, like 'if "(require-any" in value:' and 'self.value.str_not()' which means that self.value must be an instance of class NonTerminalNode or OperationNode, and calls a function which implies that some objects must have also some caracteristics...

conclusion : difficult to test, and it is easy for the fucntions to raise errors with the object taken in entry

str_print_not() : correction of a line which could be improve for the complexity

for all the functions str_*, the functions like str_debug() are defined for many classes, I choose to test the function with only 1 or 2 classes each time, I believe it is not the thing that could make failed the function

__eq__ add in class ReducedGraph used for my tests + lst_eq_ to test the equality of 2 lists of graphs + idem in the class ReducedEdge

qu° for the __eq__ : should 2 instances be equal even if they don't have the same name ??

test_remove_vertice_update_decision : I didn't succeed to verify that the decision were change if e.end==v, because the edge is removed so I don't know were to find it. However, as we verify that it was removed and that the operation to change the object 'decision' is very simple, I think it don't worth it to look deeply into this non-verify problem
