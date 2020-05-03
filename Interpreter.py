import re, OpBuilder


class LexicalAnalyzer:
    # reserved list
    Reserved = [  # if reserved[0] then token is of type reserved[1]
        ('name', 'meta'),
        ('type', 'meta'),
        ('size', 'meta'),
        ('modifydate', 'meta'),
        ('createdate', 'meta'),
        ('accessdate', 'meta'),
        ('tag', 'meta'), # user file tag
        ('title', 'meta'), # music / video
        ('author', 'meta'), # music / video
        ('length', 'meta'), # music / video
        ('time', 'meta'),

        ('contains', 'attr'),
        ('year', 'attr'),
        ('month', 'attr'),
        ('day', 'attr'),
        ('hour', 'attr'),
        ('minute', 'attr'),
        ('second', 'attr'), # useless
        # ('not', 'not'),
        ('!', 'inv'),
        ('.', 'dot'),
        (':', 'endif')
    ]

    def __init__(self,DestIn, SortFilesIn):
        self.builder = OpBuilder.OpBuild(DestIn, SortFilesIn)


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

        self.builder.BuildOps(TokenTypes)

