class Person:
    def __init__(self, name, born, died):
        self.name = name  # string
        self.born = born  # integer (or None)
        self.died = died  # integer (or None)


class Composition:
    def __init__(self, name, incipit, key, genre, year, voices, authors):
        self.name = name  # string
        self.incipit = incipit  # string
        self.key = key  # string
        self.genre = genre  # string
        self.year = year  # int if integral year is given (or None)
        self.voices = voices  # list of Voice instances
        self.authors = authors  # list of Person instances


class Print:
    def __init__(self, edition, print_id, partiture):
        self.edition = edition  # instance of Edition
        self.print_id = print_id  # int from "Print Number"
        self.partiture = partiture  # boolean

    def format(self):
        raise NotImplemented

    def composition(self):
        return self.edition.composition


class Edition:
    def __init__(self, composition, authors, name):
        self.composition = composition  # instance of Composition
        self.authors = authors  # list of Person instances
        self.name = name  # string from "Edition" field (or None)


class Voice:
    def __init__(self, name, range):
        self.name = name  # string
        self.range = range  # string


def load(filename):
    raise NotImplemented
    # will return print_id sorted list of Print instances


