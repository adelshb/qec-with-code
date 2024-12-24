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

__all__ = ["Measurement"]


class Measurement:
    r"""
    A class for collection of measurement outcomes.
    """

    __slots__ = ("_data")

    def __init__(self) -> None:

        self._data = {}
        
    @property
    def data(self)->dict:
        r"""
        The collection of outcomes.
        """
        return self._data
    
    def get_outcome(
        self, 
        qubit: any, 
        round: int, 
    )-> any:
        r"""
        Return the outcome for the qubit at the specified round or return None if not in the collection.
        
        :param qubit: The qubit on which the measurement is performed.
        :param round: The round during which the measurement is performed.
        """
        try: 
            return self.data[round][qubit]
        except KeyError:
            return None
        
    def add_outcome(
        self, 
        outcome: any, 
        qubit: any, 
        round: int, 
        type: str | None
    )->None:
        r"""
        Add an outcome to the collection.
        
        :param outcome: The outcome to store.
        :param qubit: The qubit on which the measurement is performed.
        :param round: The round during which the measurement is performed.
        :param type: The type of measurement.
        """
        
        if type not in ["check", "data", None]:
            ValueError("The value of type must be either 'check' or 'data'.")
        
        if round not in self._data.keys():
            self._data[round] = {}
        
        self._data[round][qubit] = outcome
