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

    __slots__ = "_number_of_qubits"

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        r"""
        Initialize the Repetition code instance.
        """
        super().__init__(*args, **kwargs)

        self._number_of_qubits = 2 * self.distance - 1

    def build_graph(self):
        r"""
        Build the graph for the repetition code
        """

        data = [(i, {"type": "data"}) for i in range(self.distance)]
        self._graph.add_nodes_from(data)

        check = [
            (i + self.distance, {"type": "Z-check"}) for i in range(self.distance - 1)
        ]
        self._graph.add_nodes_from(check)

        edges = [(i, i + self.distance) for i in range(self.distance - 1)]
        self._graph.add_edges_from(edges)

        edges = [(i, i + self.distance - 1) for i in range(1, self.distance)]
        self._graph.add_edges_from(edges)

    def build_memory_circuit(self, number_of_rounds: int = 2) -> Circuit:
        r"""
        Build and return a Stim Circuit object implementing a memory for the given time.

        :param number_of_rounds: The number of rounds in the memory.
        """

        # Initialize the circuit
        self._memory_circuit = Circuit()

        # Apply depolarization gate to all data qubits
        for q in range(self.distance):
            self._memory_circuit.append("DEPOLARIZE1", [q], self.depolarize1_rate)

        # Repeted block
        for round in range(number_of_rounds):

            # Loop over the ancillary qubits
            data_qubit_count = 0
            for q in range(self.distance, self.number_of_qubits):

                # Reset and apply depolarizing error to all ancillary qubits
                self._memory_circuit.append("R", [q])
                self._memory_circuit.append("DEPOLARIZE1", [q], self.depolarize1_rate)

                # Perform CNOT
                for ___ in range(2):

                    # Adding a single qubit depolarization
                    if data_qubit_count == self.distance - 1:
                        self._memory_circuit.append(
                            "DEPOLARIZE1", [self.distance - 1], self.depolarize1_rate
                        )

                    self._memory_circuit.append("CNOT", [data_qubit_count, q])
                    self._memory_circuit.append(
                        "DEPOLARIZE2", [data_qubit_count, q], self.depolarize2_rate
                    )

                    # Adding a single qubit depolarization
                    if data_qubit_count == 0:
                        self._memory_circuit.append(
                            "DEPOLARIZE1", [0], self.depolarize1_rate
                        )

                    data_qubit_count += 1
                data_qubit_count -= 1

                # Adding measurement with pre-measurement error
                self._memory_circuit.append("DEPOLARIZE1", [q], self.depolarize1_rate)
                self._memory_circuit.append("M", [q])

                # Adding detector
                if round == 0:
                    self._memory_circuit.append("DETECTOR", [target_rec(-1)])
                else:
                    self._memory_circuit.append(
                        "DETECTOR",
                        [
                            target_rec(-1),
                            target_rec(-1 - self.number_of_qubits + self.distance),
                        ],
                    )

        # End of the final round
        for q in range(self.distance):
            self._memory_circuit.append("DEPOLARIZE1", [q], self.depolarize1_rate)
            self._memory_circuit.append("M", [q])

            # Adding detector
            if q > 0:
                self._memory_circuit.append(
                    "DETECTOR",
                    [
                        target_rec(-1),
                        target_rec(-2),
                        target_rec(-2 - self.number_of_qubits + self.distance),
                    ],
                )

            # Adding the comparison with the expected state
            self._memory_circuit.append_from_stim_program_text(
                "OBSERVABLE_INCLUDE(0) rec[-1]"
            )
