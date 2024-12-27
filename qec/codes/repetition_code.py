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

__all__ = ["RepetitionCode"]


class RepetitionCode(BaseCode):
    r"""
    A class for Repetition code.
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        r"""
        Initialize the Repetition code instance.
        """
        super().__init__(*args, **kwargs)

    def build_graph(self) -> None:
        r"""
        Build the graph for the repetition code
        """

        data = [(i, {"type": "data"}) for i in range(self.distance)]
        self._graph.add_nodes_from(data)

        check = [
            (i + self.distance, {"type": "Z-check"}) for i in range(self.distance - 1)
        ]
        self._graph.add_nodes_from(check)

        edges = [(i, i + self.distance, 1) for i in range(self.distance - 1)]
        self._graph.add_weighted_edges_from(edges)

        edges = [(i, i + self.distance - 1, 2) for i in range(1, self.distance)]
        self._graph.add_weighted_edges_from(edges)

    def build_memory_circuit(self, number_of_rounds: int = 2) -> Circuit:
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
        z_qubits = [
            node
            for node, data in self.graph.nodes(data=True)
            if data.get("type") == "Z-check"
        ]

        # Initialize the circuit
        self._memory_circuit = Circuit()

        self._memory_circuit.append("R", all_qubits)
        self._memory_circuit.append("DEPOLARIZE1", all_qubits, self.depolarize1_rate)

        # Body
        for round in range(number_of_rounds):

            # A flag to tell us if a data qubit was used this round
            measured = {qd: False for qd in data_qubits}

            if round > 0:
                self._memory_circuit.append(
                    "DEPOLARIZE1", z_qubits, self.depolarize1_rate
                )

            for qz in z_qubits:

                for order in range(1, 3):

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

            # Apply depolarization channel to account for the time not being used
            not_measured = [key for key, value in measured.items() if value is False]
            self._memory_circuit.append(
                "DEPOLARIZE1", not_measured, self.depolarize1_rate
            )

            # Adding measurement with pre-measurement error
            self._memory_circuit.append("DEPOLARIZE1", z_qubits, self.depolarize1_rate)
            self._memory_circuit.append("MR", z_qubits)
            for i, q in enumerate(z_qubits):
                self.add_outcome(
                    outcome=target_rec(-1 - i), qubit=q, round=round, type="Z-check"
                )

                if round == 0:
                    self._memory_circuit.append("DETECTOR", [target_rec(-1 - i)])
                else:
                    self._memory_circuit.append(
                        "DETECTOR",
                        [
                            target_rec(-1 - i),
                            target_rec(-1 - i - self.number_of_qubits + self.distance),
                        ],
                    )

        # Final
        # Adding measurement with pre-measurement error
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
        self._memory_circuit.append_from_stim_program_text(
            "OBSERVABLE_INCLUDE(0) rec[-1]"
        )
