function [acceptedX,n] = accept_Offer(J,K,L)
    % Create a list of random permutation of numbers from 1 to J
    offer = randperm(J);
    % The first Kth offers are rejected
    rejectOffer = offer(1:K);
    % sort the rejectOffer in ascending order
    rejectOffer_sorted = sort(rejectOffer);
    % Select the L-th best offer
    bestL = rejectOffer_sorted(L);
    for i = K+1:J
        % If found Xi such that Xi < X0, end the loop
        if (offer(i) < bestL)
            % Record the accepted offer Xi and the value of i
            acceptedX = offer(i);
            n = i;
            return;
        end
    end
    % If the loop did not end early, I will accept the last offer J
    acceptedX = offer(J);
    n = J;
end

