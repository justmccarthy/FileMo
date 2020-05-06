import os #shutil, re

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
        state = True
        for x in ops:  # if there is no ops returns true
            if x[1][1] == 'filename':
                #name = os.path.basename(file)
                name = os.path.splitext(file)
                reg = x[3][1][1:-1]  # strip quotes
                if x[1][0] == 'type':
                    if x[2][0] == 'contains':
                        if reg == '':
                            state = True
                        else:
                            #state = re.match(r'.*\.\w*%s\w*$' % reg, name)
                            state = (reg in name[1])
                    else:
                        #if reg == '':
                            #state = not re.match(r'^.+(\.\S+)$' % reg, name)
                        #else:
                            #state = re.match(r'.*\.%s$' % reg, name)
                        state = (reg == name[1])

                elif x[1][0] == 'name':
                    if x[2][0] == 'contains':
                        if reg == '':
                            state = True
                        else:
                            #state = re.match(r'\w*%s\w*(.[^.]+)?$' % reg, name)
                            state = (reg in name[0])
                    else:
                        #state = re.match(r'^%s(.[^.]+)?$' % reg, name)
                        state = (reg == name[0])

                if x[0] == 6:
                    state = not state
            elif x[1] == 'medianame':
                reg = x[3][1][1:-1]  # strip quotes

            else:
                state = False  # if op is unrecognized returns false

        return boolstack and state

    def sortif(self):
        opstack = []
        for x in self.opfeed:
            if x[0] == 0:
                if opstack[i][1] == 'clear':  # clear if stack
                    i = len(opstack) - 1
                    while i >= 0:
                        opstack.pop(i)
                elif opstack[i][1] == 'path':
                    for y in self.files:
                        if self.stackif(y, opstack):  # do if stack on file
                            try:
                                os.mkdir(self.dest + x[1])  # make directory
                            except:
                                pass  # directory already exists
                            try:
                                os.rename(y, (self.dest + x[1] + os.path.basename(y)))
                            except:
                                pass
                    i = len(opstack) - 1
                    while (i >= 0 and opstack[i][1][0] == 'endline'):
                        opstack.pop(i)
            else:
                opstack.append(x)
