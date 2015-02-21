Running the server
==================

There are a few different ways that you can start the server:

1. Importing it in a ``wsgi`` file, for a minimal setup all you need is::

    from pryvate.server import app

2. You can start it via the console script exposed from the installation::

    $ pryvate-server


I'd recommend #1 as #2 uses Flasks built in http server which is not suited
for production loads. Read more here to find your preferred deploy scheme: http://flask.pocoo.org/docs/0.10/deploying/
