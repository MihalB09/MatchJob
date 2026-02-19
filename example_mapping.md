# Example Mapping — MatchJob

## Story

> As a **candidate**, I want to **find job offers that match my skills**, so that I can **focus on the most relevant opportunities**.

---

## Rule 1 — Compatibility (minimum 2 matching skills)

> A job offer is compatible if the candidate has **at least 2** required skills from the offer. Otherwise, the offer is ignored completely.

### Example 1.1 — Offer with exactly 2 matching skills is compatible

```
Given candidate skills are ['python', 'sql', 'git']
And offer "Backend Junior" requires ['python', 'git', 'docker']
When I check compatibility
Then "Backend Junior" is compatible (2 matching skills: python, git)
```

### Example 1.2 — Offer with only 1 matching skill is not compatible

```
Given candidate skills are ['python', 'sql', 'git']
And offer "Data Intern" requires ['sql', 'excel']
When I check compatibility
Then "Data Intern" is not compatible (only 1 matching skill: sql)
```

### Example 1.3 — Offer with 0 matching skills is not compatible

```
Given candidate skills are ['python', 'sql', 'git']
And offer "Designer" requires ['figma', 'photoshop']
When I check compatibility
Then "Designer" is not compatible (0 matching skills)
```

### Example 1.4 — Offer where all skills match is compatible

```
Given candidate skills are ['python', 'sql', 'git']
And offer "Perfect Match" requires ['python', 'sql', 'git']
When I check compatibility
Then "Perfect Match" is compatible (3 matching skills: python, sql, git)
```

### Example 1.5 — Candidate has empty skill list

```
Given candidate skills are []
And offer "Backend Junior" requires ['python', 'git', 'docker']
When I check compatibility
Then "Backend Junior" is not compatible (0 matching skills)
```

---

## Rule 2 — Score (number of common skills)

> The score equals the **number of skills in common** between the candidate and the offer.

### Example 2.1 — Score is 2 when 2 skills match

```
Given candidate skills are ['python', 'sql', 'git']
And offer "Backend Junior" requires ['python', 'git', 'docker']
When I compute the score
Then the score is 2 (common skills: python, git)
```

### Example 2.2 — Score is 3 when all candidate skills match

```
Given candidate skills are ['python', 'sql', 'git']
And offer "Perfect Match" requires ['python', 'sql', 'git', 'docker']
When I compute the score
Then the score is 3 (common skills: python, sql, git)
```

### Example 2.3 — Score is 0 when no skills match

```
Given candidate skills are ['python', 'sql', 'git']
And offer "Designer" requires ['figma', 'photoshop']
When I compute the score
Then the score is 0
```

### Example 2.4 — Duplicate skills in candidate list do not inflate score

```
Given candidate skills are ['python', 'python', 'sql']
And offer "Backend" requires ['python', 'sql', 'docker']
When I compute the score
Then the score is 2 (common skills: python, sql — duplicates not counted twice)
```

---

## Rule 3 — Sorting (score desc, then alphabetical title)

> Sort compatible offers by **highest score first**. If scores are equal, sort by **alphabetical order of job title**.

### Example 3.1 — Higher score comes first

```
Given compatible offers are:
  - "Fullstack" with score 3
  - "Backend Junior" with score 2
When I sort the offers
Then the order is: Fullstack, Backend Junior
```

### Example 3.2 — Same score, alphabetical title breaks tie

```
Given compatible offers are:
  - "Fullstack" with score 2
  - "Backend Junior" with score 2
When I sort the offers
Then the order is: Backend Junior, Fullstack (B before F alphabetically)
```

### Example 3.3 — Multiple score groups sorted correctly

```
Given compatible offers are:
  - "Zebra Dev" with score 2
  - "Alpha Dev" with score 3
  - "Beta Dev" with score 2
  - "Gamma Dev" with score 4
When I sort the offers
Then the order is: Gamma Dev (4), Alpha Dev (3), Beta Dev (2), Zebra Dev (2)
```

### Example 3.4 — Single compatible offer

```
Given compatible offers are:
  - "Backend Junior" with score 2
When I sort the offers
Then the result is: Backend Junior (trivially sorted)
```

