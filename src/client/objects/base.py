import dataclasses


@dataclasses.dataclass
class BaseObject:
    raw: dict
    id: int

    @classmethod
    def from_dict(cls, data):
        raw = data.copy()
        initial = {}
        for key in [
            getattr(f, "name") for f in dataclasses.fields(cls) if f.name != "raw"
        ]:
            parse_method = getattr(cls, f"parse_{key}", None)
            if callable(parse_method):
                initial[key] = parse_method(data.get(key))
            else:
                initial[key] = data.get(key)
        return cls(**initial, raw=raw)

    @classmethod
    def multiple_from_dict(cls, data):
        return [cls.from_dict(item) for item in data]
