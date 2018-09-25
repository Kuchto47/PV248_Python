import helper


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

    def get_composers(self):
        return helper.get_persons_list_string(self.authors)


class Print:
    def __init__(self, edition, print_id, partiture):
        self.edition = edition  # instance of Edition
        self.print_id = print_id  # int from "Print Number"
        self.partiture = partiture  # boolean

    def format(self):
        my_dict = {}
        my_dict["Title"] = self.composition().name
        my_dict["Incipit"] = self.composition().incipit
        my_dict["Key"] = self.composition().key
        my_dict["Genre"] = self.composition().genre
        my_dict["Year"] = self.composition().year
        number_of_voices = 0
        for i, v in enumerate(self.composition().voices):
            my_dict["Voice "+str(i)] = v
            number_of_voices += 1
        my_dict["Composer"] = self.composition().get_composers()
        my_dict["Edition"] = self.edition.name
        my_dict["Editor"] = self.edition.get_editors()
        my_dict["Print Number"] = self.print_id
        my_dict["Partiture"] = self.partiture
        self.print_format(my_dict)

    def composition(self):
        return self.edition.composition

    def print_format(self, d):
        for k, v in d:
            if v is not None:
                print("%s: %s" % (k, str(v)))


class Edition:
    def __init__(self, composition, authors, name):
        self.composition = composition  # instance of Composition
        self.authors = authors  # list of Person instances
        self.name = name  # string from "Edition" field (or None)

    def get_editors(self):
        return helper.get_persons_list_string(self.authors)


class Voice:
    def __init__(self, name, range):
        self.name = name  # string
        self.range = range  # string


def load(filename):
    raise NotImplemented
    # will return print_id sorted list of Print instances


