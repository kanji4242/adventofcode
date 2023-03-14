#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/22
#

import sys
import re
from copy import copy

import numpy as np


def find_boundaries(array):
    start, end = -1, -1
    for x in range(len(array)):
        if start == -1 and array[x] != 0:
            start = x
        if start >= 0 and end == -1:
            if (x < len(array) - 1 and array[x + 1] == 0) \
                    or (x == len(array) - 1 and array[x] != 0):
                end = x

    return start, end


class Vector(np.ndarray):
    x_rotate_matrix = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    y_rotate_matrix = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
    z_rotate_matrix = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, (3,), dtype=int)

    def __init__(self, x=0, y=0, z=0):
        self[:] = [x, y, z]

    def __getattr__(self, item):
        try:
            if item in ['x', 'y', 'z']:
                return self[['x', 'y', 'z'].index(item)]
        except ValueError:
            raise AttributeError(f"No such attribute: {item}") from None

    def rotate(self, rotate_x_axis=0, rotate_y_axis=0, rotate_z_axis=0):
        if rotate_x_axis > 0:
            for _ in range(rotate_x_axis):
                self[:] = np.dot(self.x_rotate_matrix, self)
        if rotate_y_axis > 0:
            for _ in range(rotate_y_axis):
                self[:] = np.dot(self.y_rotate_matrix, self)
        if rotate_z_axis > 0:
            for _ in range(rotate_z_axis):
                self[:] = np.dot(self.z_rotate_matrix, self)


class Point(Vector):
    pass


class Direction:
    DIRECTION_UP = 0
    DIRECTION_RIGHT = 1
    DIRECTION_DOWN = 2
    DIRECTION_LEFT = 3

    def __init__(self, direction=DIRECTION_UP):
        self.direction = direction

    def turn(self, direction):
        if direction == 'R':
            self.direction = (self.direction + 1) % 4
        elif direction == 'L':
            self.direction = (self.direction - 1) % 4
        else:
            raise TypeError(f"Invalid direction {direction}")


class Edge:
    def __init__(self, edge_id, point, vector):
        self.id = edge_id
        self.point = point
        self.vector = vector

    def __repr__(self):
        return f"Edge(<{self.id}> {self.point}-{self.vector})"

    def __eq__(self, other):
        return self.point.x == other.point.x and self.point.y == other.point.y and self.point.z == other.point.z \
               and self.vector.x == other.vector.x and self.vector.y == other.vector.y and self.vector.z == other.vector.z

    def __copy__(self):
        return Edge(self.id, self.point.copy(), self.vector.copy())

    def rotate(self, direction):
        if direction == Direction.DIRECTION_UP:
            self.point.rotate(rotate_x_axis=1)
            self.vector.rotate(rotate_x_axis=1)
        elif direction == Direction.DIRECTION_DOWN:
            self.point.rotate(rotate_x_axis=3)
            self.vector.rotate(rotate_x_axis=3)
        elif direction == Direction.DIRECTION_RIGHT:
            self.point.rotate(rotate_y_axis=3)
            self.vector.rotate(rotate_y_axis=3)
        elif direction == Direction.DIRECTION_LEFT:
            self.point.rotate(rotate_y_axis=1)
            self.vector.rotate(rotate_y_axis=1)


class EdgeNet:
    def __init__(self, edges=None):
        if edges:
            self._edges = edges
        else:
            self._edges = self._init_edges()

    def __copy__(self):
        edges = [copy(e) for e in self._edges]
        return EdgeNet(edges)

    def __repr__(self):
        return f"EdgeNet({[e for e in self._edges]})"

    def _init_edges(self):
        return [
            # Top edges
            Edge(1, Point(-1, 1, 1), Vector(1, 0, 0)),
            Edge(2, Point(1, 1, 1), Vector(0, -1, 0)),
            Edge(3, Point(1, -1, 1), Vector(-1, 0, 0)),
            Edge(4, Point(-1, -1, 1), Vector(0, 1, 0)),

            # Side edges
            Edge(5, Point(-1, 1, 1), Vector(0, 0, -1)),
            Edge(6, Point(1, 1, 1), Vector(0, 0, -1)),
            Edge(7, Point(1, -1, 1), Vector(0, 0, -1)),
            Edge(8, Point(-1, -1, 1), Vector(0, 0, -1)),

            # Bottom edges
            Edge(9, Point(-1, 1, -1), Vector(1, 0, 0)),
            Edge(10, Point(1, 1, -1), Vector(0, -1, 0)),
            Edge(11, Point(1, -1, -1), Vector(-1, 0, 0)),
            Edge(12, Point(-1, -1, -1), Vector(0, 1, 0))
        ]

    def rotate(self, direction):
        for e in self._edges:
            e.rotate(direction)

    def find_top_edges(self):
        top_edges = []
        for e in self._edges:
            if e == Edge(1, Point(-1, 1, 1), Vector(1, 0, 0)) or e == Edge(1, Point(1, 1, 1), Vector(-1, 0, 0)):
                top_edges.append(e)
        for e in self._edges:
            if e == Edge(2, Point(1, 1, 1), Vector(0, -1, 0)) or e == Edge(2, Point(1, -1, 1), Vector(0, 1, 0)):
                top_edges.append(e)
        for e in self._edges:
            if e == Edge(3, Point(1, -1, 1), Vector(-1, 0, 0)) or e == Edge(3, Point(-1, -1, 1), Vector(1, 0, 0)):
                top_edges.append(e)
        for e in self._edges:
            if e == Edge(4, Point(-1, -1, 1), Vector(0, 1, 0)) or e == Edge(4, Point(-1, 1, 1), Vector(0, -1, 0)):
                top_edges.append(e)
        return top_edges


