# Lecture 5, Monday, 02/04

### Topics: 
- Support Vector Machine
- kernel methods

##???

For non-linearly separable dataset, define

$
\xi_{x_i} =
\begin{cases}
0,\ \mathrm{if\ data\ point\ is\ on\ the\ correct\ side} \\
\xi_{x_i},\ \mathrm{if\ data\ point\ is\ on\ the\ incorrect\ side}
\end{cases}
$

where $\xi_{x_i}$ is the distance from the margin

$\min_{w,b,\xi} \frac{1}{2} ||w||^2 + C \cdot \sum_n \xi_n$ such that $y_n(W^TX^{(n)} + b) \ge 1 - \xi_n \Rightarrow \xi_n \ge 1 - y_n(W^TX^{(n)} + b)$

- $\xi_n = $ slack variable
- $C = $ capacity

Because $\xi_n \ge 0$ for any $n$, $\xi_n = \max\{0, 1 - y_n(W^TX^{(n)} + b)\}$ 

---
<center>
$\min_{w,b} \frac{1}{2} ||w||^2 + C \cdot \sum_n \max\{0, 1 - y_n(W^TX^{(n)} + b)\}$
</center>

$f_n(w,b) = C \cdot  \max\{0, 1 - y_n(W^TX^{(n)} + b)\} + \frac{1}{2N} ||w||^2$

$\frac{\partial f_n}{\partial w} = 
\begin{cases}
- C \cdot y_n X^{(n)} + \frac{1}{2N} \cdot w,\ \mathrm{if}\ 1-y_n(W^TX^{(n)}+b) > 0 \\
\frac{1}{2N} \cdot w,\ \mathrm{otherwise}
\end{cases}
$

$\frac{f_n}{b} =
\begin{cases}
-C \cdot y_n,\ \mathrm{if}\ 1-y_n(W^TX^{(n)}+b) > 0 \\
0,\ \mathrm{otherwise}
\end{cases}
$


**SGD for SVM**

```
Repeat
	For n from 1 to N
		if 1−yn(WTX(n)+b) > C
			w = w + α⋅C⋅ynX(n)
			b = b + α⋅C⋅yn
		w = w - (α⋅w)/2N
```

---

Logistic Regression 
$
\begin{cases}
\mathrm{sigmoid\ function} \rightarrow \mathrm{not\ convex}\\
-log(\mathrm{sigmoid\ function}) \rightarrow \mathrm{convex}
\end{cases}
$

SVM $\rightarrow$ convex

<center>
<img src="graphs/log-sigmoid.png" style="max-width:70%">
</center>