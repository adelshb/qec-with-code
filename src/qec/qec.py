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
from abc import ABC, abstractmethod

from numpy import ndarray
from stim import Circuit

__all__ = ["QEC"]


class QEC():
    r"""
    An abstract base class for quantum error correction codes.
    """
    
    __slots__ = ("_distance", "_memory_circuit", "_parity_data")
    
    def __init__(
        self,
        distance: int
    ) -> None:
        
        self._distance = distance
        self._memory_circuit: Circuit
        self._parity_data: list[ndarray] = []
         
    @property
    def distance(self) -> int:
        r"""
        The distance of the code
        """
        return self._distance
    
    @property
    def memory_circuit(self) -> Circuit:
        r"""
        The circuit for the memory.
        """
        return self._memory_circuit
    
    @property
    def parity_data(self) -> ndarray:
        r"""
        The parity data for the last experiment.
        """
        return self._memory_circuit
    
    @abstractmethod
    def build_memory_circuit(self, time: int) -> None:
        r"""
        Build and return a Stim Circuit object implementing a memory for the given time.
        """

    @abstractmethod
    def collect_parity_data(self, num_samples: int) -> None:
        r"""
        Run Stim sampling experiment and get measurement data.
        """
