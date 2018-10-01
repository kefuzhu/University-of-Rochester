% Plot the pmf of ranks
function [] = pmf_of_rank(J,K,L,N)
    % Initialization
    accepted_rank = zeros(1,N);
    % Record the accepted rank value, the return time N is useless here
    for i=1:N
        [accepted_rank(i), tmp] = accept_Offer(J,K,L);
    end
    
    
    [freq, bin] = hist(accepted_rank,J);
    pmfList=freq/N;
    bar(1:J,pmfList);
    xlabel('x');ylabel('pmf');title('N = ' + string(N) + ', L = ' + string(L)); ylim([0,0.5]);
end