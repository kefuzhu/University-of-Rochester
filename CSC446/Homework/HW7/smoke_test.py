#!/usr/bin/env python3
import sys
import os

DATA_DIR = '/u/cs246/data/em/' #TODO: change this to wherever you put the data if working on a different machine
SIGFIG_NUM = 5

def err(msg):
    print('ERROR: {}'.format(msg), file=sys.stderr)
    exit()

def find_filenames():
    return [fn for fn in os.listdir('.') if os.path.isfile(fn) and (fn.endswith('_em_gaussian.py') or fn.endswith('_em_aspect.py'))]

def get_output(filename):
    import subprocess
    cmd = None
    if filename.endswith('_em_gaussian.py'):
        cmd = './{} --nodev --iterations 1 --clusters_file gaussian_smoketest_clusters.txt --data_file {} --print_params'.format(filename, os.path.join(DATA_DIR,'points.dat'))
    else:
        cmd = './{} --nodev --iterations 1 --clusters_file aspect_smoketest_clusters.txt --data_file {} --print_params'.format(filename, os.path.join(DATA_DIR,'pairs.dat'))
    print('Running this command:\n{}'.format(cmd))
    try:
        output = subprocess.check_output(cmd.split()).decode('utf-8')
    except subprocess.CalledProcessError:
        err('Python file did not exit successfully (likely crashed).')
    except OSError as e:
        if e.errno == 13:
            err('Python file is not executable; run this command:\nchmod u+x {}'.format(filename))
        elif e.errno == 8:
            err('Python file does not start with a shebang; put this line at the very top:\n#!/usr/bin/python3')
        elif e.errno == 2:
            err('Unable to execute python file; if you ever edited the file on Windows, it is possible that the line endings are wrong, so try running this command:\ndos2unix {}\nOtherwise, you\'ll have to take a look at it and see what went wrong.'.format(filename))
        else:
            print('Got an OS error not caused by permissions or a shebang problem; you\'ll have to take a look at it and see what the problem is. See below:')
            raise e

    return output

def tokens(s):
    result = []
    for tok in s.split():
        try:
            result.append(float(tok))
        except ValueError as e:
            result.append(tok)
    return result

def round_to_sigfigs(num, sigfigs):
    from math import log10, floor
    if num == 0:
        return num
    else:
        return round(num, -int(floor(log10(abs(num)))) + sigfigs - 1)

def fuzzy_match(line, req):
    line_toks = tokens(line)
    if len(line_toks) != len(req):
        return False
    else:
        for l,r in zip(line_toks, req):
            if type(l) != type(r):
                return False
            elif type(l) == str and l != r:
                return False
            elif type(l) == float and round_to_sigfigs(l,SIGFIG_NUM) != round_to_sigfigs(r,SIGFIG_NUM): #float
                return False
        return True

def verify_gaussian_output(output):
    mode_req = tokens('Gaussian')
    got_mode = False
    ll_req = tokens('Train LL: -4.795391728296074')
    got_ll = False
    lda_req = tokens('Lambdas: 0.40399958634886673 | 0.5960004136511332')
    got_lda = False
    m_req = tokens('Mus: -0.9690057568561202 -1.4283354307408127 | -0.7341326313464455 -0.02772394000092204')
    got_m = False
    s_req = tokens('Sigmas: 1.8377474768519788 0.3727877556397147 0.3727877556397147 6.65242745993941 | 11.765109268523567 -0.643513686769607 -0.643513686769607 5.29925835899086')
    got_s = False

    for line in output.split('\n'):
        if fuzzy_match(line, mode_req):
            print('Choice of Gaussian vs. Aspect is correct!')
            got_mode = True
        elif fuzzy_match(line, ll_req):
            print('Train log-likelihood is correct!')
            got_ll = True
        elif fuzzy_match(line, lda_req):
            print('Lambdas are correct!')
            got_lda = True
        elif fuzzy_match(line, m_req):
            print('Mus are correct!')
            got_m = True
        elif fuzzy_match(line, s_req):
            print('Sigmas are correct!')
            got_s = True
    if not (got_mode and got_ll and got_lda and got_m and got_s):
        err('Unable to find one or more required output lines. Make sure each is on its own line and formatted correctly; if so, then there is an implementation problem. This should have produced (with all numbers matched to {} significant figures):\n{}\n{}\n{}\n{}\n\n'.format(SIGFIG_NUM,' '.join(map(str,ll_req)),' '.join(map(str,lda_req)),' '.join(map(str,m_req)),' '.join(map(str,s_req))))

