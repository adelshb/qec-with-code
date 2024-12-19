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

from stim import Circuit

__all__ = ["QEC"]


class QEC():
    r"""
    An abstract base class for quantum error correction codes.
    """
    
    __slots__ = ("_distance")
    
    def __init__(
        self,
        distance: int
    ) -> None:
        
        self._distance = distance
        
    @property
    def distance(self) -> int:
        r"""
        The distance of the code
        """
        return self._distance
    
    @abstractmethod
    def build_memory_circuit(self, time: int) -> Circuit:
        r"""
        Build and return a Stim Circuit object implementing a memory for the given time.
        """
