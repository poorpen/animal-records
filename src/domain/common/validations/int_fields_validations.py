from src.domain.common.exceptions.validation import IntegerMin, IntegerMax, ListEmpty


def validation_of_min_allowable_int(v, field_name, min_integer, flag):
    if flag == '<' and v < min_integer:
        raise IntegerMin(min_integer=min_integer, field=field_name)
    elif flag == '<=' and v <= min_integer:
        raise IntegerMin(min_integer=min_integer, field=field_name)
    elif flag not in ('<', '<='):
        raise ValueError('Unsupported flag')


def validation_of_max_allowable_int(v, field_name, max_integer, flag):
    if flag == '>' and v > max_integer:
        raise IntegerMax(max_integer=max_integer, field=field_name)
    elif flag == '>=' and v >= max_integer:
        raise IntegerMax(max_integer=max_integer, field=field_name)
    elif flag not in ('>', '>='):
        raise ValueError('Unsupported flag')
