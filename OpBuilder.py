import Sorter, Interpreter

class OpBuild:
    # Reserved = Interpreter.Reserved
    Dest = ''
    SortFiles = []

    def __init__(self,DestIn, SortFilesIn):
        self.Dest = DestIn  # hold string of file destination to pass to sorter
        self.SortFiles = SortFilesIn  # hold list of files to sort to pass to sorter

    # noinspection PyUnreachableCode
    def BuildOps(self, TokenType):
        opList = []
        state = 0
        # print(TokenType)
        opbuilder = [0, '', '', '', '']
        for x in TokenType:
            # print (x, state) # debug
            # path statement
            if (x[0] == "path") and (state == 0):
                state = 1
                opbuilder[0] = 0
                opbuilder[1] = x[1]

            # if statement
            # elif (x[0] == "not") and (state == 0):
            #     state = 2
            #     opbuilder[0] = 10

            elif (x[0] == "meta") and ((state == 0) or (state == 2)):
                state = 3
                opbuilder[1] = x[1]

            # if type1: meta =
            elif (x[0] == "inv") and (state == 3):
                opbuilder[0] = 6
                state = 4

            elif (x[0] == "expression") and ((state == 3) or (state == 4)):
                if x[1] == '=':
                    if opbuilder[0] != 6:
                        opbuilder[0] = 1
                elif x[1] == '>=':
                    if opbuilder[0] == 6:
                        opbuilder[0] = 3
                    else:
                        opbuilder[0] = 2
                elif x[1] == '<':
                    if opbuilder[0] == 6:
                        opbuilder[0] = 2
                    else:
                        opbuilder[0] = 3
                elif x[1] == '<=':
                    if opbuilder[0] == 6:
                        opbuilder[0] = 5
                    else:
                        opbuilder[0] = 4
                elif x[1] == '>':
                    if opbuilder[0] == 6:
                        opbuilder[0] = 4
                    else:
                        opbuilder[0] = 5

                state = 5

            elif ((x[0] == "string") or (x[0] == "shortstring") or (x[0] == "size")) and (state == 5):
                state = 6
                opbuilder[3] = x

            # Blocked off for demo
            # if type2 meta.attr = meta.attr
            elif (x[0] == "dot") and (state == 3):
                state = 7
                opbuilder.append(x)

            elif (x[0] == "attr") and (state == 7):
                state = 8
                opbuilder.append(x)

            elif (x[0] == "inv") and (state == 8):
                if opbuilder[0] == 10:
                    opbuilder[0] = 0
                else:
                    opbuilder[0] = 10
                state = 9

            elif (x[0] == "expression") and ((state == 8) or (state == 9)):
                state = 10
                opbuilder.append(x)
            elif (x[0] == 'meta') and (state == 10):
                state = 11
                opbuilder.append(x)
            elif (x[0] == 'dot') and (state == 11):
                state = 12
                opbuilder.append(x)
            elif (x[0] == 'attr') and (state == 12):
                state = 13
                opbuilder.append(x)

            # end if
            elif (x[0] == "endif") and ((state == 6) or (state == 13)):
                state = 14

            # end line
            elif (x[0] == "endline") and ((state == 1) or (state == 14)):
                state = 0
                opList.append(opbuilder)
                opbuilder = [0, '', '', '', '']

            elif x[0] == "endline" and state == 0:
                state = 0

            else:
                print("error: bad syntax at:", x[1])
                print("state = ", state)
                return
        Sorter.sorter(opList, self.Dest, self.SortFiles)
