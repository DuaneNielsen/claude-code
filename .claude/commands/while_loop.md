---
argument-hint: [number]
description: generate a list of random numbers < [number]
---
@.claude/include/substitutions.md

list_of_numbers = []

while (the_condition) todo:
   1. generate a random number
   2. add the number to list of numbers

output the number

## the condition
the most recently generated random number is less than $ARGUMENT

## generate a random number

```bash
$WORKING_DIR/claude/scripts/random.sh
```

## output format

The random numbers where <list_of_numbers>