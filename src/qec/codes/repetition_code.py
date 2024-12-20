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
    
    __slots__ = ("_number_of_qubits")
    
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
        
    @property
    def number_of_qubits(self) -> int:
        r"""
        The total number of physical qubits.
        """
        return self._number_of_qubits
    
    def build_memory_circuit(self, time: int = 2) -> Circuit:
        
        # Initialize the circuit
        self._memory_circuit = Circuit()
        
        # Apply depolarization gate to all data qubits
        for q in range(self.distance):
            self._memory_circuit.append("DEPOLARIZE1", [q], self.depolarize1_rate)
        
        # Repeted block
        for round in range(time):
            
            # Loop over the ancillary qubits
            data_qubit_count = 0
            for q in range(self.distance, self.number_of_qubits):
                
                # Reset and apply depolarizing error to all ancillary qubits
                self._memory_circuit.append("R", [q])
                self._memory_circuit.append("DEPOLARIZE1", [q], self.depolarize1_rate)
                
                # Perform CNOT between each neighbood data qubit followed by depolarizing error
                for ___ in range(2):
                    
                    # Adding a single qubit depolarization for the lower border data qubit as it only occurs in one CNOT
                    if data_qubit_count == self.distance:
                        self._memory_circuit.append("DEPOLARIZE1", [self.distance], self.depolarize1_rate)
                        
                    self._memory_circuit.append("CNOT", [data_qubit_count, q])
                    self._memory_circuit.append("DEPOLARIZE2", [data_qubit_count, q], self.depolarize2_rate)
                    
                    # Adding a single qubit depolarization for the upper border data qubit as they only occur in one CNOT
                    if data_qubit_count == 0:
                        self._memory_circuit.append("DEPOLARIZE1", [0], self.depolarize1_rate)
                        
                    data_qubit_count +=1
                    
            # Adding measurement with pre-measurement error
            self._memory_circuit.append("DEPOLARIZE1", [q], self.depolarize1_rate)
            self._memory_circuit.append("M", [q])
            
            # Adding detector
            if round == 0:
                self._memory_circuit.append("DETECTOR", [target_rec(-1)])
            elif round > 0 and round < time:
                self._memory_circuit.append("DETECTOR", [target_rec(-1), target_rec(-1 - self.number_of_qubits + self.distance)])
                
        # End of the final round
        for q in range(self.distance):
            self._memory_circuit.append("M", [q])
            
            # Adding detector
            if q % 2 == 0:
                self._memory_circuit.append("DETECTOR", [target_rec(-1), target_rec(-2), target_rec(-2 - self.number_of_qubits + self.distance)])