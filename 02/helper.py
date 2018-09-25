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