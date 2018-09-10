% Clean up workspace. 
close all 
clear     
% Initialize parameters
w_0 = 100;   
b = 1;      
p = 0.4;   
max_t=1000;
% Number of experiments for each p
experiments = 1000;
% List to capture result from each experiment
T0 = [];

for experiment = 1:experiments
    [w, t, broke] = casino(w_0, b, p, max_t);
    T0(end+1) = t;
end

% Show the plot
histogram(T0,'Normalization','probability')
title('Distribution of T0 (w0 = 50, max_t = 1000)')
ylabel('Frequency')
xlabel('T0')

