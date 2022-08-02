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

