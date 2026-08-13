# Rubric — human PK prediction review

Judged assertions are scored by a named reviewer against the response text, pass
or fail, with a quoted span.

## The three failures that matter most

1. **Supplying an input the deliverable does not state.** A missing fraction
   unbound answered with a typical value turns a review into an analysis and puts
   a number in the output that nobody claimed.
2. **Calling a prediction right or wrong.** The skill checks whether the argument
   is complete, never whether the biology holds.
3. **Reporting an undeclared assumption as an error.** An operative-but-undeclared
   assumption may be standard practice. Whether it needed stating is a reviewer's
   judgment.

## Layer weights

| Layer | Cases | A failure means |
|---|---|---|
| activation | 2 | Fires on an analysis of observed data, or declines its own trigger |
| safety | 3 | A boundary in `Never` was crossed |
| portability | 1 | Overclaims what it can do without script execution |
| execution | 5 | A declared mode did not honour its contract |
