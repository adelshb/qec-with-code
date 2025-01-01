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

import numpy as np
import matplotlib.pyplot as plt
import pymatching

from qec.codes.base_code import BaseCode

__all__ = ["ThresholdLAB"]


class ThresholdLAB:
    r"""
    A class for wrapping threshold calculation
    """

    __slots__ = ("_distances", "_error_rates", "_code", "_collected_stats")

    def __init__(
        self, code: BaseCode, distances: list[int], error_rates: list[float]
    ) -> None:
        r"""
        Initialization of the Base Code class.

        :param code: The code
        :param distances: Distances for the code.
        :param error_rates: Error rate.
        """

        self._distances = distances
        self._code = code
        self._error_rates = error_rates
        self._collected_stats = {}

    @property
    def distances(self) -> list[int]:
        r"""
        The distances of the code.
        """
        return self._distances

    @property
    def error_rates(self) -> list[float]:
        r"""
        The error rates.
        """
        return self._error_rates

    @property
    def code(self) -> BaseCode:
        r"""
        The code.
        """
        return self._code

    @property
    def collected_stats(self) -> dict:
        r"""
        The collected stats during sampling.
        """
        return self._collected_stats

    def compute_logical_errors(self, code: BaseCode, num_shots: int) -> int:
        r"""
        Sample the memory circuit and return the number of errors.

        :param num_shots: The number of samples.
        """

        # Sample the memory circuit
        sampler = code.memory_circuit.compile_detector_sampler()
        detection_events, observable_flips = sampler.sample(
            num_shots, separate_observables=True
        )

        # Configure the decoder using the memory circuit then run the decoder
        detector_error_model = code.memory_circuit.detector_error_model(
            decompose_errors=False
        )

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

    def collect_stats(self, num_shots: int) -> None:
        r""" """

        for distance in self.distances:

            temp_logical_error_rate = []

            for prob_error in self.error_rates:

                code = self.code(
                    distance=distance,
                    depolarize1_rate=prob_error,
                    depolarize2_rate=prob_error,
                )
                code.build_memory_circuit(number_of_rounds=distance * 3)
                num_errors_sampled = self.compute_logical_errors(
                    code=code, num_shots=num_shots
                )
                temp_logical_error_rate.append(num_errors_sampled / num_shots)

            self._collected_stats[distance] = temp_logical_error_rate

    def plot_stats(self) -> None:
        r""" """

        fig, ax = plt.subplots(1, 1)

        for distance in self.collected_stats.keys():
            ax.plot(
                self.error_rates, self.collected_stats[distance], label=f"d={distance}"
            )

        # ax.set_ylim(1e-3, 5e-1)
        # ax.set_xlim(2e-2, 1e-1)
        ax.loglog()
        ax.set_title("Repetition Code Error Rates")
        ax.set_xlabel("Phyical Error Rate")
        ax.set_ylabel("Logical Error Rate")
        ax.grid(which="major")
        ax.grid(which="minor")
        ax.legend()
        fig.set_dpi(120)
