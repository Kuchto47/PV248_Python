import re


def get_persons_list_string(d, delimiter):
    result = None
    for i, a in enumerate(d):
        if i == 0:
            result = a.name
        else:
            result = result + delimiter + " " + a.name
        if a.born is not None:
            result = result + " (" + str(a.born) + "--"
            if a.died is not None:
                result = result + str(a.died) + ")"
            else:
                result = result + ")"
        else:
            if a.died is not None:
                result = result + " (--" + str(a.died) + ")"
    return result


def get_editors_list_string(d):
    return get_persons_list_string(d, ",")


def get_composers_list_string(d):
    return get_persons_list_string(d, ";")


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
    separated_source.append(actual_record)
    return separated_source


def get_partiture_text(partiture):
    if partiture:
        return "yes"
    return "no"


def standard_string_getter(ln):
    stripped_line = ln.strip()
    if len(stripped_line) == 0:
        return None
    return stripped_line
