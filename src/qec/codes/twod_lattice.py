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
from abc import abstractmethod

from stim import Circuit, target_rec

from qec.codes.base_code import BaseCode

__all__ = ["TwoDLattice"]


class TwoDLattice(BaseCode):
    r"""
    A Parent class for 2D Lattice code.
    """
    
    __slots__ = ("_lattice")
    
    def __init__(
        self,
        *args, 
        **kwargs,
    ) -> None:
        r"""
        Initialize the 2D Lattice code instance.
        """
        super().__init__(*args, **kwargs)
        self._lattice: dict[tuple[float, float], int]
        
    @property
    def lattice(self)->dict[tuple[float, float], int]:
        r"""
        Return the lattice coordinates.
        """
        return self._lattice
    
    @abstractmethod
    def build_lattice(self):
        r"""
        Build the 2D lattice.
        """
        pass
        
    def build_memory_circuit(self, number_of_rounds: int = 2) -> Circuit:        
        pass