---

## Rule 4 — Output (display title, score, matching skills)

> For each compatible offer, display: **job title**, **score**, and **list of matching skills**.

### Example 4.1 — Standard output with PDF example data

```
Given candidate skills are ['python', 'sql', 'git']
And offers are:
  - "Backend Junior" requires ['python', 'git', 'docker']
  - "Data Intern" requires ['sql', 'excel']
  - "Fullstack" requires ['python', 'sql', 'react']
When I run the matching algorithm
Then the output is:
  Backend Junior – score 2 – python, git
  Fullstack – score 2 – python, sql
```

### Example 4.2 — No compatible offers produces empty output

```
Given candidate skills are ['rust', 'haskell']
And offers are:
  - "Backend Junior" requires ['python', 'git', 'docker']
  - "Data Intern" requires ['sql', 'excel']
When I run the matching algorithm
Then the output is empty (no compatible offers)
```

### Example 4.3 — No offers at all

```
Given candidate skills are ['python', 'sql', 'git']
And offers list is empty
When I run the matching algorithm
Then the output is empty
```

### Example 4.4 — All offers are compatible

```
Given candidate skills are ['python', 'sql', 'git', 'docker', 'react']
And offers are:
  - "Backend Junior" requires ['python', 'git', 'docker']
  - "Fullstack" requires ['python', 'sql', 'react']
When I run the matching algorithm
Then the output is:
  Backend Junior – score 3 – python, git, docker
  Fullstack – score 3 – python, sql, react
```

---

## Rule 5 (Bonus) — TOP 3 offers only

> Return only the **top 3** compatible offers after sorting.

### Example 5.1 — More than 3 compatible offers, only top 3 returned

```
Given candidate skills are ['python', 'sql', 'git', 'docker']
And there are 5 compatible offers sorted as:
  1. "Alpha" with score 4
  2. "Beta" with score 3
  3. "Gamma" with score 3
  4. "Delta" with score 2
  5. "Epsilon" with score 2
When I apply the TOP 3 rule
Then only Alpha, Beta, Gamma are returned
```

### Example 5.2 — Exactly 3 compatible offers, all returned

```
Given there are 3 compatible offers sorted as:
  1. "Alpha" with score 4
  2. "Beta" with score 3
  3. "Gamma" with score 2
When I apply the TOP 3 rule
Then all 3 are returned: Alpha, Beta, Gamma
```

### Example 5.3 — Fewer than 3 compatible offers, all returned

```
Given there are 2 compatible offers sorted as:
  1. "Alpha" with score 4
  2. "Beta" with score 2
When I apply the TOP 3 rule
Then both are returned: Alpha, Beta
```

### Example 5.4 — Zero compatible offers

```
Given there are 0 compatible offers
When I apply the TOP 3 rule
Then the result is empty
```

---

## Rule 6 (Bonus) — Case insensitivity

> Skill comparison ignores case: `'Python'` and `'python'` are treated as the **same skill**.

### Example 6.1 — Mixed case still matches

```
Given candidate skills are ['Python', 'SQL', 'git']
And offer "Backend" requires ['python', 'sql', 'docker']
When I check compatibility
Then "Backend" is compatible (2 matching skills: python, sql)
And the score is 2
```

### Example 6.2 — All-uppercase candidate vs all-lowercase offer

```
Given candidate skills are ['PYTHON', 'GIT']
And offer "DevOps" requires ['python', 'git', 'docker']
When I check compatibility
Then "DevOps" is compatible (2 matching skills: python, git)
```

### Example 6.3 — Mixed case in both lists

```
Given candidate skills are ['PyThOn', 'Sql']
And offer "Backend" requires ['PYTHON', 'sql', 'docker']
When I check compatibility
Then "Backend" is compatible (2 matching skills: python, sql)
```

---

## Rule 7 (Bonus) — Bonus skill list with extra points

> The candidate has a separate **bonus skill list**. When an offer's required skill matches a bonus skill, it adds **extra points** on top of the base score.

### Example 7.1 — Bonus skills add to base score

