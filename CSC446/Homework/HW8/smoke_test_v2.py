#!/usr/bin/env python3
import sys
import os

DATA_DIR = '/u/cs246/data/em/' #TODO: change this to wherever you put the data if working on a different machine
DATA_DIR = './'
SIGFIG_NUM = 5

def err(msg):
    print('ERROR: {}'.format(msg), file=sys.stderr) #NOTE: If you get a SyntaxError on this line, you are using Python 2, which is wrong. Use Python 3.
    exit()

def find_filenames():
    return [fn for fn in os.listdir('.') if os.path.isfile(fn) and (fn.endswith('_hmm_gaussian.py') or fn.endswith('_hmm_aspect.py'))]

def get_output(filename):
    import subprocess
    cmd = None
    if filename.endswith('_hmm_gaussian.py'):
        cmd = './{} --nodev --iterations 1 --clusters_file gaussian_hmm_smoketest_clusters.txt --data_file {} --print_params'.format(filename, os.path.join(DATA_DIR,'points.dat'))
    else:
        cmd = './{} --nodev --iterations 1 --clusters_file aspect_hmm_smoketest_clusters.txt --data_file {} --print_params'.format(filename, os.path.join(DATA_DIR,'pairs.dat'))
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

class Req:
    def __init__(self, req, name):
        self.req = tokens(req)
        self.name = name
        self.matched = False

    def check(self,line):
        if fuzzy_match(line, self.req):
            self.matched = True

    def report(self):
        s = '{}: '.format(self.name)
        if self.matched:
            return s + 'Correct!'
        else:
            return s + 'NOT CORRECT!'

    def req_str(self):
        return ' '.join(map(str,self.req))


def verify_reqs(reqs, output):
    for line in output.split('\n'):
        for r in reqs:
            r.check(line)
    for r in reqs:
        print(r.report())
    if not all([r.matched for r in reqs]):
        err('Unable to find one or more required output lines. Make sure each is on its own line and formatted correctly; if so, then there is an implementation problem. This should have produced (with all numbers matched to {} significant figures):\n{}\n'.format(SIGFIG_NUM, '\n'.join([r.req_str() for r in reqs])))

def main():
    filenames = find_filenames()
    if len(filenames) == 0:
        err('No files ending in \'_hmm_gaussian.py\' or \'_hmm_aspect.py\' found. Make sure your file is named LastName_hmm_gaussian.py or LastName_hmm_aspect.py.')
    if len(filenames) > 1:
        err('Only include a single file ending in \'_hmm_gaussian.py\' or \'_hmm_aspect.py\' in the submission directory.')
    print('Found Python file to run.')
    if not os.path.exists(DATA_DIR):
        err('Could not find the data directory; looked for {}. Change the DATA_DIR variable at the top of this smoke test file to wherever you have downloaded the data (points.dat or pairs.dat).'.format(DATA_DIR))
    print('Found data directory.')
    output = get_output(filenames[0])
    print('Ran Python file.')

    reqs = None
    if filenames[0].endswith('_hmm_gaussian.py'):
        reqs = [
            Req('Gaussian','Choice of Gaussian vs. Aspect'),
            Req('Train LL: -4.77194807426858', 'Training average log-likelihood'),
            Req('Initials: 0.0010293432934191963 | 0.9989706567065809','Initials'),
            Req('Transitions: 0.6800829801249292 0.3181313552693809 | 0.2963455752361618 0.7031681707785262', 'Transitions'),
            Req('Mus: -0.9101279067641551 -0.9203512949184322 | -0.7538900144698526 -0.2908644342850219', 'Mus'),
            Req('Sigmas: 2.026438798790241 0.615133664604066 0.615133664604066 7.048866518165362 | 13.074328199275778 -0.9132213696293714 -0.9132213696293714 5.450981937211618','Sigmas')
            ]
    else:
        reqs = [
            Req('Aspect','Choice of Gaussian vs. Aspect'),
            Req('Train LL: -4.496379120406352', 'Training average log-likelihood'),
            Req('Initials: 0.08411545977900343 | 0.9158845402209965','Initials'),
            Req('Transitions: 0.5965326139226069 0.401982900544391 | 0.4035512461715157 0.5957112677840523','Transitions'),
            Req('Theta_1: 0.09315537977494442 0.20087102585486133 0.04058060562384928 0.17589568862727886 0.09967059986582012 0.06534132527681508 0.07933577864672024 0.07567442954995247 0.11216106371419242 0.05731410306556584 | 0.16242341766099813 0.12132450569207631 0.07498649432612291 0.09296537420348697 0.15368085582158733 0.030202439937987356 0.10734028452366948 0.048760984480318306 0.17452652877516905 0.03378911457858414','Theta_1'),
            Req('Theta_2: 0.15322086741298546 0.18555569376507733 0.05904859072701839 0.059141272536125396 0.06084417528931156 0.09719542448501794 0.10783216299243874 0.0873876662268806 0.09284543461192021 0.09692871195322444 | 0.07564199101480143 0.09441372487584568 0.10541141008562734 0.1030956979528182 0.1125064925815035 0.16282659709824157 0.0943855474139385 0.08149924688873533 0.08715265525895204 0.0830666368295364','Theta_2')
                ]
    verify_reqs(reqs,output)
    print('Congratulations, you passed this simple test! However, make sure that your code runs AND PASSES THIS TEST on the csug server. Also, don\'t forget your README!')

if __name__ == '__main__':
    main()
