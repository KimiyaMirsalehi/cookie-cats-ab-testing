# Cookie Cats — A/B Testing Experiment Design

## 1. Business Context

Cookie Cats is a mobile puzzle game in which players progress through
levels and encounter gates that temporarily restrict further progress.

The development team conducted an A/B experiment to evaluate the impact
of moving the first gate from level 30 to level 40.

The experiment compares two versions of the game:

| Group | Description |
|-------|-------------|
| Control (gate_30) | Players encounter the first gate at level 30. |
| Treatment (gate_40) | Players encounter the first gate at level 40. |

## 2. Business Problem

The placement of progression gates may influence player engagement
and retention.

Moving the first gate to a later level could allow players to progress
further before encountering an interruption.

However, the change could also affect the gameplay experience and
players' willingness to return.

The company therefore needs to determine whether moving the first gate
from level 30 to level 40 produces a meaningful improvement in player
retention.

## 3. Business Objective

Evaluate the effect of moving the first progression gate from level 30
to level 40 on player retention and engagement.

The analysis will aim to:

1. Compare player retention between the control and treatment groups.
2. Estimate the magnitude and uncertainty of observed differences.
3. Investigate whether player engagement differs between groups.
4. Assess whether the available evidence supports implementing the
   proposed change.

## 4. Key Business Question

**Should the company move the first progression gate from level 30
to level 40?**

The recommendation will consider statistical evidence, the magnitude
of observed effects, and limitations of the available data.

## 5. Experiment Metrics

### 5.1 Primary Metric — Day 7 Retention

Day 7 retention measures the proportion of players who returned
to the game seven days after installation.

Day 7 Retention = Players retained on Day 7 / Total players

The primary objective is to determine whether moving the first
gate from Level 30 to Level 40 improves Day 7 retention.

### 5.2 Secondary Metrics

The following metrics will provide additional context:

- Day 1 Retention: Percentage of players returning one day
  after installation.
- Game Rounds: Total rounds played per user during the first
  14 days.

Secondary metrics will be analysed to understand potential
trade-offs, but they will not replace the primary decision metric.

## 6. Statistical Hypotheses

Let:

- p30 = Day 7 retention probability for Gate 30.
- p40 = Day 7 retention probability for Gate 40.

Null Hypothesis (H0):

p40 <= p30

Moving the gate to Level 40 does not improve Day 7 retention.

Alternative Hypothesis (H1):

p40 > p30

Moving the gate to Level 40 improves Day 7 retention.

The primary hypothesis will be evaluated using a one-sided
two-proportion statistical test.

## 7. Statistical Significance

The significance level for the primary hypothesis test
is set at:

Alpha = 0.05 (5%)

A p-value below 0.05 will be considered statistically
significant evidence in favour of improved Day 7 retention,
subject to the validity of the experiment and test assumptions.

Statistical significance alone will not determine the
final business recommendation.

Effect sizes, confidence intervals, secondary metrics,
and data limitations will also be considered.

## 8. Experiment Integrity

The analysis assumes an intended 50/50 allocation between
the control and treatment groups.

A chi-square goodness-of-fit test produced:

- Chi-square statistic: 6.9024
- P-value: 0.008608
- SRM significance threshold: 0.001

No sample ratio mismatch was detected at the predefined
0.1% significance threshold.

However, the result is significant at the 5% level.
The intended allocation and randomisation implementation
cannot be independently verified from the available dataset.

This limitation will be considered when interpreting
the experiment results.

## 9. Primary A/B Test Results

### 9.1 Experiment Summary

The experiment compared Day 7 retention between two groups:

| Metric | Gate 30 (Control) | Gate 40 (Treatment) |
|--------|-------------------|---------------------|
| Players | 44,700 | 45,489 |
| Day 7 retained players | 8,502 | 8,279 |
| Day 7 retention | 19.02% | 18.20% |

The observed treatment effect (Gate 40 minus Gate 30) was
-0.820 percentage points, representing a relative decrease
of approximately 4.31%.

### 9.2 Primary Hypothesis Test

A one-sided two-proportion Z-test was conducted to evaluate
whether Gate 40 improves Day 7 retention.

- Null hypothesis: p40 <= p30
- Alternative hypothesis: p40 > p30
- Significance level: 0.05
- Z-statistic: -3.164359
- P-value: 0.999223

The primary test failed to reject the null hypothesis.

There is insufficient statistical evidence that moving the
first progression gate from Level 30 to Level 40 improves
Day 7 retention.

### 9.3 Supplementary Two-Sided Analysis

A supplementary two-sided Z-test was conducted to investigate
whether retention rates differ between the experimental groups.

- Z-statistic: -3.164359
- P-value: 0.001554
- Significance level: 0.05

The two-sided test identified a statistically significant
difference between the groups.

The observed difference was negative, indicating lower
Day 7 retention among players assigned to Gate 40.

