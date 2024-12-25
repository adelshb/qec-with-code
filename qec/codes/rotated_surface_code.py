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

__all__ = ["RotatedSurfaceCode"]


class RotatedSurfaceCode(TwoDLattice):
    r"""
    A class for the Rotated Surface code.
    """

    __slots__ = ("_data_qubits", "_x_qubits", "_z_qubits", "_check_qubits")

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        r"""
        Initialize the Rotated Surface Code instance.
        """

        super().__init__(*args, **kwargs)
        self.build_lattice()

    @property
    def data_qubits(self) -> list:
        r"""
        The data qubits.
        """
        return self._data_qubits

    @property
    def check_qubits(self) -> list:
        r"""
        The check qubits.
        """
        return self._check_qubits

    @property
    def x_qubits(self) -> dict:
        r"""
        The qubits for X checks.
        """
        return self._x_qubits

    @property
    def z_qubits(self) -> dict:
        r"""
        The qubits for Z checks.
        """
        return self._z_qubits

    def build_memory_circuit(self, number_of_rounds: int = 2) -> None:
        r"""
        Build and return a Stim Circuit object implementing a memory for the given time.

        :param number_of_rounds: The number of rounds in the memory.
        """

        # Initialization
        self._memory_circuit = Circuit()

        self._memory_circuit.append("R", [q for q in self.lattice.values()])
        self._memory_circuit.append(
            "DEPOLARIZE1", [q for q in self.lattice.values()], self.depolarize1_rate
        )

        self.append_stab_circuit(round=0)

        for i in range(len(self.z_qubits.keys())):
            self._memory_circuit.append("DETECTOR", [target_rec(-1 - i)])

        # Body rounds
        for round in range(1, number_of_rounds):

            self.append_stab_circuit(round=round)

            for i in range(len(self.check_qubits)):
                self._memory_circuit.append(
                    "DETECTOR",
                    [target_rec(-1 - i), target_rec(-1 - i - len(self.check_qubits))],
                )

        # Finalization

        self._memory_circuit.append(
            "DEPOLARIZE1", [q for q in self.data_qubits], self.depolarize1_rate
        )
        self._memory_circuit.append("MR", [q for q in self.data_qubits])
        for i, q in enumerate(self.data_qubits):
            self.add_outcome(
                outcome=target_rec(-1 - i), qubit=q, round=number_of_rounds, type="data"
            )

        for qz in self.z_qubits.keys():

            qz_adjacent_data_qubits = [
                self.lattice[i] for i in self.z_qubits[qz] if i in self.lattice.keys()
            ]

            recs = [
                self.get_target_rec(qubit=qd, round=number_of_rounds)
                for qd in qz_adjacent_data_qubits
            ]
            recs += [self.get_target_rec(qubit=qz, round=number_of_rounds - 1)]
            self._memory_circuit.append("DETECTOR", [target_rec(r) for r in recs])

        # Adding the comparison with the expected state
        ql = [self.lattice[(i + 1, i + 1)] for i in range(self.distance)]
        recs = [self.get_target_rec(qubit=q, round=number_of_rounds) for q in ql]
        recs_str = " ".join(f"rec[{rec}]" for rec in recs)
        self._memory_circuit.append_from_stim_program_text(
            f"OBSERVABLE_INCLUDE(0) {recs_str}"
        )

    def append_stab_circuit(self, round: int) -> None:
        r"""
        Append the stabilizer circuit.
        """

        self._memory_circuit.append("H", [q for q in self.x_qubits.keys()])
        self._memory_circuit.append(
            "DEPOLARIZE1", [q for q in self.x_qubits.keys()], self.depolarize1_rate
        )

        # Perform CNOTs with specific order to avoid hook errors
        for i in range(4):
            for q in self.z_qubits.keys():
                try:
                    control = self.lattice[self.z_qubits[q][i]]
                    self._memory_circuit.append("CNOT", [control, q])
                    self._memory_circuit.append(
                        "DEPOLARIZE2", [control, q], self.depolarize2_rate
                    )
                except KeyError:
                    pass

            for q in self.x_qubits:
                try:
                    target = self.lattice[self.x_qubits[q][i]]
                    self._memory_circuit.append("CNOT", [q, target])
                    self._memory_circuit.append(
                        "DEPOLARIZE2", [target, q], self.depolarize2_rate
                    )
                except KeyError:
                    pass

        self._memory_circuit.append("H", [q for q in self.x_qubits.keys()])
        self._memory_circuit.append(
            "DEPOLARIZE1", [q in self.x_qubits.keys()], self.depolarize1_rate
        )

        self._memory_circuit.append(
            "DEPOLARIZE1", [q in self.check_qubits], self.depolarize1_rate
        )
        self._memory_circuit.append("MR", [q for q in self.check_qubits])
        for i, q in enumerate(self.check_qubits):
            self.add_outcome(
                outcome=target_rec(-1 - i), qubit=q, round=round, type="check"
            )

    def build_lattice(self) -> None:
        r"""
        Compute the coordinates of the data qubits, the z and x measurements.
        """

        # Compute coordinates of the data qubits
        data_qubits_coords = [
            (col, row)
            for row in range(1, self.distance + 1)
            for col in range(1, self.distance + 1)
        ]

        # Compute the coordinates of the X qubits measurements.
        x_qubits_coords = [
            (col + (0.5 if row % 2 != 0 else -0.5), row - 0.5)
            for row in range(1, self.distance + 2)
            for col in range(2, self.distance, 2)
        ]

        # Compute the coordinates of the Z qubits measurements.
        z_qubits_coords = [
            (col + (0.5 if row % 2 == 0 else -0.5), row + 0.5)
            for row in range(1, self.distance)
            for col in range(1, self.distance + 1, 2)
        ]

        self._lattice = {
            tuple(c): i
            for i, c in enumerate(
                data_qubits_coords + x_qubits_coords + z_qubits_coords
            )
        }
        self._number_of_qubits = len(self.lattice)

        self._data_qubits = [self._lattice[coord] for coord in data_qubits_coords]
        self._check_qubits = [
            q for q in self._lattice.values() if q not in self.data_qubits
        ]

        index_reorder_x = [1, 3, 0, 2]
        self._x_qubits = {
            self._lattice[coord]: [
                self.get_adjacent_coords(coord)[i] for i in index_reorder_x
            ]
            for coord in x_qubits_coords
        }

        index_reorder_z = [1, 0, 3, 2]
        self._z_qubits = {
            self._lattice[coord]: [
                self.get_adjacent_coords(coord)[i] for i in index_reorder_z
            ]
            for coord in z_qubits_coords
        }

    @staticmethod
    def get_adjacent_coords(coord: tuple[float, float]) -> list[tuple[float, float]]:
        r"""
        Returns the four diagonal coordinates, ordered as:
        - top-left,
        - top-right,
        - bottom-left,
        - bottom-right.

        :param coords: The coordinates of the vertex we want to have the neighboors.
        """
        col, row = coord
        return [(col + dx, row + dy) for dx in [-0.5, 0.5] for dy in [-0.5, 0.5]]
