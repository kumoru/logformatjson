=============
logformatjson
=============

``logformatjson`` is a library that provides a simple JSON formatter for the standard python logging package. It allows for nested arbitrary metadata to be inserted at instantiation and run time. The library is opionanted but attempts to allow most opinions to be overridden.

**warning**: This library is under active development. The log format and API are expected to change.

.. image:: https://circleci.com/gh/kumoru/logformatjson.svg?style=svg
    :target: https://circleci.com/gh/kumoru/logformatjson


Install
-------

* via ``pip``:

.. code-block:: shell

        pip install logformatjson

Examples
========

1. basic usage - JSONFormatter can be set on any handler as your would expect:

.. code-block:: python

        import logging
        import sys
        from logformatjson import JSONFormatter

        LOGGER = logging.getLogger()
        LOGGER.setLevel(logging.DEBUG)
        log_handler = logging.StreamHandler(sys.stdout)
        log_handler.setFormatter(JSONFormatter())
        LOGGER.addHandler(log_handler)

        LOGGER.debug('this is my debug message', extra={'some_key': 'important_value'})

which produces the following json (from ipython):

.. code-block:: javascript

        {
          "timestamp": "2016-02-19T19:39:17.061886",
          "message": "this is my debug message",
          "levelname": "DEBUG",
          "metadata": {
            "filename": "test.py",
            "funcName": "<module>",
            "extra": {
              "some_key": "important_value"
            },
            "log_type": "python",
            "lineno": 11,
            "module": "test",
            "pathname": "test.py"
          },
          "log_version": "1.0"
        }

2. Adding an additional metadata in **every** log entry:

.. code-block:: python

        …
        log_handler.setFormatter(JSONFormatter(metadata={'application_version': '1.0.0'}))
        …

3. Overriding the defaults at instantiation:

    * Override attributes copied or skipped from the LogRecord_:
        .. code-block:: python

                …
                log_handler.setFormatter(JSONFormatter(kept_attrs= ['created', …]))
                log_handler.setFormatter(JSONFormatter(skipped_attrs= ['filename', …]))
                …

    * Override the provided json encoder:

        .. code-block:: python

                def my_json_encoder(obj):
                  return int(obj)

                …
                log_handler.setFormatter(JSONFormatter(json_encoder = my_json_encoder))
                …




4. Override the defaults at runtime:

    * Log type (intended to be mixed with extra fields):

        .. code-block:: python

                …
                logger.debug('GET / HTTP/1.1', log_type='HTTP'}
                …

5. Extra fields:

        .. code-block:: python

                …
                LOGGER.debug('this is my debug message', extra={'some_key': 'important_value'})
                …


.. _LogRecord: https://docs.python.org/3.4/library/logging.html#logrecord-attributes

Tests
=====

Tests can be run via ``make``:

.. code-block:: shell

        make lint
        make test

Authors
=======
* Ryan Richard <ryan@kumoru.io>
