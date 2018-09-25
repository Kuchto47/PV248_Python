class Person:
    def __init__(self, name, born, died):
        self.name = name
        self.born = born
        self.died = died


class Composition:
    def __init__(self, name, incipit, key, genre, year, voices, authors):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.voices = voices
        self.authors = authors


class Print:
    def __init__(self, edition, print_id, partiture):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture

    def format(self):
        raise NotImplemented

    def composition(self):
        raise NotImplemented


class Edition:
    def __init__(self, composition, authors, name):
        self.composition = composition
        self.authors = authors
        self.name = name


class Voice:
    def __init__(self, name, range):
        self.name = name
        self.range = range


def load(filename):
    raise NotImplemented
    # will return print_id sorted list of Print instances


