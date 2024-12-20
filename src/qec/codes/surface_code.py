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

from stim import Circuit, target_rec

from qec.codes.twod_lattice import TwoDLattice

__all__ = ["SurfaceCode"]


class SurfaceCode(TwoDLattice):
    r"""
    A class for Surface code.
    """
    
    __slots__ = ()
    
    def __init__(
        self,
        *args, 
        **kwargs,
    ) -> None:
        r"""
        Initialize the Surface code instance.
        """
        super().__init__(*args, **kwargs)

    def build_memory_circuit(self, number_of_rounds: int = 2) -> None:
        r"""
        """
        pass
    
    def data_qubit_coords(self)->list[tuple]:
        r"""
        Return the coordinates of the data qubits which are of the form (i,i) where i range from 0 to distance-1 
        """
        return [(i,i) for i in range(self.distance)]

    def z_measure_coords(distance):
        r"""
        Return the coordinates of the Z measurments.
        """
        coords = [
            (col + (0.5 if row % 2 == 0 else -0.5), row + 0.5)
            for row in range(1, distance)
            for col in range(1, distance + 1, 2)
        ]
        return coords

    def x_measure_coords(distance):
        r"""
        Return the coordinates of the X measurements.
        """
        coords = [
            (col + (0.5 if row % 2 != 0 else -0.5), row - 0.5)
            for row in range(1, distance + 2)
            for col in range(2, distance, 2)
        ]
        return coords
