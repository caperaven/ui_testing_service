import pandas as pd
from process_api.utils.get_value import get_value
import matplotlib.pyplot as plt


class DataCache:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataCache, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        self.store = {}

    def get(self, name):
        return self.store.get(name, None)

    def load(self, name, source):
        if name in self.store:
            return self.store[name]

        # load the pandas from the source
        data_frame = pd.read_csv(source)
        self.store[name] = data_frame

        return self.store[name]

    def unload(self, name):
        del self.store[name]

    def call(self, name, method, args=None):
        df = self.store[name]
        method = getattr(df, method)

        if (method is None):
            return None

        if args is None:
            return method()
        else:
            return method(**args)

    def get_perspective(self, name, perspective):
        df = self.store[name]

        if "filter" in perspective:
            query = format_filter(perspective["filter"])
            df = df.query(query)

        if "sort" in perspective:
            sort = perspective["sort"]
            by_list = []
            ascending_list = []

            for key, value in sort.items():
                by_list.append(key)
                ascending_list.append(value == "asc")

            df = df.sort_values(by=by_list, ascending=ascending_list)

        if "group_by" in perspective:
            group_by = perspective["group_by"]
            df = df.groupby(group_by).sum()

        return df


data_cache = DataCache()


def format_filter(filter_expr):
    filter_expr = filter_expr.replace(" eq ", " == ")
    filter_expr = filter_expr.replace(" gt ", " > ")
    filter_expr = filter_expr.replace(" lt ", " < ")
    filter_expr = filter_expr.replace(" gte ", " >= ")
    filter_expr = filter_expr.replace(" lte ", " <= ")
    filter_expr = filter_expr.replace(" ne ", " != ")
    return filter_expr


class DataModule:
    @staticmethod
    def register(api):
        api.add_module("data", DataModule)

    @staticmethod
    async def perform(api, step, ctx=None, process=None, item=None):
        action = step["action"]

        fn = getattr(DataModule, action, None)

        if fn is not None:
            return await fn(api, step, ctx, process, item)

    @staticmethod
    async def load(api, step, ctx=None, process=None, item=None):
        args = step["args"]
        name = await get_value(args.get("name"), ctx, process, item)
        source = await get_value(args.get("source"), ctx, process, item)
        return data_cache.load(name, source)

    @staticmethod
    async def unload(api, step, ctx=None, process=None, item=None):
        args = step["args"]
        name = await get_value(args.get("name"), ctx, process, item)
        data_cache.unload(name)
        return True

    @staticmethod
    async def set_data(api, step, ctx=None, process=None, item=None):
        args = step["args"]
        name = await get_value(args.get("name"), ctx, process, item)
        data = await get_value(args.get("data"), ctx, process, item)
        data_cache.store[name] = pd.DataFrame(data)
        return True

    @staticmethod
    async def get(api, step, ctx=None, process=None, item=None):
        args = step["args"]
        name = await get_value(args.get("name"), ctx, process, item)
        return data_cache.get(name)

    @staticmethod
    async def call(api, step, ctx=None, process=None, item=None):
        args = step["args"]
        name = await get_value(args.get("name"), ctx, process, item)
        method = await get_value(args.get("method"), ctx, process, item)
        args = await get_value(args.get("args"), ctx, process, item)
        return data_cache.call(name, method, args)

    @staticmethod
    async def get_perspective(api, step, ctx=None, process=None, item=None):
        args = step["args"]
        name = await get_value(args.get("name"), ctx, process, item)
        perspective = await get_value(args.get("perspective"), ctx, process, item)
        return data_cache.get_perspective(name, perspective)

    @staticmethod
    async def plot(api, step, ctx=None, process=None, item=None):
        args = step["args"]
        name = await get_value(args["name"], ctx, process, item)
        field = await get_value(args["field"], ctx, process, item)
        kind = await get_value(args.get("kind", "line"), ctx, process, item)
        title = await get_value(args.get("title", ""), ctx, process, item)
        ylabel = await get_value(args.get("ylabel", ""), ctx, process, item)
        xlabel = await get_value(args.get("xlabel", ""), ctx, process, item)
        file = await get_value(args.get("file", None), ctx, process, item)

        df = data_cache.get(name)
        df[field].plot(kind=kind, title=title, ylabel=ylabel, xlabel=xlabel)

        if file is not None:
            plt.savefig(file, dpi=300, bbox_inches='tight')

        #plt.show()