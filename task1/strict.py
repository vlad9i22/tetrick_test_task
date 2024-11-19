from functools import wraps


def strict(func):
    @wraps(func)
    def new_func(*args):
        if len(args) + 1 != len(func.__annotations__):
            raise TypeError("Not all variables are annotated or no return annotations")
        for f_val, cls, val_name in zip(args,
                                        func.__annotations__.values(),
                                        func.__annotations__.keys()):
            if not type(f_val) is cls:
                raise TypeError(f"Wrong argument for {val_name} shoul be {cls}"
                                f" but is {type(f_val)} instead")
        res = func(*args)
        if not type(res) is func.__annotations__['return']:
            raise TypeError("Wrong return type")
        return res
    return new_func



