% Clean up workspace. 
close all 
clear     
% Initialize parameters
w0_list = 1:1:20;   
b = 1;      
p = 0.55;   
max_t=100;
% Number of experiments for each p
experiments = 50;
% List to capture result from each experiment
home_prob = [];

figure; hold on; grid on;

% Set axis limit
ylabel ('Probability of Reach Home'); xlabel('w0'); axis([0,20,0,1])
for w_0 = w0_list
    % Number of times reach home
    broke_times = 0;
    % Add more times of experiments
    experiments = experiments + 50;
    % Show progress
    fprintf('w_0 = %d, experiments = %d\n', w_0, experiments)
    for experiment = 1:experiments
        [w, t, broke] = casino(w_0, b, p, max_t);
        broke_times = broke_times + broke;
    end
    home_prob(end+1) = broke_times/experiments;
end
% Show the plot
plot(home_prob)
