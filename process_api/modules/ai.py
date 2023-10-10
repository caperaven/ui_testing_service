from transformers import pipeline, AutoTokenizer, AutoConfig

from process_api.utils.get_value import get_value


class PipelineCache:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PipelineCache, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        self.store = {}

    def get(self, name):
        return self.store.get(name, None)

    def load(self, name, pipeline_settings):
        if name in self.store:
            return self.store[name]

        model = pipeline_settings.get("model", None)
        tokenizer = AutoTokenizer.from_pretrained(model)
        config = AutoConfig.from_pretrained(model)

        pipeline_settings["tokenizer"] = tokenizer
        pipeline_settings["config"] = config
        self.store[name] = pipeline(**pipeline_settings)
        return self.store[name]

    def unload(self, name):
        del self.store[name]


pipeline_cache = PipelineCache()


class AiModule:

    @staticmethod
    def register(api):
        api.add_module("ai", AiModule)

    @staticmethod
    async def perform(api, step, ctx=None, process=None, item=None):
        await AiModule.load(api, step, ctx, process, item)
        return await AiModule.execute(api, step, ctx, process, item)

    @staticmethod
    async def load(api, step, ctx=None, process=None, item=None):
        args = step["args"]
        name = await get_value(args.get("name"), ctx, process, item)
        pipeline_settings = await get_value(args.get("pipeline"), ctx, process, item)
        pipeline_cache.load(name, pipeline_settings)
        return True

    @staticmethod
    async def unload(api, step, ctx=None, process=None, item=None):
        args = step["args"]
        name = await get_value(args.get("name"), ctx, process, item)
        pipeline_cache.unload(name)
        return True

    @staticmethod
    async def execute(api, step, ctx=None, process=None, item=None):
        args = step["args"]
        pipe_input = await get_value(args.get("input"), ctx, process, item)

        execute = pipeline_cache.get(args.get("name"))
        if execute is None:
            raise Exception("Pipeline not loaded")

        if isinstance(pipe_input, dict):
            return execute(**pipe_input)
        else:
            return execute(pipe_input)


