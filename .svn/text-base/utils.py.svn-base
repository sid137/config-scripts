import sys
import subprocess

class CmdException(Exception): 
    def __init__(self,  message):
        self.message = message
        
    def __str__(self):
        return repr(self.message)

    
def run_cmd(cmds, env=None, cwd='.', root = False):
    env = env or {}
    for cmd in cmds.splitlines():
        if cmd:
            print "Cmd: ", cmd
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, cwd=cwd, env=env )
            output = proc.communicate()[0]
            print "Output: ", output
            if not (proc.returncode == 0):
                print output
                raise Exception(output)
    return output
    
def initFromArgs(beingInitted, bJustArgs=False):
    codeObject = beingInitted.__class__.__init__.im_func.func_code
    for k,v in sys._getframe(1).f_locals.items():
        if k!='self' and ((not bJustArgs) or k in codeObject.co_varnames[1:codeObject.co_argcount]):
            setattr(beingInitted,k,v)


def icount(d):
    """Returns the total number of values in a list of dictionaries,
    or a list of lists
    needs to be made more like ruby's flatten - doesn't handle nestd lists
    > > > d = [[5,3,2], [2,4,3],[1,2,3]]
    9
    """
    try:
        return sum([len(list) for list in d.itervalues()])
    except:
        return sum([len(list) for list in d])

def lslice(list, size=10):
    for i in xrange(0, len(list), size):
        yield (i, i+size,list[i: i+size])

def ranger(lis):
    """Returns list tupe ranged tuples for an numerical input list

    >>> l = [0,2,3,5,6, 8, 9, 10, 14, 15, 22, 34, 35, 36, 38]
    >>> ranger(l)
    [(0, 0), (2, 3), (5, 6), (8, 10), (14, 15), (22, 22), (34, 36), (38, 38)]
    
    """
    tset = []
    try:
        t1 = lis[0]
        for i, v in enumerate(lis):
            if (v-lis[i-1] > 1):
                t2 = lis[i-1]
                tset.append((t1,t2))
                t1 = v
                if v is lis[-1]:
                    t2 = v
                    tset.append((t1,t2))
    except IndexError:
        pass
    return tset
