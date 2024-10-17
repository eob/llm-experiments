# Are LLMs less racist if they have to explain themselves?

The context for this code is at:

* [Blog writeup](https://edwardbenson.com/2024/10/llms-are-less-racist-if-they-explain-themselves)
* [Spreadsheet data](https://docs.google.com/spreadsheets/d/15uKNVNJRp1RKtWgZCvbh_pOajy3Ncr9A621MUMWv4NI/edit?gid=0#gid=0)

## Running

From the project root, run:

```bash
PYTHONPATH=`pwd`/src python src/llm_experiments/reducing_racism/main.py
```

## Example Result

Using the following:

```
run_with("No explanation", 500, PROMPT_PREFIX + WITHOUT_REASON)
run_with("Explanation", 500, PROMPT_PREFIX + WITH_REASON)
```

For the case in which no explanation was required, I got:

```
CASE 1: EXPLANATIONS, THEN CHOICE
Total trials: 13619
- (Black, Asian):        1.5% bias favoring Asian    (0.015818)
- (Black, White):        1.8% bias favoring White    (0.018409)
- (Hispanic, White):     2.8% bias favoring White    (0.028149)
- (White, Asian):        3.6% bias favoring Asian    (0.036102)
- (Black, Hispanic):     5.5% bias favoring Hispanic (0.054875)
- (Hispanic, Asian):    33.0% bias favoring Asian    (0.329766)
 

CASE 2: NO EXPLANATION FOR CHOICE
Total trials: 12033
- (Black, White):     0.5% bias favoring Black    (-0.004960)
- (Black, Hispanic):  3.6% bias favoring Hispanic  (0.035964)
- (Hispanic, White): 12.7% bias favoring Hispanic (-0.126746)
- (Black, Asian):    18.6% bias favoring Asian     (0.186220)
- (Hispanic, Asian): 27.4% bias favoring Asian     (0.273726)
- (White, Asian):    31.5% bias favoring Asian     (0.315054)

```
