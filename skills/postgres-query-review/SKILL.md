---
name: postgres-query-review
description: Reviews PostgreSQL queries and execution plans for correctness and performance. Use when diagnosing a slow query, interpreting EXPLAIN output, or evaluating index changes.
license: Apache-2.0
---

# PostgreSQL query review

Review query behavior using observed evidence before recommending changes.

## Inputs to seek

- Query text and intended result, including parameter values or selectivity where relevant.
- PostgreSQL version, schema, indexes, row counts, and workload constraints.
- An `EXPLAIN (ANALYZE, BUFFERS)` plan when one is already available and safe to obtain. A plain `EXPLAIN` plan is useful but contains estimates rather than measured execution.

## Workflow

1. Check semantic correctness first: filtering, joins, null handling, ordering, limits, and transaction behavior.
2. Read the plan from leaves toward the root. Compare estimated and actual row counts, loops, scan types, join choices, sorts, and buffer activity where present.
3. Form specific hypotheses for the largest observed cost. Separate plan evidence from possibilities that require schema or workload data.
4. Recommend the smallest useful query, index, statistics, or schema change. Explain the expected benefit and its write, storage, or maintenance cost.
5. Propose a safe measurement plan using the same workload and data shape. Compare before and after latency, rows, buffers, and regression risk.

## Safety and evidence

- `EXPLAIN ANALYZE` executes the statement. Do not run it on a production or data-modifying query without explicit authorization and an appropriate safety plan. A transaction rollback does not necessarily undo external side effects.
- Do not execute SQL, change indexes, or modify data unless the user authorizes the action.
- Do not claim an index will help solely because a column appears in a predicate. Check selectivity, access pattern, and observed plan.
- Do not invent plan nodes, timings, row counts, or benchmark results.

## Output

Report correctness findings, observed bottlenecks, recommendations, trade-offs, and how to verify each change. Cite the supplied plan or schema evidence. If evidence is missing, ask only for inputs that would change the recommendation.

## Reference

PostgreSQL documents that `EXPLAIN ANALYZE` executes its statement: https://www.postgresql.org/docs/current/sql-explain.html
