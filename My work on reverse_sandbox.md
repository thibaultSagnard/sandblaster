### What I have done for now :
***

- modification in the folder reverse_sandbox of *regex_parser_v1.py*, *regex_parser_v2.py* and *regex_parser_v3.py* to add 1 line of code at the beginning to import the files
- modification of *sandbox_regex.py* :
    -> at the beginning 1 line ti import the file
    -> line 137 there was an oversight of 'self.'
    -> I have added in the class Node an '__hash__' and '__eq__' and '__ne__' functions 
    -> I have commented a lot of lines, it is more for me, but it could help people who didn't write it to understand the code
    
- creation of the file *'sandbox_regex_test.py'* ; I have 1 or 2 functions left to work on at the end of the file, I have quite finished the others, unless some of them are not working well yet

When I run the code with **'python2 -m unittest discover -v -s tests/ -p 'sandbox_regex_test.py'** I have :  
    -> 30 correct tests  
    -> 1 skipped; it is normal, the test verify that the code return an AssertError, and to avoid the other tests running I skipped the other part of the function, perhaps there is another way to not skipped it, I will check it later  
    -> **2 errors and 1 failure, 3 skipped**  
   
   
- In *'test_combine_start_end_nodes'* : FAIL (I need to check)
- In *'test_find_node_type_jump'* : ERROR ; keyError, 'find_node_type_jump' doesn't recognize graph_dict[current_node] which I created before running the test, so I don't understand... I need to check
- In *'test_fill_from_regex_list'* : SKIP ; because the original function 'fill_from_regex_list' doesn't allow to go to the loop line 216 twice because of the 'assert(self.start_node == None)' which we modified the line after, however we can imagine entries where you could enter twice the loop, so do I, and so the test failed. So I skipped it, and if in the reality of the project we can go twice in the the loop there is something to change..
- test__str__ : keyError

- In *'test_convert_to_canonical'* which runs correctly I print something, it's very strange because if I supress the lines of print, it failed with 2 things that are not equal anymore, unless they are when I print them... perhaps an error linked to hash function...? Sometimes it failed also even with the print ...

There are also some others errors that could appears, but then dissapears when I believe to do anything so it's very strange...
