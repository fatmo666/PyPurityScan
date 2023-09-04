def merge(src, target):
    for k, v in src.items():
        if hasattr(target, '__getitem__'):
            if target.get(k) and type(v) == dict:
                merge(v, target.get(k))
            else:
                target[k] = v
        elif hasattr(target, k) and type(v) == dict:
            merge(v, getattr(target, k))
        else:
            setattr(target, k, v)