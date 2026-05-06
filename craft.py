import subprocess
from glob import glob
from time import time
from models import Team, filestamp

def go_model(context: str, file: str, model: str, job: str) -> None:
    '''run Ollama model w/ context, input file, model, job'''
    cmd = ['ollama', 'run', f'{model}-{job}', '--nowordwrap', context]
    try:
        tic = time()
        if file:
            with open(file) as f:
                proc = subprocess.run(cmd, input=f.read(),
                                       text=True, capture_output=True)
        else:
            proc = subprocess.run(cmd, text=True, capture_output=True)
        with open(filestamp(model, job, file), 'w') as f:
            _ = f.write(proc.stdout)
        print(f'..{model} took {(time() - tic):.1f}s')
    except subprocess.CalledProcessError as e:
        print(f'Command failed: {e}')

def go_team(context: str, file: list[str] | str,
                           use: list[str] | str, job: str) -> None:
    '''run Ollama models w/ context, input file/s, model/s, job'''
    tic = time()
    files = file if isinstance(file, list) else (
        [x for x in glob(file)] if '*' in file else [file])
    models = use if isinstance(use, list) else (
        [x[0] for x in Team.coders] if use == 'all' else [use])
    for model in models:
        for file in files: # do all tasks w/ model
            go_model(context, file, model, job)
    if len(files) > 2 + len(models):
        print(f'TOTAL TIME: {(time() - tic):.1f}s')

# SHORTCUTS
def ask(context: str='', file: str='', use: str=Team.coders[0][0]):
    go_team(context, file, use, 'ask')
def see(context: str='', file: str='', use: str=Team.coders[0][0]):
    go_team(context, file, use, 'see')
def plan(context: str='', file: str='', use: str=Team.coders[0][0]):
    go_team(context, file, use, 'plan')
def code(context: str='', file: str='', use: str=Team.coders[0][0]):
    go_team(context, file, use, 'code')
def q(context: str='', file: str='', use: str=Team.coders[0][0]):
    go_team(context, file, use, 'q')
