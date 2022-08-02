### NonTerminalNode
***

In the majority of the functions, these were defined with '__' in front of them, but when I tried ti import them in my test file it ddidn't recognized them, so I had to supress at least 1 of the '_' (1 time I had to supress the 2, I don't know why...)
So I modified your original file + I add commentaries on some functions
For example I added some comm to some lines even if they didn't sent errors

**Here are some of important comments I made :**

- In the function *'simplify_list'* defined line 55 (of my file) : FAILED  
-> if there is at least 3 versions of 1 word, the function won't keep only 1 version of the word, but at least 2 like (I took an example in the code)  
-> no detection of only 1 word if there is "ex/" and "/ex" for instance (they are supposed to be considered as equal right ?)  
so my test failed

- The functions *'single_argument_regex'* line 241 and *'_not_regex'* line 349 are the same except the names of the variables

- In the function *'str_not(self)'*, defined line 407, I think there is an error of ident and others, because in the part where self.argument is not a list there are part of the code which considered it as a list. Plus some parts of the code don't return anything.
I tried to understand whatc can be possible to correct this, I wrote just after str_not() a function *'corr_str_not(self)'* and I based a quick test on it.
Let me know if I understand correctly and what is the correct function, and I will write the test.

- In the function *'is_last_regular_expression'*, the variable *"num_regex"* is used but undefined

- In the function *'is_non_terminal_deny'* line 505 and after, the functions *'is_terminal()'* and *'is_non_terminal()'* are undefined, NonTerminalNode as not object *'terminal'*, and the function *'is_allow'* is unknown, and there is the same issues for the other functions after so I couldn't run the tests




here are my comments, I hope they will help you !
