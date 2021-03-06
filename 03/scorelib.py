import helper
import re


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
        return helper.get_composers_list_string(self.authors)


class Print:
    def __init__(self, edition, print_id, partiture):
        self.edition = edition  # instance of Edition
        self.print_id = print_id  # int from "Print Number"
        self.partiture = partiture  # boolean

    def format(self):
        my_dict = {}
        self.init_dictionary(my_dict)
        self.print_format(my_dict)

    def composition(self):
        return self.edition.composition

    def init_dictionary(self, my_dict):
        my_dict["Print Number"] = self.print_id
        my_dict["Composer"] = self.composition().get_composers()
        my_dict["Title"] = self.composition().name
        my_dict["Genre"] = self.composition().genre
        my_dict["Key"] = self.composition().key
        my_dict["Composition Year"] = self.composition().year
        my_dict["Edition"] = self.edition.name
        my_dict["Editor"] = self.edition.get_editors()
        for v in self.composition().voices:
            my_dict["Voice " + str(v.order)] = self.get_voice_string(v)
        my_dict["Partiture"] = helper.get_partiture_text(self.partiture)
        my_dict["Incipit"] = self.composition().incipit

    def print_format(self, d):
        for k, v in d.items():
            if v is not None:
                print("%s: %s" % (k, str(v)))

    def get_voice_string(self, voice):
        res = None
        if voice.range is not None:
            res = voice.range
            if voice.name is not None:
                res += ", " + voice.name
        else:
            if voice.name is not None:
                res = voice.name
        return res


class Edition:
    def __init__(self, composition, authors, name):
        self.composition = composition  # instance of Composition
        self.authors = authors  # list of Person instances
        self.name = name  # string from "Edition" field (or None)

    def get_editors(self):
        return helper.get_editors_list_string(self.authors)


class Voice:
    def __init__(self, name, rng, order):
        self.name = name  # string
        self.range = rng  # string
        self.order = order  # determines order of voice in print


def load(filename):
    f = open(filename, 'r', encoding="utf_8")
    separated_source = helper.get_separated_source(f)
    list_of_prints = get_list_of_prints(separated_source)
    list_of_prints.sort(key=sort_prints)
    return list_of_prints


def sort_prints(p):
    return p.print_id


def get_list_of_prints(records):
    list_of_prints = []
    for record in records:
        print_number = None
        partiture = False
        edition = None
        editors = []
        year = None
        title = None
        incipit = None
        key = None
        genre = None
        voices = {}
        composers = []
        for line in record:
            match = re.match(r"Print Number: ([0-9]+)", line)
            if match is not None:
                print_number = int(match.group(1))
                continue
            match = re.match(r"Partiture: (.*)", line)
            if match is not None:
                if len(match.group(1).strip()) == 0 or re.match(r"no.*", match.group(1)) is not None:
                    partiture = False
                else:
                    partiture = True
                continue
            match = re.match(r"Edition: (.*)", line)
            if match is not None:
                edition = helper.standard_string_getter(match.group(1))
                continue
            match = re.match(r"Editor:(.*)", line)
            if match is not None:
                editors = helper.get_individual_editors_from_string(match.group(1))
                continue
            match = re.match(r"Composition Year:(.*)", line)
            if match is not None:
                year = helper.get_composition_year(match.group(1))
                continue
            match = re.match(r"Title:(.*)", line)
            if match is not None:
                title = helper.standard_string_getter(match.group(1))
                continue
            match = re.match(r"Incipit:(.*)", line)
            if match is not None:
                incipit = helper.standard_string_getter(match.group(1))
                continue
            match = re.match(r"Key:(.*)", line)
            if match is not None:
                key = helper.standard_string_getter(match.group(1))
                continue
            match = re.match(r"Genre:(.*)", line)
            if match is not None:
                genre = helper.standard_string_getter(match.group(1))
                continue
            match = re.match(r"Voice ([0-9]{1,2}):(.*)", line)
            if match is not None:
                voices[int(match.group(1))] = helper.standard_string_getter(match.group(2))
                continue
            match = re.match(r"Composer:(.*)", line)
            if match is not None:
                composers = match.group(1).split(";")
                continue
        list_of_prints.append(
            create_print_object_from(
                print_number,
                partiture,
                edition,
                editors,
                year,
                title,
                incipit,
                key,
                genre,
                voices,
                composers
            )
        )
    return list_of_prints


def create_print_object_from(print_number, partiture, edition, editors, year, title, incipit, key, genre, voices, composers):
    composition_obj = get_composition_obj(composers, voices, year, genre, key, incipit, title)
    editors_list = get_editors_list(editors)
    ed = Edition(composition_obj, editors_list, edition)
    return Print(ed, print_number, partiture)


def get_editors_list(editors):
    ed_lst = []
    rm1 = r"\(partiture\)"
    rm2 = r"arranger"
    rm3 = r"continuo:"
    rm4 = r"\(bass realisation\)"
    for editor in editors:
        name = None
        stripped_editor = editor.strip()
        if len(stripped_editor) != 0:
            name = re.sub(rm1, "", stripped_editor)
            name = re.sub(rm2, "", name)
            name = re.sub(rm3, "", name)
            name = re.sub(rm4, "", name)
        ed_lst.append(Person(name.strip(), None, None))
    return ed_lst


def get_composition_obj(composers, voices, year, genre, key, incipit, title):
    composers_list = []
    for composer in composers:
        composers_list.append(create_composer_from_line(composer))
    voices_list = []
    for k, v in voices.items():
        if v is not None:
            voices_list.append(get_voice_obj_from_line(k, v))
    return Composition(title, incipit, key, genre, year, voices_list, composers_list)


def get_voice_obj_from_line(order, ln):
    rng = None
    name = None
    m = re.match(r"([^,; ]+--[^,; ]+)", ln)
    if m is None:
        if len(ln.strip()) != 0:
            name = ln.strip()
    else:
        rng = m.group(1)
        rest = re.sub(r"[^,; ]+--[^,; ]+[;,]?", "", ln)
        if len(rest.strip()) != 0:
            name = rest.strip()
    return Voice(name, rng, order)


def create_composer_from_line(composer):
    name = re.sub(r'\([^)]*\)', '', composer).strip()
    if len(name) == 0:
        name = None
    birth = None
    death = None
    match_brackets = re.match(r".*\(([^)]*)\).*", composer)
    if match_brackets is not None:
        birth = get_birth_year(match_brackets.group(1))
        death = get_death_year(match_brackets.group(1))
    return Person(name, birth, death)


# It is not forbidden in Discussion Forum to parse years like 1700/2, only said it is not mandatory,
# I wondered whether it will work this way and it does so I left it here,
# I believe it won't ruin my chances of passing.
def get_birth_year(ln):
    match = re.match(r"([0-9]{4}).*", ln)
    if match is not None:
        if ln[0] != "+":
            return int(match.group(1))
    return None


def get_death_year(ln):
    match = re.match(r".*[-+]+([0-9]{4}).*", ln)
    if match is not None:
        return int(match.group(1))
    return None
