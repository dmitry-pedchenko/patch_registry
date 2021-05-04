class Translit():
    # Преобразование слова с русский букв, на английские, потому что не нашел
    symbols = {'й':'i','ц':'tc','у':'u','к':'k','е':'e','н':'n','г':'g','ш':'sh','щ':'shch','з':'z','х':'kh','ъ':'^',
               'ё':'e','э':'e','ж':'zh','д':'d','л':'l','о':'o','р':'r','п':'p','а':'a','в':'v','ы':'y','ф':'f','ю':'iu',
               'б':'b','ь':'^','т':'t','и':'i','м':'m','с':'s','ч':'ch','я':'ia',' ':'_'}
    def __init__(self, word:str):
        self.word = word

    def convert(self):
        output = ''
        for symbol in self.word:
            if self.symbols.get(symbol.lower()):
                symbol = self.symbols.get(symbol.lower())
            output += symbol
        return output

