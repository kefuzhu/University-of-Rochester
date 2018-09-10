function [w, t, broke] = casino(w_0, bet, p, max_t)

    % Starting time
    t = 1;
    % Boolean to indicate broke or not
    broke = 0; 
    % Wealth starts with w_0
    w(t) = w_0;
    while ( (w(t)>0) && (t<max_t) )
       % Random outcome of this bet (win or lose with probablity of p for winning)
       x = random('bino', 1, p);

       % If win, add wealth by amount of bet
       if (x==1)                     
           w(t+1) = w(t) + bet;
       % If lose, substract wealth by amount of bet
       else 
           w(t+1) = w(t) - bet;
       end
       % Increment the time counter
       t = t + 1;
    end

    % If the while loop ends before reaching the maximum play time,
    % the person must be broke
    if t < max_t
        % Change the broke to 1
        broke = 1;  
    end
end