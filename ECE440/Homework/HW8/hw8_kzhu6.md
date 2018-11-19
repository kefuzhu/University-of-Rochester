# ECE 440, HW8, Kefu Zhu

## Question 7

### (A)

Because all varialbes are integer based, and the range of $X(t)$ is between $X_{min} = 0$ and $X_{max}$, the states of the CTMC should be any integer between 0 and $X_max$, where $X_{max}$ is nonnegative integer.

### (B)

Because we have

- $T_p$ ~ $exp(\lambda)$
- $T_c$ ~ $exp(\alpha)$
- $T_d$ ~ $exp(\beta)$

Follow the summary from the range table given in the question, it is obvious to show the foloowing $v_x$ for different scenarios


| Range | Possible Events | $v_x$ |
|:-----:|:---------------:|:-----:|
| A | premium | $\lambda$ |
| B | premium, claim paid at $X(t)$ | $\lambda + \alpha$ |
| C | preimum, claim | $\lambda + \alpha$ |
| D | preimum, claim, dividend | $\lambda + \alpha + \beta$ |
| E | claim, dividend | $\lambda + \beta$ |

### (C)

**(1) Possible transition states out of A**:

The only possible transition out of this state is having a payment of premium $\rightarrow$ State 1

**(2) Possible transition states out of B**

- A payment of preimum: $x + 1$
- A claim paid at $X(t)$: $x - x = 0$

**(3) Possible transition states out of C**

- A payment of preimum: $x + 1$
- A payment of claim: $x - c$

**(4) Possible transition states out of D**

- A payment of preimum: $x + 1$
- A payment of claim: $x - c$
- A payment of divident: $x - d$

**(5) Possible transition states out of E**

- A payment of claim: $x - c$
- A payment of divident: $x - d$

### (D)

Since we have alreadly listed all possible transition states for each range, it is easy to compute their transition probabilities given 

- $T_p$ ~ $exp(\lambda)$
- $T_c$ ~ $exp(\alpha)$
- $T_d$ ~ $exp(\beta)$

**(1) Transition probabilites out of A**:

- premium: $\frac{\lambda}{\lambda} = 1$

**(2) Transition probabilites out of B**

- premium: $\frac{\lambda}{\lambda + \alpha}$
- claim: $\frac{\alpha}{\lambda + \alpha}$

**(3) Transition probabilites out of C**

- premium: $\frac{\lambda}{\lambda + \alpha}$
- claim: $\frac{\alpha}{\lambda + \alpha}$

**(4) Transition probabilites out of D**

- premium: $\frac{\lambda}{\lambda + \alpha + \beta}$
- claim: $\frac{\alpha}{\lambda + \alpha + \beta}$
- divident: $\frac{\beta}{\lambda + \alpha + \beta}$

**(5) Transition probabilites out of E**

- claim: $\frac{\alpha}{\alpha + \beta}$
- divident: $\frac{\beta}{\alpha + \beta}$

### (E)

**cashflow.m**

```matlab
function [X,T]=cashflow(X_0,lambda,alpha,beta,c,d,X_r,X_max,T_max)
    index=1;
    X(index)=X_0;
    T(index)=0;
    while T(index)<T_max
        x=X(index);
        if x==0 
            tau=exprnd(1/lambda);
            T(index+1)=T(index)+tau;
            X(index+1)=x+1;
        elseif 0<x && x<c 
            tau=exprnd(1/(lambda+alpha));
            T(index+1)=T(index)+tau;
            u=rand;
            if u<(lambda/(lambda+alpha))
                X(index+1)=x+1;
            else
                X(index+1)=0;
            end
        elseif c<=x && x<X_r
            tau=exprnd(1/(lambda+alpha));
            T(index+1)=T(index)+tau;
            u=rand;
            if u<(lambda/(lambda+alpha))
                X(index+1)=x+1;
            else
                X(index+1)=x-c;
            end
        elseif X_r<=x && x<X_max
            tau=exprnd(1/(lambda+alpha+beta));
            T(index+1)=T(index)+tau;
            u=rand;
            if u<(lambda/(lambda+alpha+beta))
                X(index+1)=X(index)+1;
            elseif u<((lambda+alpha)/(lambda+alpha+beta))
                                X(index+1)=X(index)-c;
            else
                X(index+1)=X(index)-d;
            end
        elseif x==X_max
            tau=exprnd(1/(alpha+beta));
            T(index+1)=T(index)+tau;
            u=rand;
            if u<(alpha/(lambda+alpha))
                X(index+1)=x-c;
            else
                X(index+1)=x-d;
            end
        else
            disp('Out Of Range')
            break 
        end
        index=index+1;
    end
end
```

**Plot** 

```matlab
clc; clear all; close all;

X_0=200;
N=200;
r=0.04;
lambda=N;
alpha=r*N;
beta=4;
X_r=200;
X_max=300;
T_max=5;
d=30;
c=20;

[X,t]=cashflow(X_0,lambda,alpha,beta,c,d,X_r,X_max,T_max);

% Plot
hold on
grid on
xlabel('time')
ylabel('Cash Level')
title('Simulation of Evolution of Cash Level over 5 Years')
axis([0 5 0 310])
stairs(t,X);
```

![Question7_e]()