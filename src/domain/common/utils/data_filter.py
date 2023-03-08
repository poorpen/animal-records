from src.domain.common.constants.empty import Empty


def data_filter(**kwargs):
    filtered = {}
    for name, value in kwargs.items():
        if isinstance(value, Empty) or value is None:
            continue
        filtered[name] = value
    return filtered
