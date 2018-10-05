function []=prob_1_versus_K(J,L)
    N=1000;
    kList = L:J-1;
    prob_of_rank_1 = zeros(1,J-L);
    kIndex = 1;
    for K=kList
        % Initialization
        accepted_rank = zeros(1,N);
        % Record the accepted rank value, the return time N is useless here
        for i=1:N
            [accept_rank(i),tmp] = accept_Offer(J,K,L);
        end
        [freq, bin] = hist(accept_rank,J);
        pmf_vector = freq/N;
        prob_of_rank_1(1,kIndex) = pmf_vector(1,1);
        kIndex = kIndex + 1;
    end
    % Plot histogram
    bar(kList,prob_of_rank_1)
    xlabel('K');ylabel('P(X) = 1');
    title('P(X) = 1 for different K, J = ' + string(J) + ', L = ' + string(L) + ', N = ' + string(N));
    axis([0,J,0,0.5])
end