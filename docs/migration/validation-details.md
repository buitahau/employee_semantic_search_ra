# Model Migration - Detailed Results

**Migration**: all-MiniLM-L6-v2 → multilingual-e5-small

> **Summary metrics**: See `validation-summary.md`
> **Test queries**: See `test-queries.md`

---

## BEFORE (all-MiniLM-L6-v2)

### Group 1: Job Description Queries

#### Q1: backend engineer
**Expected**: Alice (ID 1)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
|  1   |     195     |     training     | 0.53 |    No     |
|  2   |     75      |     cv     |  0.53 |    No     |
|  3   |      1      |     experience     | 0.52 |   ☐ Yes   |

**Precision@3**: 1 / 3

---

#### Q2: UI developer
**Expected**: Bob (ID 2)

| Rank | Employee ID |     Field Type     |      Score | Relevant? |
|:----:|:-----------:|:------------------:|-----------:|:---------:|
| 1    |   __3___    |     experience     | __0.476___ |    No     |
| 2    |    147    |      training      |      0.442 |    No     |
| 3    |    _27___    |__training___       | 0.442_____ |   ☐ No    |

**Precision@3**: _0_ / 3

---

#### Q3: data pipeline specialist
**Expected**: Alice (ID 1)

| Rank | Employee ID | Field Type |        Score | Relevant? |
|:----:|:-----------:|:----------:|-------------:|:---------:|
| 1    |  ___170__   | __training___      |   0.479_____ |    No     |
| 2    |   ___50__   | ____training_      | 0.479  _____ |    No     |
| 3    |   ___1__    | ____experience_      |    0.46    _____ |   ☐ Yes   |

**Precision@3**: __1_ / 3

---

#### Q4: Python developer
**Expected**: Bob (ID 2)

| Rank | Employee ID | Field Type |      Score | Relevant? |
|:----:|:-----------:|:----------:|-----------:|:---------:|
| 1    |   __1___    | _____experience      |  __0.43___ |    No     |
| 2    |   ___3__    | ___task__      | __0.428___ |    No     |
| 3    |    __147__    | ____training      | __0.422___ |   ☐ No    |

**Precision@3**: 0__ / 3

---

### Group 2: Problem/Need-based Queries

#### Q5: who can build REST APIs
**Expected**: Alice (ID 1)

| Rank | Employee ID | Field Type |       Score | Relevant? |
|:----:|:-----------:|:----------:|------------:|:---------:|
| 1    | ____155_       | ___training__      |  0.516_____ | ☐ Yes     |
| 2    | ____35_       | _____ training     | 0.516 _____ | ☐ Yes     |
| 3    | _____195       | _____training      |   0.504    _____ | ☐ Yes     |

**Precision@3**: ___3 / 3

---

#### Q6: need someone to migrate legacy frontend
**Expected**: Bob (ID 2)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | ____186_       | _task____      | _0.445____ |    No     |
| 2    | ____136_       | ___task__      | ____0.445_ |    No     |
| 3    | ____86_       | _____ task     | ____ 0.445_ |    No     |

**Precision@3**: ___0 / 3

---

#### Q7: vector database expert
**Expected**: Alice (ID 1)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | ___147__       | _training____0.491      | _____ |    No     |
| 2    | ___27__       | ___training__      | 0.491 _____ |    No     |
| 3    | ____187_       | ____training_      | _0.461____ |    No     |

**Precision@3**: __0 / 3

---

#### Q8: build internal tools
**Expected**: Alice (ID 1)

| Rank | Employee ID | Field Type |      Score | Relevant? |
|:----:|:-----------:|:----------:|-----------:|:---------:|
| 1    |  __160___   | __experience___      | _0.493____ |    Yes    |
| 2    |   ___3__    | ____experience_      |      0.464_____ |    Yes    |
| 3    |    __40___    | ____experience_      |      0.462_____ |   ☐ Yes   |

**Precision@3**: _3__ / 3

---

### Group 3: Indirect Skills Queries

#### Q9: scalable backend systems
**Expected**: Alice (ID 1)

| Rank | Employee ID |      Field Type      |      Score | Relevant? |
|:----:|:-----------:|:--------------------:|-----------:|:---------:|
| 1    | ____147_       | _training____  0.471 |      _____ |    No     |
| 2    | _____27       |     training   _____         | __0.471___ |    No     |
| 3    | _____187       |        training_____         |      _0.459____ |   ☐ Yes   |

**Precision@3**: ___1 / 3

---

#### Q10: modern web interfaces
**Expected**: Bob (ID 2)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3
**Response Time**: _____ ms

---

#### Q11: database optimization
**Expected**: Alice (ID 1)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3
**Response Time**: _____ ms

---

#### Q12: component-based UI development
**Expected**: Bob (ID 2)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3
**Response Time**: _____ ms

---

## AFTER (multilingual-e5-small)

### Group 1: Job Description Queries

#### Q1: backend engineer
**Expected**: Alice (ID 1)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3
**Response Time**: _____ ms

---

#### Q2: UI developer
**Expected**: Bob (ID 2)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3
**Response Time**: _____ ms

---

#### Q3: data pipeline specialist
**Expected**: Alice (ID 1)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3
**Response Time**: _____ ms

---

#### Q4: frontend architect
**Expected**: Bob (ID 2)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3
**Response Time**: _____ ms

---

### Group 2: Problem/Need-based Queries

#### Q5: who can build REST APIs
**Expected**: Alice (ID 1)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3
**Response Time**: _____ ms

---

#### Q6: need someone to migrate legacy frontend
**Expected**: Bob (ID 2)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3
**Response Time**: _____ ms

---

#### Q7: vector database expert
**Expected**: Alice (ID 1)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3
**Response Time**: _____ ms

---

#### Q8: build internal tools
**Expected**: Alice (ID 1)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3
**Response Time**: _____ ms

---

### Group 3: Indirect Skills Queries

#### Q9: scalable backend systems
**Expected**: Alice (ID 1)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3
**Response Time**: _____ ms

---

#### Q10: modern web interfaces
**Expected**: Bob (ID 2)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3
**Response Time**: _____ ms

---

#### Q11: database optimization
**Expected**: Alice (ID 1)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3
**Response Time**: _____ ms

---

#### Q12: component-based UI development
**Expected**: Bob (ID 2)

| Rank | Employee ID | Field Type | Score | Relevant? |
|:----:|:-----------:|:----------:|------:|:---------:|
| 1    | _____       | _____      | _____ | ☐ Yes     |
| 2    | _____       | _____      | _____ | ☐ Yes     |
| 3    | _____       | _____      | _____ | ☐ Yes     |

**Precision@3**: ___ / 3
**Response Time**: _____ ms

---

## Notes

Use this space for qualitative observations:

**BEFORE model observations**:
________________________________________________________________
________________________________________________________________

**AFTER model observations**:
________________________________________________________________
________________________________________________________________

**Key differences noticed**:
________________________________________________________________
________________________________________________________________
