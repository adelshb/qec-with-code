# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from qec import Measurement


class TestMeasurement:

    @pytest.fixture(autouse=True)
    def init(self) -> None:
        self.measurement = Measurement()

    def test_init(self):
        assert isinstance(self.measurement, Measurement)
        
    def test_add_and_get_measurement(self):
        self.measurement.add_outcome(
            outcome='0',
            qubit=0,
            round=1,
            type='check'
        )
        assert self.measurement.get_outcome(qubit=0,round=1) == '0'
