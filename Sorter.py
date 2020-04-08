import os, shutil, re

class sorter:
    ifstack = []
    opfeed = []
    files = []
    dest = ''

    def __init__(self, oplist, dest, filelist):
        self.opfeed = oplist
        self.files = filelist
        self.dest = dest
        self.sortif()

    def stackif(self, file, ops):
        boolstack = True
        for x in ops:
            if x[1] == 'type' and x[3][0] == 'shortstring':
                name = os.path.basename(file)
                reg = x[3][1]
                boolstack = boolstack and re.match(r'.+\.%s' % reg, name)
            if x[1] == 'name' and x[3][0] == 'shortstring':
                name = os.path.basename(file)
                reg = x[3][1]
                if x[0] == 1:
                    boolstack = boolstack and (re.match(r'^%s\.[^.]*' % reg, name))
                elif x[0] == 6:
                    boolstack = boolstack and (not re.match(r'^%s\.[^.]*' % reg, name))
                else:
                    boolstack = False
        return boolstack




    def sortif(self):
        opstack = []
        for x in self.opfeed:
            if x[0] == 0:
                for y in self.files:
                    if self.stackif(y, opstack):
                        print('moved', y, 'to', self.dest + x[1])
                        try:
                            os.mkdir(self.dest + x[1])
                        except:
                            pass
                        try:
                            os.rename(y, (self.dest + x[1] + os.path.basename(y)))
                        except:
                            print('failed to move', y, 'to', self.dest + x[1])
                            self.files.remove(y)
                        self.files.remove(y)
                    else:
                        print(y, 'not moved to', self.dest + x[1])
                opstack.pop(-1)
            else:
                opstack.append(x)
