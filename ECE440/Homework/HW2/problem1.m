% pmf
x = [0 1];
p = [1/2 1/2];

% Plot for pmf
bar(x,p)
ylim([0,1.5]);ylabel("Probability");xlabel("X");title("pmf Plot of X");

% Generate figure in new window
figure
% cdf           
X = [-2,-1,0,1,2];
F = [0,0,0.5,1,1];
stairs(X, F)
ylim([0,1.5]);ylabel("Cumulative Probability");xlabel("X");title("cdf Plot of X");

