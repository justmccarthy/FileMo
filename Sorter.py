import os, shutil, re

class sorter:
    ifstack = []
    opfeed = []
    files = []
    dest = ''

    def __init__(self, oplist, dest, filelist):
        print("sorter init")
        self.opfeed = oplist
        self.files = filelist
        self.dest = dest
        self.sortif()

    def stackif(self, file, ops):
        print("stackif: ")
        boolstack = True
        for x in ops:
            print(x)
            if x[1] == 'type' and x[3][0] == 'shortstring':
                reg = x[3][1]
                boolstack = boolstack and re.match(r'.+\.%s' % reg, file)
        return boolstack




    def sortif(self):
        print("sortif init")
        print(self.opfeed)
        opstack = []
        for x in self.opfeed:
            if x[0] == 0:
                print(self.files)
                for y in self.files:
                    print(y)
                    if self.stackif(y, opstack):
                        print('move', y, 'to', self.dest + x[1])
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
                        print('no move', y, 'to', self.dest + x[1])
                opstack.pop(-1)
            else:
                opstack.append(x)
