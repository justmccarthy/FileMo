import re, Sorter


class LexicalAnalyzer:
    Dest = ''
    SortFiles = []

    # reserved list
    Reserved = [  # if reserved[0] then token is of type reserved[1]
        ('name', 'meta'),
        ('type', 'meta'),
        # ('size', 'meta'),
        # ('modifydate', 'meta'),
        # ('createdate', 'meta'),
        # ('accessdate', 'meta'),
        # ('tag', 'meta'), # user file tag
        # ('title', 'meta'), # music / video
        # ('author', 'meta'), # music / video
        # ('length', 'meta'), # music / video
        # ('time', 'meta')
        # ('contains', 'attr'),
        # ('year', 'attr'),
        # ('month', 'attr'),
        # ('day', 'attr'),
        # ('hour', 'attr'),
        # ('minute', 'attr'),
        # ('second', 'attr'), # useless
        # ('not', 'not'),
        ('!', 'inv'),
        ('.', 'dot'),
        (':', 'endif')
    ]

    def __init__(self,DestIn, SortFilesIn):
        self.Dest = DestIn  # hold string of file destination to pass to sorter
        self.SortFiles = SortFilesIn  # hold list of files to sort to pass to sorter

    def parseTokens(self, strin):
        strin = strin.lower()  # were not doing case sensitivity
        Tokens = re.split(r'(?:(\".+?\")|(\'.+?\')|(\B\\.+\\(\B|\b))|(\B\/.+\/(\B|\b))|(\<\=)|(\>\=)|(\b\w+\b)|([\.\+\-\*\/\<\>\=\:\!\n\t]))', strin) # defines what tokens can look like and split accordingly
        Tokens = list(filter(None, Tokens))  # re.split used in on big regex like this causes a empty variables to to be added, this filters them out
        self._IdentifyTokens(Tokens)  # call identify tokens process, pass the token list

    def _IdentifyTokens(self, Tokens):  # need to work on names for token typings
        TokenTypes = []
        for x in Tokens:
            if x == ' ' or x == '\0' or x == '\t':  # filter missed spaces, end_string, and tabs out
                continue
            elif re.match(r'\n', x):  # since the language relies on new lines for new statements \n is a valid token
                TokenTypes.append(("endline","\\n"))
            elif re.match(r'^(\<\=)|(\>\=)|([\<\>\=])$', x):  # expression operators
                TokenTypes.append(("expression", x))
            elif re.match(r'^[\+\-\*\/]$',x):  # math operators # not used in current build
                TokenTypes.append(("operator", x))
            elif re.match(r'(\B\\.+\\(\B|\b))|(\B\/.+\/(\B|\b))', x):  # destination subdirectory
                TokenTypes.append(("path", x))
            elif re.match(r'(\".+?\")|(\'.+?\')', x):  # string
                TokenTypes.append(("string", x))
            elif re.match(r'\b\d+[kmgt]?[b]\b', x):  # size in bytes or k/m/g/t bytes
                TokenTypes.append(("size", x))
            elif re.match(r'\b\d+[smhdyc]\b', x):  # time in second, minutes, hours, days, years, centuries(lol)
                TokenTypes.append(("time", x))
            else:  # specific / simple definitions
                identified = False
                for y in self.Reserved:
                    if x == y[0]:
                        TokenTypes.append((y[1], x))
                        identified = True
                        break
                if identified == False:
                    TokenTypes.append(("shortstring", x))
                    # print("unrecognized token", x)
                    # return

        self._BuildOps(TokenTypes)

    # noinspection PyUnreachableCode
    def _BuildOps(self, TokenType):
        opList = []
        state = 0
        #print(TokenType)
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
            #if type2 meta.attr = meta.attr
            #elif (x[0] == "dot") and (state == 3):
            #    state = 7
            #    opbuilder.append(x)

            #elif (x[0] == "attr") and (state == 7):
            #    state = 8
            #    opbuilder.append(x)

            #elif (x[0] == "inv") and (state == 8):
            #    if opbuilder[0] == 10:
            #        opbuilder[0] = 0
            #    else:
            #        opbuilder[0] = 10
            #    state = 9

            #elif (x[0] == "expression") and ((state == 8) or (state == 9)):
            #    state = 10
            #    opbuilder.append(x)
            #elif (x[0] == 'meta') and (state == 10):
            #    state = 11
            #    opbuilder.append(x)
            #elif (x[0] == 'dot') and (state == 11):
            #    state = 12
            #    opbuilder.append(x)
            #elif (x[0] == 'attr') and (state == 12):
            #    state = 13
            #    opbuilder.append(x)


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