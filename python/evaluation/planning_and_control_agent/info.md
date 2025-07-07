# STATS

- fixed code so it works for planning and control
- added option to choose how many problems and what level to be run (you choose how many and which level, problems are chosen randomly) - still gotta fix some minor issues
- added time and cost tracking.

1. I ran 2 very easy problems
- Total benchmark time: 1621.63s
- Total cost: 0.59965

2. I ran 3 random usaco problems:
- Total benchmark time: 1959.68s
- Total cost: 1.522318
- One of the problems was platinum level, just for testing. Failed. We won't be doing platinum problems in the future, like we said last time.
- For the other problems, the silver and gold one, failed because of execution time, but all of the test cases before that passed, so most likely the
code was good in terms of corectness

3. I ran 5 random usaco problems (2 x bronze, 2 x silver, 1 x gold)
- bronze passed, silver exec limit reached (on last test case, which again suggest code was technically correct), gold wrong answer
- Total benchmark time: 3006.73s
- Total cost: 2.24801

Average cost per problem (upper limit) : $0.5
Average time per problem (upper limit) : 750s

Therefore, 

Average cost 300 problems: ~$150
Average time 300 problems: ~60h