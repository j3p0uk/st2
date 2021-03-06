# -*- coding: utf-8 -*-

# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from integration.orchestra import base
from st2client import models
from st2common.constants import action as ac_const


class DatastoreFunctionTest(base.TestWorkflowExecution):
    @classmethod
    def set_kvp(cls, name, value, scope='system', secret=False):
        kvp = models.KeyValuePair(
            id=name,
            name=name,
            value=value,
            scope=scope,
            secret=secret
        )

        cls.st2client.keys.update(kvp)

    @classmethod
    def del_kvp(cls, name, scope='system'):
        kvp = models.KeyValuePair(
            id=name,
            name=name,
            scope=scope
        )

        cls.st2client.keys.delete(kvp)

    def test_st2kv_system_scope(self):
        key = 'lakshmi'
        value = 'kanahansnasnasdlsajks'

        self.set_kvp(key, value)
        wf_name = 'examples.orchestra-st2kv'
        wf_input = {'key_name': 'system.%s' % key}
        execution = self._execute_workflow(wf_name, wf_input)

        output = self._wait_for_completion(execution)

        self.assertEqual(output.status, ac_const.LIVEACTION_STATUS_SUCCEEDED)
        self.assertIn('output', output.result)
        self.assertIn('value', output.result['output'])
        self.assertEqual(value, output.result['output']['value'])
        self.del_kvp(key)

    def test_st2kv_user_scope(self):
        key = 'winson'
        value = 'SoDiamondEng'

        self.set_kvp(key, value, 'user')
        wf_name = 'examples.orchestra-st2kv'
        wf_input = {'key_name': key}
        execution = self._execute_workflow(wf_name, wf_input)

        output = self._wait_for_completion(execution)

        self.assertEqual(output.status, ac_const.LIVEACTION_STATUS_SUCCEEDED)
        self.assertIn('output', output.result)
        self.assertIn('value', output.result['output'])
        self.assertEqual(value, output.result['output']['value'])
        # self.del_kvp(key)

    def test_st2kv_decrypt(self):
        key = 'kami'
        value = 'eggplant'

        self.set_kvp(key, value, secret=True)
        wf_name = 'examples.orchestra-st2kv'
        wf_input = {
            'key_name': 'system.%s' % key,
            'decrypt': True
        }

        execution = self._execute_workflow(wf_name, wf_input)

        output = self._wait_for_completion(execution)

        self.assertEqual(output.status, ac_const.LIVEACTION_STATUS_SUCCEEDED)
        self.assertIn('output', output.result)
        self.assertIn('value', output.result['output'])
        self.assertEqual(value, output.result['output']['value'])
        self.del_kvp(key)
