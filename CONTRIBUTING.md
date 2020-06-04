## Contributing

First fork this project.

* git clone https://github.com/YOURNAMEHERE/dotifi
- Install [Graphviz](https://graphviz.org)
- Clone, fork, or download the [source](https://github.com/palindromicity/dotifi)
- Install [poetry](https://python-poetry.org/docs/)
- If required setup [pyenv](https://github.com/pyenv/pyenv) or your preference to get a python 3.8 environment, as poetry will use whatever the current python is.
    - for example setup pyenv local to the project directory
- In the source route directory run `poetry install`, this will install all the dependencies
- Run `peotry run pytest -v` to run the tests and ensure things are working
* git checkout -b my-fix upstream/master

#### fix some code...

* git commit -m "added this feature"
* git push origin my-fix

Lastly, open a pull request on Github.
