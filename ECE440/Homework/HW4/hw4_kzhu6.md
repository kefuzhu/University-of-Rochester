# ECE HW#4 Kefu Zhu

## Question 7

### (A)

**Is the process XN a MC?**

The process $X_n$ is a Markov chain because we can write 
$
\begin{cases}
X_{n+1} = 0,\ X_n = 0 \\
X_{n+1} = \sum_{i=1}^{X_n} D_i,\ X_n > 0 \\
\end{cases}
$ 

which indicate that the number of women in the $n+1$ generation only depends on the number of women in the $n$ generation $\Leftrightarrow$ memory less property of markov chain.

**What are the transition probabilities $P(X_{n+1} = j|X_n = 0)$ and $P(X_{n+1} = j|X_n = 1) $?**

Because once the total number of women becomes zero at some point in time, the number will stay as zero and won't increase in the future. We have

$P_{0j}=P(X_{n+1} = j|X_n = 0) =
\begin{cases}
0,\ j \ne 0 \\
1,\ j = 0 \\
\end{cases}
$

As stated before, because $X_n$ is a Markov chain, we can write

$P_{1j}=P(X_{n+1} = j|X_n = 1) = P(\sum_{i=1}^{X_n} D_i = j|X_n = 1) = P(D_i=j) = p_j$

**What are the transition probabilities into state $Xn = 0$?**

The probability of the number of women becomes zero at some point given there are still $i$ women in the last generation is equivalent to the probability that every woman has no daughter, which can be represented as

$P(X_{n+1} = 0 | X_n = i) = \prod_{k=1}^i P(D_k = 0) = p_0^i$

**Is the probability $P(X_{n+1} = i|X_n = i)$ of a state transitioning into itself strictly positive? Isthis MC recurrent?**

As stated before, $P(X_{n+1} = i|X_n = i) = 1$, for $i = 0$

For $i>0$, we know that one way of having the same number of women for two generations in a row is that every woman has exactly one daughter, with probability $p_1^i$. Therefore, we have

$P(X_{n+1} = i|X_n = i) \ge p_1^i > 0$, for $i > 0$

Since $P(X_{n+1} = 0|X_n = 0) = 1$, the state $0$ is recurrent. Because $\forall i \ne 0, p_0^i > 0$, all states that is not state $0$ are transient (Because there is a probability that state $i$ goest to state $0$ and then stays there forever $\rightarrow$ never come back to state $i$).

The MC is not recurrent.

### (B)

**Is $X_{rN}$ not a MC?**

For the special case, state $0$, which means that there are no women of type $r$ in the current generation, can happens because of two scenarios

1. Type $r$ has not been created so far $\rightarrow P(X_{rm} > 0| X_{rn}=0)=0$ 
2. Type $r$ existed in the past but is now extinct $\rightarrow P(X_{rm}) > 0$

Since the transition probabilities to other states starting from state $0$ depend on the past scenarios, this process must not be a Markov chain

**Given $X_{rn} > 0$, is the process $X_{r,n:\infty} = X_{rn}, X_{r,n+1},...$ a MC?**

Because we are conditioning on $X_{rn} > 0$, we eliminate the other scenario for the state $0$. The process now is a Markov chain. Now we have

$P_{0j} = 
\begin{cases}
1,\ j = 0\\
0,\ j \ne 0\\
\end{cases}
$

$P_{1j} = (1-q)p_j$, which indicate the probability of having exactly $j$ daughters without the mutation

**What is the value for $P_{i0}$?**

Consider one scenario of $P_{i0}$,

$P_{10} = p_0 + (1-p_0)q$ because the number of women who has the mutation becomes extinct if one of the following two mutually exclusive scenarios happens:

1. woman has no daughters
2. woman has daughters but her daughters has type $r$

Because of independence, $P_{i0} = P_{10}^i = (p_0 + (1-p_0)q)^i,\ i \ge 0$

**Is $P_{ii} > 0$? Is this MC recurrent**

Same logic as stated in part A, only state $0$ is recurrent. All other states are transient.

$P_{ii} \ge ((1-q)p_i)^i > 0,\ i \ge 0$

The MC is not recurrent

### (C)

```matlab
% Set simulation parameter
X_o = 100;
max_t = 50;
max_types = 1000; 

% Set stochastic process parameters
mu = 1.05;
q = 10^-2;
% Initialize empty matrix with all zeros for storing population size
X=zeros(max_types, max_t);
% Initialize empty matrix with all zeros for storing number of types
number_of_types=zeros(1, max_t);
% Initialize population (1 people)
X(1:X_o,1) = 1;
% Initialize first generation
number_of_types(1)=X_o; 
number_of_extinct_types=zeros(1,max_t);

% Start simulation
for n=2:max_t
    disp('n = '+string(n))
    number_of_types(n)=number_of_types(n-1);
    for type = 1:number_of_types(n-1);
        for i = 1:X(type,n-1)
            % Daughter/Not Daughter
            daughters = poissrnd(mu,1,1); 
            % Mutation/No mutation
            mutation = binornd(1,q,1,1);
            
            % If there is a mutation
            if mutation
                number_of_types(n) = number_of_types(n)+1;
                X(number_of_types(n),n) = daughters;
            % Otherwise
            else
                X(type,n) = X(type,n) + daughters;
            end
        end
        
        % Add the extinct type
        if X(type,n)== 0
            number_of_extinct_types(n)=number_of_extinct_types(n)+1;
        end
    end
end
```

```
# The total number of mitochondrial DNA types by generation n
number_of_types

# The total number of extinct types by generation n
number_of_extinct
```