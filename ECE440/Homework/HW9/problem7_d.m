% Set parameters
h=0.01; sigma=1; t_MAX=10;

W_vector=normrnd(0,sigma*sqrt(h),1,t_MAX/h);
X_vector=cumsum(W_vector);

% Plot sample path
plot(h:h:t_MAX,X_vector);
xlabel('time');title('Weiner Process Simulated, h = ' + string(h));
grid on; axis([0 t_MAX -5 5])