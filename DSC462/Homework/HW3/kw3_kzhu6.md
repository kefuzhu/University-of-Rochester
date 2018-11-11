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


<center>

| Test\Infection |  T  |  F  |
|:--------------:|:---:|:---:|
|        T       | 401 |  12 |
|        F       |  24 | 753 |

</center>

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
<center>
![graph](https://github.com/datamasterkfz/University-of-Rochester/raw/master/DSC462/Homework/HW3/plot.png)
</center>

### (c)

PPV = $\frac{401}{401+12} \approx 97.09\%$

NPV = $\frac{753}{753+24} \approx 96.91\%$

prev = $\frac{401+24}{1190} \approx 35.71\%$

PPV is higher than any PPV in part (b), NPV is lower than any NPV in part (b)

### (d)

LR (Test Positive) = $\frac{P(Positive|Infection)}{P(Positive|	Not\ Infected)} = \frac{401/(401+24)}{12/(12+753)} \approx 60.15$

LR (Test Negative) = $\frac{P(Negative|Infection)}{P(Negative|	Not\ Infected)} = \frac{24/(401+24)}{753/(12+753)} \approx 0.06$

$\therefore$ 

$Odds(Infection|Test\ Positive) = 60.15\ \times\ Odds(Infection)$

$Odds(Infection|Test\ Negative) = 0.06\ \times\ Odds(Infection)$

## Question 3

### (a)

$P(O_+|T_+) = \frac{P(T_+|O_+)P(O_+)}{P(T_+|O_+)P(O_+)\ +\ P(T_+|O_-)P(O_-)} = \frac{sens\ \times\ prev}{sens\ \times\ prev\ +\ (1-spec)(1-prev)}$

$P(O_+|T_-) = \frac{P(T_-|O_+)P(O_+)}{P(T_-|O_+)P(O_+)\ +\ P(T_-|O_-)P(O_-)} = \frac{(1-sens)\ \times\ prev}{(1-sens)prev\ +\ spec(1-prev)}$

$\Delta = P(O_+|T_+) - P(O_+|T_-)$ depends on $prev$ since it cannot be reduced from the result

As $prev \rightarrow 0, \Delta = 0-0 = 0$

As $prev \rightarrow 1, \Delta = 1-1 = 0$

### (b)

RR = $\frac{P(O_+|T_+)}{P(O_+|T_-)} = \frac{sens\ \times\ prev}{sens\ \times\ prev\ +\ (1-spec)(1-prev)} \cdot \frac{(1-sens)prev\ +\ spec(1-prev)}{(1-sens)prev}$ 

$= \frac{sens}{sens\ \times\ prev\ +\ (1-spec)(1-prev)} \cdot \frac{(1-sens)prev\ +\ spec(1-prev)}{(1-sens)}$

RR also depends on $prev$ since it cannot be reduced from the result

As $prev \rightarrow 0, RR = \frac{sens\ \times\ spec}{(1-spec)(1-sens)}$

As $prev \rightarrow 1, RR = 1$

### (c)

OR = $\frac{Odds(O_+|T_+)}{Odds(O+|T_-)} = \frac{P(O_+|T_+)}{1-P(O_+|T_-)} \cdot  \frac{1-P(O_+|T_-)}{P(O_+|T_-)} = \frac{sens\ \times\ spec}{(1-sens)(1-spec)}$, which does not depend on $prev$