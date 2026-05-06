import os
import sys
import ollama
from models import Team
from traits import CODER_TRAITS, HELPERS

def make_model(name: str,
                 spec:  dict[str, str | float | int],
                 delete_flag: bool)-> tuple[str, bool]:
    '''make Ollama model from dictionary, or delete by flag'''
    try:
        if delete_flag:
            resp = ollama.delete(name)
            return f'Deleted [{name}] {resp.status}!', False
        ollama.create(name, parameters=dict(
                temperature=spec.get('temperature', Team.temperature),
                top_k=spec.get('top_k', Team.top_k),
                top_p=spec.get('top_p', Team.top_p)),
            from_=spec.get('model', Team.helper),
            system=spec.get('trait', Team.trait))
        print(f'Created [{name}]', spec)
        return Team.alias.format(name, name), True
    except Exception as e:
        return f'Failed at [{name}]: {e}', False

def make_team(delete_flag: bool) -> None:
    '''make Ollama coder/helper model team, or delete by flag'''

    results: list[str] = []
    success: bool = True
    for name,model in Team.coders:
        spec = {'model': model} # reset model
        result, made = make_model(f'{name}-ask', spec, delete_flag)
        results.append(result)
        success &= made
        for job,trait in CODER_TRAITS.items():
            spec['trait'] = trait # reuse model w/ new trait
            result, made = make_model(f'{name}-{job}', spec, delete_flag)
            results.append(result)
            success &= made

    for name,spec in HELPERS.items():
        result, made = make_model(name, spec, delete_flag)
        results.append(result)
        success &= made

    print('ADD THESE SHELL COMMANDS:' if success else 'RESULT:')
    print('\n'.join(results))

if __name__ == '__main__':
    if not os.path.exists(Team.output):
        os.makedirs(Team.output) # verify output folder
    delete_flag = len(sys.argv) > 1 and sys.argv[1] == 'rm'
    make_team(delete_flag)