```
Given candidate skills are ['python', 'sql', 'git']
And candidate bonus skills are ['docker', 'kubernetes']
And offer "DevOps" requires ['python', 'git', 'docker']
When I compute the score
Then base score is 2 (python, git)
And bonus points is 1 (docker)
And total score is 3
```

### Example 7.2 — No bonus skills match, score unchanged

```
Given candidate skills are ['python', 'sql', 'git']
And candidate bonus skills are ['rust', 'haskell']
And offer "Backend" requires ['python', 'git', 'docker']
When I compute the score
Then base score is 2 (python, git)
And bonus points is 0
And total score is 2
```

### Example 7.3 — Bonus skills alone do not make an offer compatible

```
Given candidate skills are ['rust']
And candidate bonus skills are ['python', 'git']
And offer "Backend" requires ['python', 'git', 'docker']
When I check compatibility
Then "Backend" is not compatible (only 0 base matching skills from candidate main list)
```

### Example 7.4 — Empty bonus skill list

```
Given candidate skills are ['python', 'sql', 'git']
And candidate bonus skills are []
And offer "Backend" requires ['python', 'git', 'docker']
When I compute the score
Then base score is 2 (python, git)
And bonus points is 0
And total score is 2
```

---

## Rule 8 (Bonus) — Location filter

> Offers have a **location**. If the candidate specifies a **preferred location**, offers that don't match that location are excluded before any other processing.

### Example 8.1 — Matching location, offer kept

```
Given candidate preferred location is "Paris"
And offer "Backend" is located in "Paris" and requires ['python', 'git', 'docker']
And candidate skills are ['python', 'git']
When I run the matching algorithm
Then "Backend" is kept (location matches) and evaluated for compatibility
```

### Example 8.2 — Non-matching location, offer excluded

```
Given candidate preferred location is "Paris"
And offer "Backend" is located in "Lyon" and requires ['python', 'git', 'docker']
And candidate skills are ['python', 'git']
When I run the matching algorithm
Then "Backend" is excluded (location does not match), regardless of skill compatibility
```

### Example 8.3 — Candidate has no preferred location, all offers kept

```
Given candidate has no preferred location
And offers are:
  - "Backend Paris" located in "Paris" requires ['python', 'git']
  - "Backend Lyon" located in "Lyon" requires ['python', 'sql']
And candidate skills are ['python', 'git', 'sql']
When I run the matching algorithm
Then both offers are evaluated for compatibility (no location filter applied)
```

### Example 8.4 — All offers excluded by location, empty result

```
Given candidate preferred location is "Paris"
And offers are:
  - "Backend Lyon" located in "Lyon" requires ['python', 'git']
  - "Backend Marseille" located in "Marseille" requires ['python', 'sql']
And candidate skills are ['python', 'git', 'sql']
When I run the matching algorithm
Then the output is empty (all offers excluded by location)
```

---

## Questions (open ambiguities)

| # | Question |
|---|----------|
| Q1 | **Duplicate skills in offer list**: If an offer lists `['python', 'python', 'git']`, should duplicates be deduplicated before matching? |
| Q2 | **Bonus skill overlap**: Can a skill appear in both the candidate's main skill list and bonus skill list? If so, does it count for both base score and bonus points? |
| Q3 | **Bonus compatibility**: Should bonus skill matches count toward the compatibility threshold of 2, or only toward the score? (Example 7.3 assumes they do NOT count toward compatibility.) |
| Q4 | **Location case sensitivity**: Should location comparison be case-insensitive (e.g., "paris" vs "Paris")? |
| Q5 | **Partial location match**: Should "Paris 15e" match "Paris", or must locations be exact strings? |
| Q6 | **TOP 3 tie-breaking at boundary**: If offers ranked 3rd and 4th have the same score and adjacent alphabetical titles, which one gets the 3rd slot? (Assumed: strict alphabetical.) |
| Q7 | **Matching skills display order**: Should matching skills in the output be listed in candidate order, offer order, or alphabetical order? |
| Q8 | **Empty candidate skill list**: Is this a valid input, or should it produce an error/warning? |
