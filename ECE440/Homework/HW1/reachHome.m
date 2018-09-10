% Clean up workspace. 
close all 
clear     
% Initialize parameters
w_0 = 10;   
b = 1;      
p = 0.55;   
max_t=100;

% figure; hold on; grid on; xlabel('bet index'); 
% 
% % Set axis limit
% ylabel ('w(t)'); xlabel('t'); axis([0,max_t,0,200])

% Number of experiments for each p
experiment_list = 100:300:2500;

for experiments = experiment_list
    % Number of times reach home
    broke_times = 0;
    for experiment = 1:experiments
        [w, t, broke] = casino(w_0, b, p, max_t);
%         plot(w,'b')
        broke_times = broke_times + broke;
    end
    fprintf('Under %d experiments, the probability of reaching home is %.2f\n', experiments, broke_times/experiments)
end



