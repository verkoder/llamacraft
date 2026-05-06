from dataclasses import dataclass

@dataclass
class Context:
    LOW: int = 2048
    DEFAULT: int = 8192
    HIGH: int = 16384

@dataclass
class Temperature:
    LOW: float = 0.1
    DEFAULT: float = 0.8
    HIGH: float = 0.95

@dataclass
class TopK:
    LOW: int = 10
    DEFAULT: int = 40
    HIGH: int = 80

@dataclass
class TopP:
    LOW: float = 0.5
    DEFAULT: float = 0.9
    HIGH: float = 0.98

@dataclass
class Team:
    alias: str = "alias {}='ollama run {}' --keepalive 10m"
    coders: tuple[tuple[str, str], ...] = ( # first is default
        ('deep', 'second_constantine/deepseek-coder-v2:16b'),
        ('qwen', 'sparksammy/qwen3-coder-30b-unsloth:small-fixed'),
        ('cog', 'cogito:14b'),
    )
    helper: str = 'frob/qwen3.5-instruct:9b'
    num_ctx: int = Context.HIGH
    output: str = './output/'
    temperature: float = Temperature.LOW # creativity
    top_k: int = TopK.LOW # chance of nonsense
    top_p: float = TopP.LOW

def filestamp(model: str, job: str, file: str) -> str:
    '''generate filename path as ./output/model_job_file.ext'''
    file = f"_{file.split('.')[0].replace('/', '-')}" if file else ''
    ext = 'py' if job == 'code' else 'md'
    return f'{Team.output}{model}_{job}{file}.{ext}'
