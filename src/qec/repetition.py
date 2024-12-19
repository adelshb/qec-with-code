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

from stim import Circuit

from qec import QEC

__all__ = ["RepCode"]


class RepQEC(QEC):
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
        
        super(QEC, self).__init__(*args, **kwargs)
    
    def build_memory_circuit(self, time: int) -> Circuit:
        
        # Initialize the circuit
        circ = Circuit()
        
        # Repeted 
        
        
        # Final round