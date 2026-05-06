LlamaCraft: Model Teams Made Simple
===================================
LlamaCraft is an Ollama micro-scaffold for LLM assistants. Users can quickly build a team of custom local LLM variants to fit their needs. The resulting team can then be asked to offer parallel approaches to problems and tasks.

Why?
----

Running local LLMs is both convenient and cheap, but the additional overhead of coding agents and large contexts quickly adds up. LlamaCraft runs Ollama directly with little overhead, letting users add bare-minimum contexts for each task. The structure is simple, but can create and direct dozens of custom model variants. In a Python shell, LlamaCraft allows for LLM inquiries alongside other work.

Requirements
------------

Install Ollama, and pull a model or two. The starter models listed punch above their weight in under 16 GB memory, but adjust for your needs and hardware.

Building a Model Team
=====================

Download LlamaCraft, and modify these two files:
- `models.py` Edit according to your Ollama setup. The Team class contains the default settings, the base helper model, and the base list of nickname/model name pairs. The model names must match a pulled model shown in your 'ollama ls' results.
- `traits.py` Edit according to your LLM needs. The default includes four Python coding assistants, plus helpers for cooking, housework & fun. The helpers spawn from a single model with different traits. The coders spawn by multiple models and traits, so with three models and four job traits, LlamaCraft creates twelve Ollama model variants.

From a command-line, enter `python build.py` to create the model team. A list of commands will be printed to the screen. Enter `python build.py rm` to remove the team from Ollama.

Using the Coder Models
======================

Load the coding assistants in a Python shell:
    from craft import *

Four job methods can be called:
    ask("Load CSV") # coding assistant
    see(file="feeds.py") # code reviewer
    plan("Authorize login via Facebook") # code planner
    code("Django form for Feed class", "feeds.py") # code writer

All 4 jobs have the same 3 keyword arguments (kwargs):
- context: input text; default=None
- file: filename or list; default=None
- use: model or list; 'all' for all models; default to first Team.coders model

LLM output is written to ./output as:
- .md files (see, ask, or plan results)
- .py files (code results)

To use different models:
    code("Django form for Feed class", "feeds.py", ["qwen", "cog"])
A separate output file will be written by each model.

To input multiple files, use a list of files, or glob notation:
    see("Find and report bugs", "./data/load_*.py")

Using the Helper Models
=======================

(If you only want coding help in a Python shell, skip this section)

Copy the printed commands, and paste to your shell resource file, bash_profile/zshrc/etc.

Restart the shell. The helper models can be called by nickname:
    > food 'chickpea onion recipes'
Sure! Here are some chickpea and onion recipes...

The coder models can be called by nickname-job:
    > cog-code 'sort a dict by name, state, and age'
Sure! Here's a dictionary-sorting algorithm...

Customizing
-----------

LlamaCraft is just 4 files, ~200 lines of code. Being tiny makes it easy to customize:
- Change setup -> build.py: methods to create the team of model variants
- Change jobs -> craft.py: methods to ask, see, plan, and code
- Change LLMs -> models.py: the Team class containing Ollama defaults
- Change behavior -> traits.py: specs defining the team of model variants
