from process_api.expressions.sanitize import sanitize


class Conditions:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Conditions, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        self.store = {}
        self.globals: dict[str, any] = {}

    def exec(self, condition, ctx=None, process=None, item=None):
        fn = self.store.get(condition)

        if fn:
            return fn(ctx, process, item)

        sanitized = sanitize(condition)

        code_str = f"lambda context, process, item: {sanitized}"
        dynamic_function = eval(compile(code_str, "<string>", "eval"))
        self.store[condition] = dynamic_function
        result = dynamic_function(ctx, process, item)
        return result


conditions = Conditions()
