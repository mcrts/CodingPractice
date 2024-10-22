from aoc2023.day16 import go_straight, Node, Direction
import numpy as np
import pytest




GRID = np.ones((4, 8))
go_straight_cases = [
    (Node(0, 0, Direction.UP), Node.OutsideNode()),
    (Node(0, 0, Direction.RIGHT), Node(0, 1, Direction.RIGHT)),
    (Node(0, 0, Direction.DOWN), Node(1, 0, Direction.DOWN)),
    (Node(0, 0, Direction.LEFT), Node.OutsideNode()),

    (Node(3, 0, Direction.UP), Node(2, 0, Direction.UP)),
    (Node(3, 0, Direction.RIGHT), Node(3, 1, Direction.RIGHT)),
    (Node(3, 0, Direction.DOWN), Node.OutsideNode()),
    (Node(3, 0, Direction.LEFT), Node.OutsideNode()),

    (Node(3, 7, Direction.UP), Node(2, 7, Direction.UP)),
    (Node(3, 7, Direction.RIGHT), Node.OutsideNode()),
    (Node(3, 7, Direction.DOWN), Node.OutsideNode()),
    (Node(3, 7, Direction.LEFT), Node(3, 6, Direction.LEFT)),

    (Node(0, 7, Direction.UP), Node.OutsideNode()),
    (Node(0, 7, Direction.RIGHT), Node.OutsideNode()),
    (Node(0, 7, Direction.DOWN), Node(1, 7, Direction.DOWN)),
    (Node(0, 7, Direction.LEFT), Node(0, 6, Direction.LEFT)),

    (Node(1, 3, Direction.UP), Node(0, 3, Direction.UP)),
    (Node(1, 3, Direction.RIGHT), Node(1, 4, Direction.RIGHT)),
    (Node(1, 3, Direction.DOWN), Node(2, 3, Direction.DOWN)),
    (Node(1, 3, Direction.LEFT), Node(1, 2, Direction.LEFT)),
]


@pytest.mark.parametrize("node_in,expected", go_straight_cases)
def test_go_straight(node_in, expected):
    assert go_straight(GRID, node_in) == expected