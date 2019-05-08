# Lecture 13, Wednesday, 03/20

### Topics: 
- Expectation Maximization (EM)
	- unsupervised learning

**Notation**:

- features: $x$
- label: $y$
- hidden label/cluster: $z$

## Mixture of Gaussian

$N(X^{(n)}; \mu_k; \Sigma_k) = \frac{1}{Z} \cdot e^{\frac{1}{2}(X^{(n)} - \mu_k)^T \Sigma_k^{-1} (X^{(n)} - \mu_k)}$

$P(X^{(n)}; \lambda_k; \mu_k; \Sigma) = \sum_{k=1}^K \lambda_k \cdot N(X^{(n)}; \mu_k; \Sigma_k)$

Where

- $\lambda_k$ = prior/weight
- $\mu_k$ = mean of cluster $k$
- $\Sigma_k$ = covariance of cluster $k$

For a data point $X^{(n)}$, $Z^{(n)} \in \{1,2,...,K\}$

We want to know

<center>
$P(X^{(n)}, Z^{(n)}) = P(Z^{(n)}) \cdot P(X^{(n)}|Z^{(n)})$
</center>

```
# Sudo-code

```
