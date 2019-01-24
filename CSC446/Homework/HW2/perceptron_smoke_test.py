#!/usr/bin/python3
from __future__ import print_function #in case somebody tries to run this file with Python 2
import sys
import os

DATA_DIR = '/u/cs246/data/adult/' #TODO: change this to wherever you put the data if working on a different machine

def err(msg):
    print('ERROR: {}'.format(msg), file=sys.stderr)
    exit()

def find_filenames():
    return [fn for fn in os.listdir('.') if os.path.isfile(fn) and fn.endswith('_perceptron.py')]

def get_output(filename):
    import subprocess
    cmd = './{} --nodev --iterations 5 --lr 2.0 --train_file {} --test_file {}'.format(filename, os.path.join(DATA_DIR, 'a7a.train'), os.path.join(DATA_DIR, 'a7a.test'))
    print('Running this command:\n{}'.format(cmd))
    try:
        output = subprocess.check_output(cmd.split()).decode('utf-8')
    except subprocess.CalledProcessError:
        err('Perceptron file did not exit successfully (likely crashed).')
    except OSError as e:
        if e.errno == 13:
            err('Perceptron file is not executable; run this command:\nchmod u+x {}'.format(filename))
        elif e.errno == 8:
            err('Perceptron file does not start with a shebang; put this line at the very top:\n#!/usr/bin/python3\n(Replace python3 with python if using Python 2)')
        elif e.errno == 2:
            err('Unable to execute perceptron file; if you ever edited the file on Windows, it is possible that the line endings are wrong, so try running this command:\ndos2unix {}\nOtherwise, you\'ll have to take a look at it and see what went wrong.'.format(filename))
        else:
            print('Got an OS error not caused by permissions or a shebang problem; you\'ll have to take a look at it and see what the problem is. See below:')
            raise e

    return output

def verify_output(output):
    acc_req = 'Test accuracy: 0.79955088'
    got_acc = False
    weight_req = 'Feature weights (bias last): -16.0 -6.0 6.0 6.0 2.0 2.0 -2.0 10.0 16.0 4.0 2.0 -6.0 0.0 -18.0 6.0 8.0 -6.0 2.0 -6.0 0.0 -2.0 0.0 4.0 -4.0 4.0 2.0 -8.0 10.0 -2.0 4.0 2.0 10.0 -4.0 -18.0 -14.0 0.0 0.0 0.0 6.0 18.0 -6.0 -16.0 -10.0 -4.0 -8.0 18.0 8.0 4.0 0.0 6.0 16.0 0.0 -4.0 0.0 0.0 -8.0 -6.0 -2.0 12.0 0.0 10.0 -4.0 -4.0 -2.0 -6.0 -2.0 2.0 8.0 -6.0 -8.0 -4.0 -6.0 -2.0 -14.0 6.0 -10.0 2.0 -14.0 -2.0 -2.0 0.0 10.0 10.0 10.0 2.0 -12.0 16.0 0.0 0.0 -22.0 10.0 0.0 -4.0 -6.0 12.0 0.0 0.0 8.0 6.0 4.0 4.0 -12.0 2.0 -4.0 10.0 -4.0 -6.0 -2.0 18.0 -2.0 0.0 -18.0 -8.0 10.0 6.0 10.0 -10.0 14.0 4.0 -4.0 -10.0 -6.0 0.0 -8.0'
    got_weight = False
    for line in output.split('\n'):
        if line.startswith(acc_req):
            print('Test accuracy is correct!')
            got_acc = True
        elif line.startswith(weight_req):
            print('Feature weights are correct!')
            got_weight = True
    if not (got_acc and got_weight):
        err('Unable to find one or more required output lines. Make sure each is on its own line and formatted correctly; if so, then there is an implementation problem. This should have produced (only considering the first 8 decimal places of test accuracy):\n{}\n{}'.format(acc_req,weight_req))

def main():
    filenames = find_filenames()
    if len(filenames) == 0:
        err('No files ending in \'_perceptron.py\' found. Make sure your file is named LastName_perceptron.py.')
        exit()
    if len(filenames) > 1:
        err('Only include a single file ending in \'_perceptron.py\' in the submission directory.')
    print('Found Python file to run.')
    if not os.path.exists(DATA_DIR):
        err('Could not find the data directory; looked for {}. Change the DATA_DIR variable at the top of this smoke test file to wherever you have downloaded the data (a7a.*).'.format(DATA_DIR))
    print('Found data directory.')
    output = get_output(filenames[0])
    print('Ran Python file.')
    verify_output(output)
    print('Congratulations, you passed this simple test! However, make sure that your code runs on the csug server. Also, don\'t forget your README!')

if __name__ == '__main__':
    main()
