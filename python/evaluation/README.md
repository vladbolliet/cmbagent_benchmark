# Major modifications

- changed the way of calculating the accuracy (if one test case is wrong out of all test cases, problem is FAILED, OR, if test case doesn't execute in under 4s,
problem is FAILED). 
- changed code a little bit for handling anthropic and google models

# Short description of results

## Benchmark ran: first 33 problems of the selected 307 usaco problems (ALL MODELS WERE TESTED ON EXACT SAME PROBLEMS)

## Performances:

- **gpt-4.1-2025-04-14** : (*I did 2 bechmarks/evaluations on this one*)
    - first try: 18.18% total accuracy
    - second try: 15.15%
- **gpt-4o-2024-11-20** : 9.09%
- **claude-3-7-sonnet** : (*I did 2 bechmarks/evaluations*)
    - first try: 15.15%
    - second try 15.15%
- **gpt-3.5-turbo-0125**: 3.03%
- **gemini-2.5-pro**: 42.42%

## Refferences:

According to USACO benchmark, on zero-shot, gpt-3.5 performance was 0.59% and gpt-4 was 8.7% (https://arxiv.org/pdf/2404.10952v1)