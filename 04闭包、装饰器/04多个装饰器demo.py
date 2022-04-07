def set_h1(func):
    def local_get_str(*args, **kwargs):
        return "<h1>" + func(*args, **kwargs) + "</h1>"

    return local_get_str


def set_p(func):
    def local_get_str(*args, **kwargs):
        return "<p>" + func(*args, **kwargs) + "</p>"

    return local_get_str


@set_h1
@set_p
def get_str():
    return "hello world!"


print(get_str())
