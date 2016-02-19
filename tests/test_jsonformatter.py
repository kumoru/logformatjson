# pylint: disable=missing-docstring
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

import json
import logging
import uuid

from logformatjson import JSONFormatter

class TestJsonFormatter():
    '''logformatjson.JSONFormatter'''


    def test_init(self):  # pylint: disable=no-self-use
        '''logformatjson.JSONFormatter.__init__() -> JSONFormatter'''

        _ = JSONFormatter()
        assert isinstance(_, JSONFormatter)

    def test_custom_attrs(self):  # pylint: disable=no-self-use
        '''logformatjson.JSONFormatter(…) -> JSONFormatter.…'''

        def fake_encoder():  # pylint: disable=missing-docstring
            pass

        _ = JSONFormatter(
            json_encoder = fake_encoder,
            kept_attrs = ['foo'],
            log_version = '9.9',
            log_type = 'test',
            metadata = {'a': 'b'},
            skipped_attrs = []
        )

        assert _.json_encoder == fake_encoder
        assert _.kept_attrs == ['foo']
        assert _.log_version == '9.9'
        assert _.log_type == 'test'
        assert _.permanent_metadata == {'a': 'b'}
        assert _.skipped_attrs == []

    def test_json_encode(self):  # pylint: disable=no-self-use
        '''pyjsonloggin.JSONFormatter.json_encode(UUID()) -> str(uuid)'''

        _ = JSONFormatter()
        result = _.json_encode('a')

        assert isinstance(result, str)

        my_uuid = uuid.uuid4()
        result = _.json_encode(my_uuid)
        assert result == str(my_uuid)

    def test_jsonify(self):  # pylint: disable=no-self-use
        '''logformatjson.JSONFormatter.jsonify() -> {"test": "log"}'''

        _ = JSONFormatter()
        result = _.jsonify({'test': 'log'})

        assert result == '{"test": "log"}'

    def test_extra_metadata(self):  # pylint: disable=no-self-use
        '''logformatjson.JSONFormatter.extra_metadata() -> {'a':'b'}'''

        _ = JSONFormatter(metadata = {'a': 'b'})
        result = _.extra_metadata()

        assert result == {'a': 'b'}

    def test_format_standard(self, mocker):
        '''logformatjson.JSONFormatter.format() -> {"timstamp": "…"}'''
        _ = JSONFormatter()

        mocker.patch.object(JSONFormatter, 'get_timestamp', autospec=True, return_value = '2016-02-19T15:00:52.469601')  # pylint: disable=line-too-long

        record = logging.LogRecord('testLogRecord', 'debug', '/test.py', 1, '%s', 'a', None, func=self, sinfo=None,)  # pylint: disable=line-too-long
        result = json.loads(_.format(record))

        assert result['timestamp'] == '2016-02-19T15:00:52.469601'
        assert result['message'] == 'a'
        assert result['log_version'] == '0.1'
        assert result['levelname'] == 'Level debug'
