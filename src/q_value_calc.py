from enum import auto, Enum
class ParserType(Enum):
    PASSATUTTO = auto()
    SIMON = auto()

class DecoyMethod(Enum):
    CREATE_RANDOM_PEAKS = auto()

class QValueCalc:
    def __init__(self, folder, decoyMethod, parserType=ParserType.PASSATUTTO, filtering=Filtering.STANDARD, verbose=True):
        self.parser = self.getParserClass(parserType,folder)
        self.decoyGenerator = ...
        self.filter = ...
        self.spectra = None

    def calcTrue(self):
        if not self.spectra:
            self.spectra = self.filter( self.parser.parseFolder(self.verbose) )
        self.createQuery()
        self.createTrueLibrary()
        return self.computeQValue( self.match(decoy=False) )

    def createQuery(self):
        # bla bla bla
        self.query_spec = ...

    def calcDecoy(self):
        pass # TODO: Me!


    def getParserClass(self, parserType, folder):
        if parserType == ParserType.PASSATUTTO:
            import src.passatutto_parser
            return src.passatutto_parser.PassatuttoParser(folder)
        elif parserType == ParserType.SIMON:
            pass

