# Model Migration - Detailed Results (5 Core Queries)

**Migration**: all-MiniLM-L6-v2 → multilingual-e5-small

> **Summary**: See `validation-summary-v2.md`
> **Queries**: 3 Semantic + 2 Practical (balanced mix)

---

## BEFORE (all-MiniLM-L6-v2)

### Group 1: Semantic Queries (Abstract Understanding)

#### Q1: backend engineer
**Expected**: Alice (ID 1) - Python, FastAPI, backend projects
**Type**: Semantic - Tests if model understands "backend engineer" concept

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
|  1   |     195     |  training  | 0.53  |    No     |
|  2   |     75      |     cv     | 0.53  |    No     |
|  3   |      1      | experience | 0.52  |   Yes     |

**Precision@3**: 1 / 3 = **33%**


---

#### Q2: UI developer
**Expected**: Bob (ID 2) - React, Angular, frontend
**Type**: Semantic - Tests "UI developer" → React/Angular understanding

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    |      3      | experience | 0.476 |    No     |
| 2    |    147      |  training  | 0.442 |    No     |
| 3    |     27      |  training  | 0.442 |    No     |

**Precision@3**: 0 / 3 = **0%** ❌


**Notes**: Bob (ID 2) KHÔNG xuất hiện trong top 3! Semantic matching rất kém.

---

#### Q3: vector database expert
**Expected**: Alice (ID 1) - pgvector project, PostgreSQL
**Type**: Semantic - Tests domain knowledge understanding

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    |    147      |  training  | 0.491 |    No     |
| 2    |     27      |  training  | 0.491 |    No     |
| 3    |    187      |  training  | 0.461 |    No     |

**Precision@3**: 0 / 3 = **0%** ❌


**Notes**: Alice (ID 1) KHÔNG xuất hiện! Model không hiểu "vector database" ≈ pgvector.

---

### Group 2: Practical Queries (Tech Stack - HR Searches)

#### Q4: Python developer
**Expected**: Alice (ID 1) - Python level 5, 6 years experience
**Type**: Practical - Direct skill match (how HR actually searches)

| Rank | Employee ID | Field Type |       Score | Relevant? |
|:----:|:-----------:|:----------:|------------:|:---------:|
| 1    |   ____3_    | _____user_skill      |  _0.259____ | ☐ Yes     |
| 2    |   ____1_    | ___user_skill__      | __ 0.222___ | ☐ Yes     |
| 3    |    ___203__    | __user_skill___      |    0.2048   _____ | ☐ Yes     |

**Precision@3**: __3_ / 3

---

#### Q5: React developer
**Expected**: Bob (ID 2) - React level 5, expert frontend
**Type**: Practical - Direct skill match

| Rank | Employee ID | Field Type |        Score | Relevant? |
|:----:|:-----------:|:----------:|-------------:|:---------:|
| 1    |   __57___   | ___user_skill__      |    __0.481__ | ☐ Yes     |
| 2    |  ___147__   | __user_skill___      |   0.481_____ | ☐ Yes     |
| 3    |   ___87__   | ___user_skill__      | 0.481  _____ | ☐ Yes     |

**Precision@3**: __3_ / 3

---

### BEFORE Summary

| Group | Avg P@3 | Notes |
|:------|:-------:|:------|
| Semantic (Q1-Q3) | **11%** | Very poor - model struggles with abstract queries |
| Practical (Q4-Q5) | **___%** | To be filled |
| **Overall** | **___%** | |

---

## AFTER (multilingual-e5-small)

### Group 1: Semantic Queries (Abstract Understanding)

#### Q1: backend engineer
**Expected**: Alice (ID 1)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3


---

#### Q2: UI developer
**Expected**: Bob (ID 2)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3


---

#### Q3: vector database expert
**Expected**: Alice (ID 1)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3


---

### Group 2: Practical Queries (Tech Stack - HR Searches)

#### Q4: Python developer
**Expected**: Alice (ID 1)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | __148___       | __user_skill___      | __0.0775___ | ☐ Yes     |
| 2    | ___178__       | ____user_skill_      | __0.0775___ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3


---

#### Q5: React developer
**Expected**: Bob (ID 2)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    |   _____20   | ___cv__      | 0.0627_____ | ☐ Yes     |
| 2    |  ____116_   | _cv____      | __0.0557___ | ☐ Yes     |
| 3    |   ___2__    | __cv___      | ___0.0492__ | ☐ Yes     |

**Precision@3**: __3_ / 3


---

### AFTER Summary

| Group | Avg P@3 | Notes |
|:------|:-------:|:------|
| Semantic (Q1-Q3) | **___%** | Expected improvement |
| Practical (Q4-Q5) | **___%** | Should be high |
| **Overall** | **___%** | |

---

## COMPARISON

### Semantic Queries Performance

| Query | BEFORE P@3 | AFTER P@3 | Δ | Improvement |
|:------|:----------:|:---------:|:-:|:-----------:|
| Q1: backend engineer | 33% | ___% | ___% | ___% |
| Q2: UI developer | 0% | ___% | ___% | ___% |
| Q3: vector database | 0% | ___% | ___% | ___% |
| **Average** | **11%** | **___%** | **___%** | **___%** |

### Practical Queries Performance

| Query | BEFORE P@3 | AFTER P@3 | Δ | Improvement |
|:------|:----------:|:---------:|:-:|:-----------:|
| Q4: Python developer | ___% | ___% | ___% | ___% |
| Q5: React developer | ___% | ___% | ___% | ___% |
| **Average** | **___%** | **___%** | **___%** | **___%** |

---

## KEY INSIGHTS

### BEFORE Model Issues

**Semantic Understanding**: ❌ Very poor (11% avg P@3)
- Q2 "UI developer" → 0% (Bob not in top 3)
- Q3 "vector database" → 0% (Alice not in top 3)
- Only Q1 has 1 relevant result (Alice at rank 3)

**Practical (Tech Stack)**: ___ (to be filled)

**Overall**: Old model **struggles with semantic queries** - relies too much on keyword matching.

---

### AFTER Model Improvements (Expected)

Based on research (+56% MTEB improvement):
- ✅ Semantic queries should improve significantly
- ✅ Practical queries should remain high/improve
- ✅ Overall P@3 target: **≥70%**

---

### Migration Success Criteria

- [ ] Semantic P@3 improves from 11% → **≥60%**
- [ ] Practical P@3 maintained at **≥80%**
- [ ] Overall P@3 **≥70%**
- [ ] Response time < 1 second

---

**Next**: Fill AFTER section + complete comparison analysis
