from agents import set_default_openai_key
from openai import AsyncOpenAI
set_default_openai_key("")

custom=AsyncOpenAI(api_key="")

set_default_openai_key(custom)

from agents import set_tracing_export_api_key, set_tracing_disabled
set_tracing_export_api_key("")

set_tracing_disabled(True)


from agents import enable_verbose_stdout_logging
enable_verbose_stdout_logging()


import logging
logger=logging.getLogger("openai.agents")
logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)
logger.setLevel(logging.WARNING)
logger.addHandler(logging.StreamHandler())

