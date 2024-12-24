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

from qec import RotatedSurfaceCode


class TestRotatedSurfaceCode:

    @pytest.fixture(autouse=True)
    def init(self) -> None:
        self.code = RotatedSurfaceCode(
            distance = 3,
            depolarize1_rate = 0.01,
            depolarize2_rate = 0
            )

    def test_build_lattice(self):
        assert self.code.lattice == {(1, 1): 0, (2, 1): 1, (3, 1): 2, (1, 2): 3, (2, 2): 4, (3, 2): 5, (1, 3): 6, (2, 3): 7, (3, 3): 8, (2.5, 0.5): 9, (1.5, 1.5): 10, (2.5, 2.5): 11, (1.5, 3.5): 12, (0.5, 1.5): 13, (2.5, 1.5): 14, (1.5, 2.5): 15, (3.5, 2.5): 16}
        assert self.code.data_qubits == [0, 1, 2, 3, 4, 5, 6, 7, 8]