class Face:
    def __init__(self, size, coord, edges):
        self.size = size
        self.coord = coord
        self.edges = edges

    def __repr__(self):
        return f"Face(<{self.coord}> ^:{self.edges[0]}, >:{self.edges[1]}, v:{self.edges[2]}, <:{self.edges[3]})"

    def is_adjacent(self, other):
        delta = abs(np.array(self.coord) - np.array(other.coord))
        return (delta[0] == 1 and delta[1] == 0) or (delta[0] == 0 and delta[1] == 1)

    def edge_id_direction(self, edge_id):
        for n in range(len(self.edges)):
            if self.edges[n].id == edge_id:
                return n
        return -1

    def get_coords_from_edge(self, direction):
        coords = []
        if direction == Direction.DIRECTION_UP or direction == Direction.DIRECTION_DOWN:
            coords = [(x, 0 if direction == Direction.DIRECTION_UP else self.size - 1) for x in range(self.size)]
            if self.edges[direction].vector.x < 0:
                coords.reverse()
        if direction == Direction.DIRECTION_LEFT or direction == Direction.DIRECTION_RIGHT:
            coords = [(0 if direction == Direction.DIRECTION_LEFT else self.size - 1, y) for y in range(self.size)]
            if self.edges[direction].vector.y > 0:
                coords.reverse()

        return coords


