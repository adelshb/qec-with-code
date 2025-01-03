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

from qec.codes.base_code import BaseCode

__all__ = ["BivariateBicycleCode"]


class BivariateBicycleCode(BaseCode):
    r"""
    A class for the Bivariate Bicycle code.
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        r"""
        Initialize the Bivariate Bicycle code instance.
        """

        self._name = "Bivariate Bicycle"
        self._checks = ["Z-check", "X-check"]
        # self._logic_check = []

        super().__init__(*args, **kwargs)

    def build_graph(self) -> None:
        r"""
        Build the graph for the Bivariate Bicycle code
        """

        # Add the nodes for the L data qubits
        L_data_qubits_coords = [
            (col, row)
            for row in range(1, self.distance + 1, 2)
            for col in range(1, 2 * self.distance + 1, 2)
        ]
        L_data = [
            (i, {"type": "data", "label": "L", "coords": L_data_qubits_coords[i]})
            for i in range(len(L_data_qubits_coords))
        ]
        self._graph.add_nodes_from(L_data)

        # Add the nodes for the R data qubits
        R_data_qubits_coords = [
            (col, row)
            for row in range(2, self.distance + 1, 2)
            for col in range(2, 2 * self.distance + 1, 2)
        ]
        R_data = [
            (
                i + len(L_data),
                {"type": "data", "label": "R", "coords": R_data_qubits_coords[i]},
            )
            for i in range(len(R_data_qubits_coords))
        ]
        self._graph.add_nodes_from(R_data)

        # Add X check qubits
        X_check_qubits_coords = [
            (col - 1, row)
            for row in range(2, self.distance + 1, 2)
            for col in range(2, 2 * self.distance + 1, 2)
        ]
        X_check = [
            (
                i + len(L_data) + len(R_data),
                {"type": "check", "label": "X", "coords": X_check_qubits_coords[i]},
            )
            for i in range(len(X_check_qubits_coords))
        ]
        self._graph.add_nodes_from(X_check)

        # Add Z check qubits
        Z_check_qubits_coords = [
            (col + 1, row)
            for row in range(1, self.distance + 1, 2)
            for col in range(1, 2 * self.distance + 1, 2)
        ]
        Z_check = [
            (
                i + len(L_data) + len(R_data) + len(X_check),
                {"type": "check", "label": "Z", "coords": Z_check_qubits_coords[i]},
            )
            for i in range(len(Z_check_qubits_coords))
        ]
        self._graph.add_nodes_from(Z_check)

    def get_neighbor_qubits(
        self, coord: tuple[float, float], index_order: list[int] | None = None
    ) -> list[int]:
        r"""
        Returns the four diagonal qubit, ordered as default:
        - top-left,
        - top-right,
        - bottom-left,
        - bottom-right.

        :param coords: The coordinates of the vertex we want to have the neighbors.
        :param index_order: The order in which the neighbors are
        """
        col, row = coord
        neighbors_coords = [(col + dx, row + dy) for dx in [-1, 1] for dy in [-1, 1]]

        # TODO: Add long range neighbours

        new_neighbors_coords = []
        for col, row in neighbors_coords:
            if col < 1:
                new_col = col + 12
            elif col > 12:
                new_col = col - 12
            else:
                new_col = col

            if row < 1:
                new_row = row + 12
            elif col > 12:
                new_row = row - 12
            else:
                new_row = row

            new_neighbors_coords.append((new_col, new_row))

        neighbors = []
        for coords in new_neighbors_coords:
            try:
                node = [
                    node
                    for node, data in self.graph.nodes(data=True)
                    if data.get("coords") == coords
                ][0]
                neighbors.append(node)
            except IndexError:
                neighbors.append(None)

        if index_order is None:
            return neighbors
        else:
            return [neighbors[i] for i in index_order]
