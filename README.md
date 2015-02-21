[![Build Status](https://travis-ci.org/Dinoshauer/pryvate.svg?branch=master)](https://travis-ci.org/Dinoshauer/pryvate)
[![Coverage Status](https://coveralls.io/repos/Dinoshauer/pryvate/badge.png)](https://coveralls.io/r/Dinoshauer/pryvate)
[![Documentation Status](https://readthedocs.org/projects/pryvate/badge/?version=latest)](https://readthedocs.org/projects/pryvate/?badge=latest)


Pryvate
=======

Private PyPi repository and proxy supporting:

* [x] `python setup.py sdist upload...`
* [x] `python setup.py sdist register...`
* [x] Downloading private and public packages
* [x] Configurable
* [ ] Caching packages - *Won't happen right now.*

# TODO:

* [x] Tests
* [x] Sphinx docs
    * [x] Write better docstrings
* [ ] Find a better datastore than a variable
* [ ] Put on the cheeseshop
* [x] TravisCI
* [ ] ReadTheDocs

# Usage:

## Configuration:

Since `pryvate` is a flask app, it uses flask based [configuration schemes][0].
All you need to configure `pryvate` is to create a python file with
`UPPER_CASED_VARIABLE_NAMES`, those variables are the only ones that will be
read by flask.

Pryvate is expecting an `env var` called `PRYVATE_CONFIG` and will look in that
variables value for the path to the config file

### Example

Here's a very small example:

    $ cat config.py
    PRIVATE_EGGS = {'foo'}

### Available configuration parameters

*In case I ever forget to update this list, you can always find the available*
*parameters in [`pryvate.defaultconfig`][1]*

* `BASEDIR`: Where private eggs will be stored
    * *Default:* `./eggs/`
    * *Note:* Pryvate will try to create the directory upon start if it doesn't
      exist yet
* `PYPI`: The base url from where to download eggs that are not stored in
  pryvate
    * *Default:* `https://pypi.python.org{}`
* `PRIVATE_EGGS`: A `set()` of egg names
    * *Note:* All names should be lowercase

[0]: http://flask.pocoo.org/docs/0.10/config/
[1]: pryvate/defaultconfig.py
