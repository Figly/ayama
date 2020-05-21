## Pre-commit
This project uses pre-commit checks to enforce linting and formatting standards. The following is checked/enforced:
1. Trailing white spaces
1. YAML file configuration
1. End of file breaks
1. Requirements text file format/package order

[Black](https://github.com/ambv/black) is used to auto-format the code base and [Flake8](https://gitlab.com/pycqa/flake8)
is used to check for conformance against PEP8 standards.

### Local pre-commit setup
Run the following from within the app's virtual environment:
1. `pip install pre-commit black flake8`
1. `pre-commit install`

### Usage
The pre-commit hooks are run with every `git commit`. In some cases files could be altered by the pre-commit hooks, the commit will
fail, and the files will need to be added to git tracking again before retrying the commit step.

An example could go like this:
1. Make changes to file
1. `git add <file> && git commit -m "message"`
1. Pre-commit runs, and fixes a formatting conflict using Black. The output message says the Black check failed, and files were altered.

At this point you can run `git status` and the file changes won't be added to tracking. Run `git add <file> && git commit -m "message"` again
and the commit should be successful if no other conflicts were picked up.
