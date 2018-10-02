import re


def get_persons_list_string(d):
    result = ""
    for i, a in enumerate(d):
        if i == 0:
            result = a.name
        else:
            result = result + ", " + a.name
        if a.born is not None:
            result = result + " (" + a.born + "-"
            if a.died is not None:
                result = result + a.died + ")"
            else:
                result = result + ")"
        else:
            if a.died is not None:
                result = result + " (-" + a.died + ")"
    return result


def get_composition_year(yr):
    match = re.match(r".*([0-9]{4}).*", yr)
    if match is not None:
        return int(match.group(1))
    return None


def get_individual_editors_from_string(text):
    result = []
    if len(text.strip()) == 0:
        return result
    texts = text.split(",")
    if len(texts) == 1:
        result.append(text)
    else:
        next_is_surname = False
        name = ""
        for txt in texts:
            entry = txt.strip()
            if next_is_surname:
                next_is_surname = False
                result.append(name + " " + entry)
                name = ""
            else:
                if len(entry.split(" ")) >= 2:
                    result.append(entry)  # has name and surname as well
                else:
                    name = entry
                    next_is_surname = True
    return result


def get_separated_source(file):
    records_dividing_exp = re.compile(r"Print Number: [0-9]+")
    separated_source = []
    actual_record = []
    for line in file:
        match = records_dividing_exp.match(line)
        if match is not None:
            if len(actual_record) == 0:
                actual_record.append(line)
            else:
                separated_source.append(actual_record)
                actual_record = [line]
        else:
            actual_record.append(line)
    return separated_source


def get_edition_from_ln(ln):
    return standard_string_getter(ln)


def get_title_from_line(ln):
    return standard_string_getter(ln)


def get_incipit_from_line(ln):
    return standard_string_getter(ln)


def get_key_from_line(ln):
    return standard_string_getter(ln)


def get_genre_from_line(ln):
    return standard_string_getter(ln)


def get_voice_from_line(ln):
    return standard_string_getter(ln)


def standard_string_getter(ln):
    stripped_line = ln.strip()
    if len(stripped_line) == 0:
        return None
    return stripped_line
