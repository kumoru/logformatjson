=============
logformatjson
=============

``logformatjson`` is a library that provides a simple JSON formatter for the standard python logging package. It allows for nested arbitrary metadata to be inserted at instantian and run time.

Install
=======

via ``pip``:
        pip install logformatjson

Exmaples
========

1. Basic Usage:

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
          "log_version": "0.1"
        }

2. Adding an additional metadata in every log entry:

.. code-block:: python
        …

        log_handler.setFormatter(JSONFormatter(metadata={'application_version': '1.0.0'}))
        …


Tests
=====

Tests can be run via ``make``:

.. code-block:: shell
        make lint
        make unit

Authors
=======
* Ryan Richard <ryan@kumoru.io>