def verify_aspect_output(output):
    mode_req = tokens('Aspect')
    got_mode = False
    ll_req = tokens('Train LL: -4.494520844361525')
    got_ll = False
    lda_req = tokens('Lambdas: 0.6142948717948742 | 0.385705128205127')
    got_lda = False
    a_req = tokens('Alphas: 0.20800723503426125 0.03615529484255335 0.09405544540679639 0.034530393603752506 0.20619847646874592 0.012750754063495332 0.15193571950328646 0.012532112918213255 0.23332985495147565 0.01050471320741587 | 0.0 0.3601225100311033 0.0 0.2935729718179452 0.0 0.10356371233884977 0.0 0.14136138084949817 0.0 0.10137942496260628')
    got_a = False
    b_req = tokens('Betas: 0.12118682388952612 0.15600542627569594 0.08042018852829635 0.08028105325402597 0.08932484608160254 0.11645622456433231 0.09948172110334244 0.08475325849843195 0.09069632235655374 0.08139413544818923 | 0.1037061658633874 0.11450889147415692 0.0850922386571384 0.08243310619910282 0.08243310619910282 0.15157055010802756 0.1037061658633874 0.08395261046083746 0.08889099931147496 0.1037061658633874')
    got_b = False

    for line in output.split('\n'):
        if fuzzy_match(line, mode_req):
            print('Choice of Gaussian vs. Aspect is correct!')
            got_mode = True
        elif fuzzy_match(line, ll_req):
            print('Train log-likelihood is correct!')
            got_ll = True
        elif fuzzy_match(line, lda_req):
            print('Lambdas are correct!')
            got_lda = True
        elif fuzzy_match(line, a_req):
            print('Alphas are correct!')
            got_m = True
        elif fuzzy_match(line, b_req):
            print('Betas are correct!')
            got_s = True
    if not (got_ll and got_lda and got_m and got_s):
        err('Unable to find one or more required output lines. Make sure each is on its own line and formatted correctly; if so, then there is an implementation problem. This should have produced (with all numbers matched to {} significant figures):\n{}\n{}\n{}\n{}\n\n'.format(SIGFIG_NUM,' '.join(map(str,ll_req)),' '.join(map(str,lda_req)),' '.join(map(str,a_req)),' '.join(map(str,b_req))))

def main():
    filenames = find_filenames()
    if len(filenames) == 0:
        err('No files ending in \'_em_gaussian.py\' or \'_em_aspect.py\' found. Make sure your file is named LastName_em_gaussian.py or LastName_em_aspect.py.')
    if len(filenames) > 1:
        err('Only include a single file ending in \'_em_gaussian.py\' or \'_em_aspect.py\' in the submission directory.')
    print('Found Python file to run.')
    if not os.path.exists(DATA_DIR):
        err('Could not find the data directory; looked for {}. Change the DATA_DIR variable at the top of this smoke test file to wherever you have downloaded the data (points.dat or pairs.dat).'.format(DATA_DIR))
    print('Found data directory.')
    output = get_output(filenames[0])
    print('Ran Python file.')
    if filenames[0].endswith('_em_gaussian.py'):
        verify_gaussian_output(output)
    else:
        verify_aspect_output(output)
    print('Congratulations, you passed this simple test! However, make sure that your code runs AND PASSES THIS TEST on the csug server. Also, don\'t forget your README!')

if __name__ == '__main__':
    main()
