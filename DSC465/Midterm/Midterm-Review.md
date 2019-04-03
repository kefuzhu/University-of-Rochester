# DSC 465 Midterm Review

## Topics

[Chapter 1: ANOVA](#anova)  
[Chapter 2,3,5: Linear Regression](#linear-regression)  
[Chapter 8: Bayesian Inference](#bayes)  
[Chapter 9: Survival Analysis](#survival)  
[Chapter 13.1-13.9: Classification](#classification)  

## <a name='anova'></a> ANOVA

Given a total of $n$ samples from $k$ different groups, where $n = n_1 + n_2 + ... n_k$

A **balanced design** refers to the situation where the sample sizes for all groups are equal ($n_1 = n_2 = ... = n_k$)

- **SST/SS(B)** $= \sum_{i=1}^k n_i(\bar{y_i} - \bar{y})^2$ 
- **SSE/SS(W)** $= \sum_{i=1}^k \sum_{j=1}^{n_i} (y_{ij} - \bar{y_i})^2$
- **SSTO/SS(T)** $= \sum_{i=1}^k \sum_{j=1}^{n_i} (y_{ij} - \bar{y})^2$

The total variation of the dataset (SSTO/SS(T)) is the sum of 

- Variation between groups (SST/SS(B))
- Vartation within group (SSE/SS(W))

<center>
$SSTO = SST + SSE$
</center>

The test statistics for ANOVA is

<center>
$F_{obs} = \frac{SST/(k-1)}{SSE/(n-k)}$
</center>

We reject the null hypothesis (no significant differences between groups) if the observed significance level, $\alpha_{obs}$, is greater then some threshold (usually uses $0.05$ as the cutoff)

<center>
$\alpha_{obs} = P(F_{k-1,n-k} > F_{obs})$
</center>

**ANOVA Table**

<img src='graphs/ANOVA-Table.png'; width=70%>

**Note:** ANOVA assumes that each sample comes from a population with possibly differing means, but with one common variance $\sigma^2$. It can be shown that $MSE$ is an estimator of $\sigma^2$. When $k=2$, $MSE$ is identitcal to the pooled sample variance $S_p^2$

### Bonferroni Correction

**Background**: When we report several confidence intervals together, each with a confidence level $(1-\alpha)$, we must consider the fact that the probability of at least one error exists among all inference statements will be greater than $\alpha$

Suppose we wish to report $m$ confidence intervals with confidence level of $(1-\alpha)$, recall Boole's inequality

<center>
$P(\cup_{i=1}^m E_i) \le \sum_{i=1}^m P(E_i)$
</center>

If we denote $E_i =$ $\{$the $i$th confidence interval is incorrect$\}$, then $P(E_i) = \alpha$ and we have

<center>
$P(\cup_{i=1}^m E_i) \le m\alpha$
</center>

## <a name='linear-regression'></a> Linear Regression

## <a name='bayes'></a> Bayesian Inference

## <a name='survival'></a> Survival Analysis

## <a name='classification'></a> Classification