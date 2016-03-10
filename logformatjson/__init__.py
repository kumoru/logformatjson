# Copyright 2016 Kumoru.io
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''Main pyjsonlogging module.

This module provides a simple JSON formatter for the standard python
logging library. The provided log format is opionated but allows for a
number of overrides at the time the formatter is instantiated.

Example:
    See `README.md`_

Attributes:
    KEPT_ATTRS (Union[Tuple, list]): Attributes to be kept from the `LogRecord`_.
    SKIPPED_ATTRS (Union[Tuple, list]): Attributes to be skipped from the `LogRecord`_.

    .. _README.md:
        https://github.com/kumoru/logjsonformatter/README.md
'''

import json
import logging

from collections import OrderedDict
from datetime import datetime


KEPT_ATTRS = ('pathname', 'funcName', 'lineno', 'module', 'filename',)
SKIPPED_ATTRS = ('args', 'name', 'msecs', 'thread', 'process', 'exc_text',
                 'processName', 'created', 'stack_info', 'levelno',
                 'relativeCreated', 'threadName', 'exc_info', 'msg')


class JSONFormatter(logging.Formatter):
    '''JSON formatter for python logging.

    Attributes:
        kept_attrs (Union[Tuple, list]): Attributes to be kept from the `LogRecord`_.
        json_encoder (Callable[[], dict]): Function to call as `default` arg
                                           to `json.dumps`.
        log_version (str): Version of the log format.
        log_type (str): Arbitrary type to store in the metadata. Intended to
                        be useful for filtering.
        permanent_metadata (dict): metadata to be injected in every log. Maps
                                   to ``metadata`` keyword.
        skipped_attrs (Union[Tuple, list]): Attributes to be skipped from
                                          the `LogRecord`_.

    .. _LogRecord:
        https://docs.python.org/3.4/library/logging.html#logrecord-attributes

    '''

    def __init__(self, **kwargs):  # pylint: disable=missing-docstring
        super().__init__()

        self.json_encoder = kwargs.get('json_encoder', self.json_encode)
        self.kept_attrs = kwargs.get('kept_attrs', KEPT_ATTRS)
        self.log_version = kwargs.get('log_version', '1.0')
        self.log_type = kwargs.get('log_type', 'python')
        self.permanent_metadata = kwargs.get('metadata', {})
        self.skipped_attrs = kwargs.get('skipped_attrs', SKIPPED_ATTRS)


    def extra_metadata(self):
        '''Metadata to be inserted into every log.

        You may override this method to force certain keys be written to every
        log.

        Returns:
            Dictionary to be inserted.

        '''

        return self.permanent_metadata


    def get_timestamp(self):  # pylint: disable=no-self-use
        '''Get the preferred datetime format.

        Returns:
            datetime.utcnow().isoformat()
        '''

        return datetime.utcnow().isoformat()


    def json_encode(self, obj):  #pylint: disable=no-self-use
        '''Basic JSON encoder.

        A naive json_encoder that will return unmodified objects if their type
        is accepted in JSON or a string otherwise.

        Override this method or pass a different function when instantiating
        the formatter to implement your own encoder.

        Args:
            obj (Object): Object to be encoded in acceptable JSON type.

        Returns:
            Stringified object or object as is.

        '''

        try:
            if isinstance(obj, (bool, str, int, float, None,)):
                return obj
        except TypeError:
            pass

        return str(obj)


    def jsonify(self, log):
        '''Sane default for json.dumps

        You may override this method if you want to change the behaviour of
        `json.dumps`

        Args:
            log (Dict): Python dict to be converted to JSON

        Returns:
            JSON string

        '''

        return json.dumps(log, default = self.json_encoder)


    def format(self, record):
        '''Format the given record with specifics.

        This method does the heavy lifting of formatting the standard
        `LogRecord` with the various desired attributes.

        Note:
            ``log_type`` can be overriden with the ``log_type`` keyword.
            ``extra`` keyword containing a dictionary be added to the log.

        Args:
            record (Object): `LogRecord` to be converted

        Returns:
            JSON string to be logged.

        '''

        new_record = OrderedDict()

        new_record['timestamp'] = self.get_timestamp()
        new_record['message'] = record.getMessage()
        new_record['levelname'] = record.__dict__.pop('levelname')

        new_record.update(OrderedDict({'metadata': {'extra': {}}}))
        new_record['metadata']['log_type'] = self.log_type
        new_record['metadata'].update(self.extra_metadata())
        for key, value in record.__dict__.items():
            if key in self.kept_attrs:
                new_record['metadata'][key] = value
            elif key not in self.skipped_attrs:
                new_record['metadata']['extra'][key] = value

        new_record['log_version'] = self.log_version

        if record.exc_info:
            new_record['metadata']['exception'] = self.formatException(record.exc_info)

        return "%s" % (self.jsonify(new_record))