class Tiles:

    TILE_EMPTY = 0x0
    TILE_OPEN = 0X1
    TILE_FACING_UP = 0x0002
    TILE_FACING_RIGHT = 0x0102
    TILE_FACING_DOWN = 0x0202
    TILE_FACING_LEFT = 0x0302
    TILE_WALL = 0x10

    TILES = {
        TILE_EMPTY: ' ',
        TILE_OPEN: '.',
        TILE_FACING_UP: '^',
        TILE_FACING_RIGHT: '>',
        TILE_FACING_DOWN: 'v',
        TILE_FACING_LEFT: '<',
        TILE_WALL: '#'
    }

    def __init__(self, file):
        self.file = file
        self.tiles = None
        self.face_size = 0
        self.faces = {}
        self.directions = None
        self.edge_net = EdgeNet()
        self.jumps = {}

        self.facing = Direction(Direction.DIRECTION_RIGHT)
        self.position = None

    def _is_wall(self, tile):
        return tile & 0x0F03 == 0

    def read_tiles(self):
        with open(self.file) as f:
            size_x, size_y = 0, 0
            for line in f:
                line = line.rstrip()
                if not line:
                    break

                size_x = max(len(line), size_x)
                size_y += 1

            self.directions = [(int(n), d) for n, d in re.findall(r'(\d+)([RL]?)', f.readline().strip())]

        self.tiles = np.ndarray((size_x, size_y), dtype=int)
        self.tiles.fill(0)

        tiles_reverse = {v: k for k, v in self.TILES.items()}

        with open(self.file) as f:
            y = 0
            for line in f:
                line = line.rstrip()
                if not line:
                    break
                self.tiles[:, y] = [tiles_reverse[c] for c in line] + [0] * (size_x - len(line))
                y += 1

    def set_jumps_as_plane(self):
        for y in range(self.tiles.shape[1]):
            x_start, x_end = find_boundaries(self.tiles[:, y])
            if y == 0:
                self.position = (x_start, 0)
            self.jumps[(x_start, y, 3)] = (x_end, y, 0)
            self.jumps[(x_end, y, 1)] = (x_start, y, 0)

        for x in range(self.tiles.shape[0]):
            y_start, y_end = find_boundaries(self.tiles[x, :])
            self.jumps[(x, y_start, 0)] = (x, y_end, 0)
            self.jumps[(x, y_end, 2)] = (x, y_start, 0)

    def set_jumps_as_cube(self):
        self.analyse_faces()

        for edge_id in range(1, 13):
            faces = []
            for face in self.faces.values():
                edge_direction = face.edge_id_direction(edge_id)
                if edge_direction != -1:
                    faces.append((face, edge_direction))
            if len(faces) == 2:
                face1, edge_direction1 = faces[0]
                face2, edge_direction2 = faces[1]
                v1 = face1.edges[edge_direction1].vector
                v2 = face2.edges[edge_direction2].vector

                for coord1, coord2 in zip(face1.get_coords_from_edge(edge_direction1),
                                          face2.get_coords_from_edge(edge_direction2)):
                    if not ((v1 == v2).all() and face1.is_adjacent(face2)):
                        coord1 = (face1.size * face1.coord[0] + coord1[0],
                                  face1.size * face1.coord[1] + coord1[1])
                        coord2 = (face2.size * face2.coord[0] + coord2[0],
                                  face2.size * face2.coord[1] + coord2[1])
                        self.jumps[(coord1[0], coord1[1], edge_direction1)] = \
                            (coord2[0], coord2[1], (edge_direction2 - 2) % 4 - edge_direction1)
                        self.jumps[(coord2[0], coord2[1], edge_direction2)] = \
                            (coord1[0], coord1[1], (edge_direction1 - 2) % 4 - edge_direction2)

    def analyse_faces(self):
        self.face_size = np.gcd(self.tiles.shape[0], self.tiles.shape[1])

        starting_face = None

        for y in range(self.tiles.shape[1] // self.face_size):
            for x in range(self.tiles.shape[0] // self.face_size):
                if self.tiles[x * self.face_size, y * self.face_size] != self.TILE_EMPTY and not starting_face:
                    starting_face = (x, y)

        self.travel_through_faces(self.edge_net, starting_face)
        self.position = (starting_face[0] * self.face_size, starting_face[1] * self.face_size)

    def travel_through_faces(self, edge_net, face_coord):
        if face_coord in self.faces:
            return

        if self.tiles[face_coord[0] * self.face_size, face_coord[1] * self.face_size] != self.TILE_EMPTY:
            self.faces[face_coord] = Face(self.face_size, face_coord, edge_net.find_top_edges())

        if 0 < face_coord[0] < (self.tiles.shape[0] // self.face_size) - 1:
            if self.tiles[(face_coord[0] + 1) * self.face_size, face_coord[1] * self.face_size] != self.TILE_EMPTY:
                new_edge_net = copy(edge_net)
                new_edge_net.rotate(Direction.DIRECTION_RIGHT)
                self.travel_through_faces(new_edge_net, (face_coord[0] + 1, face_coord[1]))
            if self.tiles[(face_coord[0] - 1) * self.face_size, face_coord[1] * self.face_size] != self.TILE_EMPTY:
                new_edge_net = copy(edge_net)
                new_edge_net.rotate(Direction.DIRECTION_LEFT)
                self.travel_through_faces(new_edge_net, (face_coord[0] - 1, face_coord[1]))

        if 0 <= face_coord[1] < (self.tiles.shape[1] // self.face_size) - 1:
            if self.tiles[face_coord[0] * self.face_size, (face_coord[1] + 1) * self.face_size] != self.TILE_EMPTY:
                new_edge_net = copy(edge_net)
                new_edge_net.rotate(Direction.DIRECTION_DOWN)
                self.travel_through_faces(new_edge_net, (face_coord[0], face_coord[1] + 1))

    def get_next_position(self):
        jump_key = (self.position[0], self.position[1], self.facing.direction)
        if jump_key in self.jumps:
            position = (self.jumps[jump_key][0], self.jumps[jump_key][1])
            facing_delta = self.jumps[jump_key][2]

        else:
            direction_vectors = [
                (0, -1),  # 0: up
                (1, 0),   # 1: right
                (0, 1),   # 2: down
                (-1, 0),  # 3: left
            ]
            position = (self.position[0] + direction_vectors[self.facing.direction][0],
                        self.position[1] + direction_vectors[self.facing.direction][1])
            facing_delta = 0

        return position, facing_delta

    def travel_tiles(self):
        for direction in self.directions:
            steps = direction[0]
            while steps > 0:

                next_position, facing_delta = self.get_next_position()
                self.tiles[self.position] = 0x02 | (self.facing.direction << 8)

                if self._is_wall(self.tiles[next_position]):
                    break

                if steps > 0:
                    self.position = next_position
                    self.facing.direction += facing_delta

                steps -= 1

            if direction[1]:
                self.facing.turn(direction[1])
            self.tiles[self.position] = 0x02 | (self.facing.direction << 8)

        return self.get_final_password()

    def get_final_password(self):
        return 1000 * (self.position[1] + 1) + 4 * (self.position[0] + 1) + (self.facing.direction - 1) % 4

    def display_tiles(self):
        for y in range(self.tiles.shape[1]):
            print(''.join([self.TILES[self.tiles[x][y]] for x in range(self.tiles.shape[0])]))


def day22_1(file):
    tiles = Tiles(file)
    tiles.read_tiles()
    tiles.set_jumps_as_plane()

    final_password = tiles.travel_tiles()
    tiles.display_tiles()
    print(final_password)


def day22_2(file):
    tiles = Tiles(file)
    tiles.read_tiles()
    tiles.set_jumps_as_cube()

    final_password = tiles.travel_tiles()
    tiles.display_tiles()
    print(final_password)


if __name__ == '__main__':
    day22_1(sys.argv[1])
    day22_2(sys.argv[1])
