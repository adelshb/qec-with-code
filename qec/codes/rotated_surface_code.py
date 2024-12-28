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

from qec.codes.base_code import BaseCode

__all__ = ["RotatedSurfaceCode"]


class RotatedSurfaceCode(BaseCode):
    r"""
    A class for the Rotated Surface code.
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        r"""
        Initialize the Rotated Surface Code instance.
        """

        super().__init__(*args, **kwargs)

    def build_memory_circuit(self, number_of_rounds: int = 2) -> None:
        r"""
        Build and return a Stim Circuit object implementing a memory for the given time.

        :param number_of_rounds: The number of rounds in the memory.
        """

        all_qubits = [q for q in self.graph.nodes()]
        data_qubits = [
            node
            for node, data in self.graph.nodes(data=True)
            if data.get("type") == "data"
        ]
        x_qubits = [
            node
            for node, data in self.graph.nodes(data=True)
            if data.get("type") == "X-check"
        ]
        z_qubits = [
            node
            for node, data in self.graph.nodes(data=True)
            if data.get("type") == "Z-check"
        ]

        # Initialization
        self._memory_circuit = Circuit()

        self._memory_circuit.append("R", all_qubits)
        self._memory_circuit.append("DEPOLARIZE1", all_qubits, self.depolarize1_rate)

        self.append_stab_circuit(
            round=0, data_qubits=data_qubits, x_qubits=x_qubits, z_qubits=z_qubits
        )

        for i in range(len(z_qubits)):
            self._memory_circuit.append("DETECTOR", [target_rec(-1 - i)])

        # Body rounds
        for round in range(1, number_of_rounds):

            self.append_stab_circuit(
                round=round,
                data_qubits=data_qubits,
                x_qubits=x_qubits,
                z_qubits=z_qubits,
            )

            for i in range(len(x_qubits + z_qubits)):
                self._memory_circuit.append(
                    "DETECTOR",
                    [target_rec(-1 - i), target_rec(-1 - i - len(x_qubits + z_qubits))],
                )

        # Finalization
        self._memory_circuit.append("DEPOLARIZE1", data_qubits, self.depolarize1_rate)
        self._memory_circuit.append("M", data_qubits)

        for i, q in enumerate(data_qubits):
            self.add_outcome(
                outcome=target_rec(-1 - i), qubit=q, round=number_of_rounds, type="data"
            )

        for qz in z_qubits:

            qz_adjacent_data_qubits = self.graph.neighbors(qz)

            recs = [
                self.get_target_rec(qubit=qd, round=number_of_rounds)
                for qd in qz_adjacent_data_qubits
            ]
            recs += [self.get_target_rec(qubit=qz, round=number_of_rounds - 1)]

            self._memory_circuit.append("DETECTOR", [target_rec(r) for r in recs])

        # Adding the comparison with the expected state
        ql = [i + i * self.distance for i in range(self.distance)]
        recs = [self.get_target_rec(qubit=q, round=number_of_rounds) for q in ql]
        recs_str = " ".join(f"rec[{rec}]" for rec in recs)
        self._memory_circuit.append_from_stim_program_text(
            f"OBSERVABLE_INCLUDE(0) {recs_str}"
        )

    def append_stab_circuit(self, round: int, data_qubits, x_qubits, z_qubits) -> None:
        r"""
        Append the stabilizer circuit.
        """

        if round > 0:
            self._memory_circuit.append(
                "DEPOLARIZE1", x_qubits + z_qubits, self.depolarize1_rate
            )

        self._memory_circuit.append("H", [q for q in x_qubits])
        self._memory_circuit.append(
            "DEPOLARIZE1", [q for q in x_qubits], self.depolarize1_rate
        )

        # A flag to tell us if a data qubit was used this round
        measured = {qd: False for qd in data_qubits}

        # Perform CNOTs with specific order to avoid hook errors
        for order in range(1, 5):

            for qz in z_qubits:
                control = [
                    neighbor
                    for neighbor, attrs in self.graph[qz].items()
                    if attrs.get("weight") == order
                ]
                if len(control) == 1:
                    control = control[0]
                    self._memory_circuit.append("CNOT", [control, qz])
                    self._memory_circuit.append(
                        "DEPOLARIZE2", [control, qz], self.depolarize2_rate
                    )
                    measured[control] = True

            for qx in x_qubits:
                target = [
                    neighbor
                    for neighbor, attrs in self.graph[qx].items()
                    if attrs.get("weight") == order
                ]
                if len(target) == 1:
                    target = target[0]
                    self._memory_circuit.append("CNOT", [qx, target])
                    self._memory_circuit.append(
                        "DEPOLARIZE2", [target, qx], self.depolarize2_rate
                    )
                    measured[target] = True

        # Apply depolarization channel to account for the time not being used
        not_measured = [key for key, value in measured.items() if value is False]
        self._memory_circuit.append("DEPOLARIZE1", not_measured, self.depolarize1_rate)

        self._memory_circuit.append("H", [q for q in x_qubits])
        self._memory_circuit.append(
            "DEPOLARIZE1", [q for q in x_qubits], self.depolarize1_rate
        )

        self._memory_circuit.append(
            "DEPOLARIZE1", [q for q in x_qubits + z_qubits], self.depolarize1_rate
        )
        self._memory_circuit.append("MR", [q for q in x_qubits + z_qubits])
        for i, q in enumerate(x_qubits + z_qubits):
            self.add_outcome(
                outcome=target_rec(-1 - i), qubit=q, round=round, type="check"
            )

    def build_graph(self) -> None:
        r"""
        Build the 2D lattice of the rotated surface code.
        """

        # Add the nodes for the data qubits
        data_qubits_coords = [
            (col, row)
            for row in range(1, self.distance + 1)
            for col in range(1, self.distance + 1)
        ]
        data = [
            (i, {"type": "data", "coords": data_qubits_coords[i]})
            for i in range(len(data_qubits_coords))
        ]
        self._graph.add_nodes_from(data)

        # Add the nodes the X check qubits.
        x_qubits_coords = [
            (col + (0.5 if row % 2 != 0 else -0.5), row - 0.5)
            for row in range(1, self.distance + 2)
            for col in range(2, self.distance, 2)
        ]
        x_check = [
            (i + len(data), {"type": "X-check", "coords": x_qubits_coords[i]})
            for i in range(len(x_qubits_coords))
        ]
        self._graph.add_nodes_from(x_check)

        # Add the ordered edges for the X checks
        x_edges = []
        for qx in x_check:

            coords = qx[1]["coords"]
            ordered_neighboors = self.get_neighboor_qubits(
                coord=coords, index_order=[1, 3, 0, 2]
            )

            for order, neighboor in enumerate(ordered_neighboors):
                if neighboor is not None:
                    x_edges.append((neighboor, qx[0], order + 1))
        self._graph.add_weighted_edges_from(x_edges)

        # Add the nodes the Z check qubits.
        z_qubits_coords = [
            (col + (0.5 if row % 2 == 0 else -0.5), row + 0.5)
            for row in range(1, self.distance)
            for col in range(1, self.distance + 1, 2)
        ]
        z_check = [
            (
                i + len(data) + len(x_check),
                {"type": "Z-check", "coords": z_qubits_coords[i]},
            )
            for i in range(len(z_qubits_coords))
        ]
        self._graph.add_nodes_from(z_check)

        # Add the ordered edges for the Z checks
        z_edges = []
        for qz in z_check:

            coords = qz[1]["coords"]
            ordered_neighboors = self.get_neighboor_qubits(
                coord=coords, index_order=[1, 0, 3, 2]
            )

            for order, neighboor in enumerate(ordered_neighboors):
                if neighboor is not None:
                    z_edges.append((neighboor, qz[0], order + 1))
        self._graph.add_weighted_edges_from(z_edges)

    def get_neighboor_qubits(
        self, coord: tuple[float, float], index_order: list[int] | None = None
    ) -> list[int]:
        r"""
        Returns the four diagonal qubit, ordered as default:
        - top-left,
        - top-right,
        - bottom-left,
        - bottom-right.

        :param coords: The coordinates of the vertex we want to have the neighboors.
        :param index_order: The order in which the neighboors are
        """
        col, row = coord
        neighboors_coords = [
            (col + dx, row + dy) for dx in [-0.5, 0.5] for dy in [-0.5, 0.5]
        ]

        neighboors = []
        for coords in neighboors_coords:
            try:
                node = [
                    node
                    for node, data in self.graph.nodes(data=True)
                    if data.get("coords") == coords
                ][0]
                neighboors.append(node)
            except IndexError:
                neighboors.append(None)

        if index_order is None:
            return neighboors
        else:
            return [neighboors[i] for i in index_order]
