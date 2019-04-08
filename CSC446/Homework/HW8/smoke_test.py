#!/usr/bin/env python3
import sys
import os

DATA_DIR = '/u/cs246/data/em/' #TODO: change this to wherever you put the data if working on a different machine
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
        cmd = './{} --nodev --iterations 2 --clusters_file gaussian_hmm_smoketest_clusters.txt --data_file {} --print_params'.format(filename, os.path.join(DATA_DIR,'points.dat'))
    else:
        cmd = './{} --nodev --iterations 2 --clusters_file aspect_hmm_smoketest_clusters.txt --data_file {} --print_params'.format(filename, os.path.join(DATA_DIR,'pairs.dat'))
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
            Req('Train LL: -4.743163695630071', 'Training average log-likelihood'),
            Req('Initials: 4.547576784065208e-06 | 0.999995452423216','Initials'),
            Req('Transitions: 0.6500853065797068 0.348224984649036 | 0.28855257497396536 0.7108134469224332', 'Transitions'),
            Req('Mus: -0.7517330032101541 -0.4806221284917155 | -0.8927560428826611 -0.6867117229719076', 'Mus'),
            Req('Sigmas: 2.0615058993501805 0.8053297716501053 0.8053297716501053 7.528027303127667 | 12.403570211657076 -0.9540100985875335 -0.9540100985875335 5.301268330954566', 'Sigmas')
            ]
    else:
        reqs = [
            Req('Aspect','Choice of Gaussian vs. Aspect'),
            Req('Train LL: -4.496573732258457', 'Training average log-likelihood'),
            Req('Initials: 0.023146234442709086 | 0.9768537655572909','Initials'),
            Req('Transitions: 0.5945163869524955 0.4040262236049093 | 0.40664996637425155 0.5925862408901985','Transitions'),
            Req('Theta_1: 0.08985515696125525 0.19320537145616498 0.037862895341933975 0.17762027728229707 0.10250288806819183 0.06837807580079794 0.08652823091850877 0.07171210980416427 0.1147608693536056 0.056116735570485576 | 0.16581429886938123 0.12669489648783275 0.07775247439678733 0.09113893335305363 0.15090302097246605 0.02711560693159694 0.10015887481645834 0.05270383184214025 0.1719916144701287 0.03496265512460526','Theta_1'),
            Req('Theta_2: 0.15048138795444946 0.1817292921780116 0.05873108458368333 0.06004114015804868 0.06026738755004894 0.10008739593063802 0.11101407453270887 0.08679749491023184 0.09230573019506738 0.09708762256451721 | 0.07829926427540881 0.09814537424124767 0.10578391529657705 0.10224436554605924 0.11314523579775539 0.16000244632600266 0.09117840422153699 0.08208432661122406 0.08768734456353776 0.08066553038510094','Theta_2')
                ]
    verify_reqs(reqs,output)
    print('Congratulations, you passed this simple test! However, make sure that your code runs AND PASSES THIS TEST on the csug server. Also, don\'t forget your README!')

if __name__ == '__main__':
    main()
