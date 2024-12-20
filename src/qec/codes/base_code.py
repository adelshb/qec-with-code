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

import numpy as np
from numpy import ndarray
from stim import Circuit
import pymatching


__all__ = ["BaseCode"]


class BaseCode(ABC):
    r"""
    An abstract base class for quantum error correction codes.
    """
    
    __slots__ = ("_distance", "_memory_circuit", "_parity_data", "_depolarize1_rate", "_depolarize2_rate", "_sampler")
    
    def __init__(
        self,
        distance: int,
        depolarize1_rate: float,
        depolarize2_rate: float,
    ) -> None:
        
        self._distance = distance
        self._depolarize1_rate = depolarize1_rate
        self._depolarize2_rate = depolarize2_rate
        self._memory_circuit: Circuit
        self._parity_data: list[ndarray] = []
         
    @property
    def distance(self) -> int:
        r"""
        The distance of the code.
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
        return self._parity_data
    
    @property
    def depolarize1_rate(self) -> float:
        r"""
        The depolarization rate for single qubit gate.
        """
        return self._depolarize1_rate
    
    @property
    def depolarize2_rate(self) -> float:
        r"""
        The depolarization rate for two-qubit gate.
        """
        return self._depolarize2_rate
    
    @property
    def sampler(self) -> any:
        r"""
        The sampler from the memory circuit
        """
        return self._sampler
    
    @abstractmethod
    def build_memory_circuit(self, number_of_rounds: int) -> None:
        r"""
        Build and return a Stim Circuit object implementing a memory for the given time.
        """

    def compute_logical_errors(self, num_shots: int) -> int:
        
        # Sample the memory circuit
        # self._sampler = self.memory_circuit.detector_error_model(decompose_errors=True)
        self._sampler = self.memory_circuit.compile_detector_sampler()
        detection_events, observable_flips = self.sampler.sample(num_shots, separate_observables=True)

        # Configure the decoder using the memory circuit then run the decoder
        detector_error_model = self.memory_circuit.detector_error_model(decompose_errors=True)
        matcher = pymatching.Matching.from_detector_error_model(detector_error_model)
        predictions = matcher.decode_batch(detection_events)

        # Count the number of errors
        num_errors = 0
        for shot in range(num_shots):
            actual_for_shot = observable_flips[shot]
            predicted_for_shot = predictions[shot]
            if not np.array_equal(actual_for_shot, predicted_for_shot):
                num_errors += 1
        return num_errors
