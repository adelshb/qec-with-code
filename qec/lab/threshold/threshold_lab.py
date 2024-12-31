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

from __future__ import annotations

from qec.codes.base_code import BaseCode

__all__ = ["ThresholdLAB"]


class ThresholdLAB:
    r"""
    A class for wrapping threshold calculation
    """

    __slots__ = ("_distances", "_error_rate", "_code")

    def __init__(
        self, code: BaseCode, distances: list[int], error_rates: list[float]
    ) -> None:
        r"""
        Initialization of the Base Code class.

        :param code: The code
        :param distances: Distances for the code.
        :param error_rates: Error rate.
        """

        self._distances = distances
        self._code = code
        self._error_rates = error_rates

    @property
    def distances(self) -> list[int]:
        r"""
        The distances of the code.
        """
        return self._distances

    @property
    def error_rates(self) -> list[float]:
        r"""
        The error rates.
        """
        return self._error_rate

    @property
    def code(self) -> BaseCode:
        r"""
        The code.
        """
        return self._code
