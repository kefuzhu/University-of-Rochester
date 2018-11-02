# DSC 462, HW#3, Kefu Zhu

## Question 1

$\because$ $Odds(A|X=x) = \frac{P(X|A)}{P(X|A^c)} \cdot Odds(A)$

$\therefore$ 

$x = 1, Odds(A|X=x)= \frac{0}{4/10} \cdot Odds(A) = 0$ 

$x = 2, Odds(A|X=x)= \frac{1/4}{3/10} \cdot Odds(A) = \frac{5}{6} \cdot Odds(A)$

$x = 3, Odds(A|X=x)= \frac{1/4}{2/10} \cdot Odds(A) = \frac{5}{4} \cdot Odds(A)$

$x = 4, Odds(A|X=x)= \frac{1/4}{1/10} \cdot Odds(A) = \frac{5}{2} \cdot Odds(A)$

$x = 5, Odds(A|X=x)= \frac{1/4}{0} \cdot Odds(A) = \infty$

As $x$ increases, $Odds(A|X=x)$ also increases.

When $x \in {3,4,5}$, the odds that $A$ occurs increases

## Question 2

### (a)

sensitivity = $\frac{401}{401+24} \approx 94.35\%$

specificity = $\frac{753}{753+12} \approx 98.43\%$

### (b)

```r
# The estimation for sensitivity and specificity from part (a)
sens = 0.9435
spec = 0.9843
# The range of prevalence
prev = 0.01*0:20
# Calculate corresponding PPV and NPV for different value of prevalence
PPV = (sens*prev)/(sens*prev + (1-spec)*(1-prev))
NPV = (spec*(1-prev))/(spec*(1-prev) + (1-sens)*prev)

# Plot prevalence vs. PPV
plot(100*prev,PPV,type='l',col='orange', ylim = c(0,1), xlab = 'prevalence (%)', ylab = 'PPV/NPV')
# Add prevalence vs. NPV
lines(100*prev,NPV,type='l',col='blue')
# Add legend
legend('bottomright',legend=c("PPV", "NPV"),col=c("orange", "blue"),lty=1, cex=0.8)
```