### 9.4 Confidence Interval

The 95% Newcombe confidence interval for the difference in
Day 7 retention (Gate 40 minus Gate 30) was:

[-1.328, -0.312] percentage points.

The confidence interval lies entirely below zero and is
consistent with lower Day 7 retention under Gate 40.

### 9.5 Preliminary Business Recommendation

Based on the available evidence, the proposed change from
Gate 30 to Gate 40 should not be rolled out at this stage.

The primary test did not demonstrate an improvement in
Day 7 retention, while supplementary analysis identified
a statistically significant negative difference.

However, the recommendation remains conditional on the
validity of the experiment's randomisation and tracking.

The sample ratio mismatch assessment produced a p-value
of 0.008608, which did not cross the predefined 0.001
threshold but warrants caution.

Additionally, the dataset does not contain revenue or
monetisation information, preventing an assessment of
the change's overall financial impact.

## 10. Secondary Metric — Day 1 Retention

### 10.1 Objective

Day 1 retention was analysed as a secondary metric to
investigate whether moving the first progression gate
affects early player retention.

This analysis is exploratory and does not replace
the predefined primary Day 7 retention test.

### 10.2 Results

| Metric | Gate 30 | Gate 40 |
|--------|---------|---------|
| Total players | 44,700 | 45,489 |
| Day 1 retained players | 20,034 | 20,119 |
| Day 1 retention | 44.82% | 44.23% |

The observed difference in Day 1 retention
(Gate 40 minus Gate 30) was:

- Absolute difference: -0.591 percentage points
- Relative difference: -1.32%

### 10.3 Statistical Test

A supplementary two-sided two-proportion Z-test was
performed.

- Z-statistic: -1.784086
- P-value: 0.074410
- Significance level: 0.05

The difference was not statistically significant
at the 5% significance level.

### 10.4 Confidence Interval

The 95% Newcombe confidence interval for the
difference in retention was:

[-1.239, +0.058] percentage points.

Since the confidence interval includes zero,
the data do not provide sufficient evidence
of a difference in Day 1 retention.

### 10.5 Interpretation

Both Day 1 and Day 7 retention were descriptively
lower for players assigned to Gate 40.

However, only the supplementary Day 7 comparison
was statistically significant at the 5% level.

The results do not establish that the treatment
effect becomes stronger over time.

Because Day 1 retention is a secondary metric,
its results should be interpreted as exploratory.

The overall recommendation continues to prioritise
the predefined Day 7 retention objective.

## 11. Secondary Metric — Player Engagement

### 11.1 Objective

Player engagement was evaluated using the total number
of game rounds completed during the first 14 days.

The analysis aimed to determine whether moving the first
gate from Level 30 to Level 40 affected gameplay activity.

Engagement was treated as a secondary, exploratory metric.

### 11.2 Descriptive Results

| Metric | Gate 30 | Gate 40 |
|--------|---------|---------|
| Players | 44,700 | 45,489 |
| Mean game rounds | 52.46 | 51.30 |
| Median game rounds | 17 | 16 |
| Maximum game rounds | 49,854 | 2,640 |

The observed difference in mean game rounds
(Gate 40 minus Gate 30) was -1.1575 rounds.

### 11.3 Outlier Investigation

The game-round distribution was strongly right-skewed.

One player assigned to Gate 30 completed 49,854 rounds,
substantially exceeding the activity of other players.

A sensitivity analysis excluding only this observation
reduced the difference in mean game rounds from:

- Original difference: -1.1575 rounds
- Sensitivity difference: approximately -0.043 rounds

This demonstrates that the estimated mean engagement
difference is highly sensitive to an extreme observation.

The observation was retained in the primary analysis.
Its exclusion was used only for sensitivity assessment.

### 11.4 Permutation Test

A two-sided permutation test was conducted to investigate
differences in mean game rounds between the groups.

The test used:

- 5,000 permutations
- Fixed experimental group sizes
- Random seed: 42
- Significance level: 0.05

Results:

- Observed mean difference: -1.1575 rounds
- Permutation p-value: 0.468306

The result was not statistically significant at the
5% significance level.

### 11.5 Interpretation

The analysis did not identify statistically significant
evidence of a difference in mean game rounds between
Gate 30 and Gate 40.

However, this does not establish equivalence between
the two experimental groups.

The engagement distribution was highly skewed,
and the mean difference was sensitive to an extreme
observation.

As engagement was a secondary metric, these findings
provide additional context but do not override the
primary Day 7 retention analysis.

### 11.6 Business Implications

The engagement analysis does not demonstrate a clear
advantage from moving the gate to Level 40.

Combined with the retention analysis, the available
evidence does not support implementing the proposed
change at this stage.

The final recommendation remains subject to experiment
integrity, statistical assumptions, and the absence
of monetisation data.