#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/22
#

"""
This one was very tricky because when I tackled the part 2, my code was absolutely not adapted for this second part.
Instead of writing another code from scratch, I preferred a have a generic solution suitable for the 2 parts, which
(in my opinion) is more elegant. My idea was the following :

 - the first steps are quite classic: parse the tiles from input and insert them into a numpy array, then parse the
  directions and them split them into a list of tuple. Each tuple containing the number of steps and the letter
  indicating how to turn.

 - build a list of "jumps". A jump is when the next tile is not the next one in the path regarding the direction
   we're facing. For instance in part 1, when we reach a tile on the border and our next tile in the path would be
   outside the board or even outside the map, we have to wrap around. In other words, we need to jump on the opposite
   side of our current row (or column, depending on the direction we're facing). That principe also apply for part 2,
   except that we need to consider the board as a net of a cube with its 6 faces. We could jump to a completely
   different location in the map. In addition to this, we also need to take into consideration that when jumping we
   also may have to turn clockwise or counterclockwise, because the faces on the cube net will be rotated or even be
   upside-down. The advantage of this "jumps" method, is that we can iterate over all the directions sequentially with
   the same algorithm for the 2 parts.


Building the jumps for part 1:

This is pretty straight forward. Process each row of the tiles map and find the 2 boundaries of the tiles: the left and
the right boundaries. The left boundary is the lowest index on the row when an open or a wall tiles occurs,
it can happen at index 0 or at higher index if we have empty tiles before. The same applies for the right boundary
on the opposite direction which correspond to the highest index. So we get 2 coordinates, and with this we can set 2
jumps: the first one going from the first the left coordinate to the right coordinate, and the second one from the
right to the left coordinate. Finally, do the same process for the columns.


Building the jumps for part 2:

This is much trickier, because we need to interpret these tiles as a net of a cube. The problem is that there are 11
different nets for a cube (https://www.researchgate.net/figure/The-eleven-cube-nets_fig2_288835330), and the net used
in the given input sample is not the same as the net used in my input. So I had 2 options:

- option 1: hard code the jumps adapted to my input considering the net used, (and optionally do the same for my
  input sample, for debugging purpose which would be very convenient). The big downside of this is that hard coding
  all the jumps for a net of cube is a quite tedious and boring task: a cube has 12 edges and 6 faces, in a cube net
  the 6 faces are joined together, so 5 edges are connected and the 7 remaining edges are not. For the connected
  faces, we don't need to jump, however we need to create jumps for the 7 edges in both directions, and we need
  to figure out where they are precisely located on the map and in which direction. A burdensome task and not
  very funny.

- option 2: implement a generic solution, which will be adapted for every case and set all the jumps automatically.
  But we need to find an algorithm ...

I chose the option 2. My idea for the algorithm is to simulate a cube in 3 dimensions with edges of side 2 centered
at coordinate (0, 0, 0), and set its 8 vertices as point coordinates and its 12 edges as vectors. Using vectors is very
important to figure out the direction. I labelled all my edges from 1 to 12 to identify them, and I placed them in a
very specific order. This order is arbitrary, I could use another order, for the same result.

The cube configuration is the following:

Looking at the cube from the top, the 4 top horizontal edges would look like this (the arrows indicates the
vector direction):

           edge 1           Axis orientation  ^ y axis
      p1 +------->+ p2                        |
         ^        |                           |
  edge 4 |   O    | edge 2                    +---> x axis
         |        v                     z axis upward
      p4 +<-------+ p3
           edge 3

The "O" sign is the origin (0, 0, 0) and the 4 points p1 to p4 have respective coordinates: (-1, 1, 1), (1, 1, 1),
(1, -1, 1), (-1, -1, 1).
Still looking from the top and moving at lower level, we find the 4 vertical edges whose vectors are directed
downward (by convention), they would like this:

   edge 5          edge 6
         +        +

             O

         +        +
   edge 8          edge 7

And finally at the bottom level, the 4 remaining horizontal edges :

           edge 9
      p5 +------->+ p6
         ^        |
 edge 12 |   O    | edge 10
         |        v
      p8 +<-------+ p7
           edge 11

The 4 points p5 to p9 have respective coordinates: (-1, 1, -1), (1, 1, -1), (1, -1, -1), (-1, -1, -1)

For instance, if we rotate the cube to the right (counterclockwise rotation on the y axis), we would get the following
configuration while still looking from the top (note the vector direction changes) :

           edge 6
      p2 +------->+ p6
         |        |
  edge 2 |   O    | edge 10
         v        v
      p3 +------->+ p7
           edge 7

Now with this virtual cube, we can parse tiles to find there the faces are located (with non-empty tiles) with a
recursive algorithm similar the flood fill algorithm (https://en.wikipedia.org/wiki/Flood_fill). For instance, when we
detect a face at the right from our current face, we rotate the cube to right, and note new 4 top edges that
will appear and their vector (for direction). And the end of the process, we will have a map of each face, where
they are located on the tiles map, which specific edge they reference and in which direction.

With these map, we have quite easy defined all the jumps by iterating over the 12 edges and 2 jumps like in part 1
but taking into account the direction change thanks the vector directions of the edge.


"""

import sys
import re
from copy import copy

import numpy as np


def find_boundaries(array):
    """
    Find the 2 boundaries of an array of int and return 2 value: the left and the right boundaries.
    Return -1 and -1 if not found.
    The left boundary is the lowest index on the array when a value > 0 occurs or
    Same for the right boundary and the opposite side
    """
    left, right = -1, -1
    for x in range(len(array)):
        if left == -1 and array[x] != 0:
            # Mark the left boundary
            left = x
        if left >= 0 and right == -1:
            # Mark the right boundary if left has been set and the next value is 0 or end of list
            if (x < len(array) - 1 and array[x + 1] == 0) \
                    or (x == len(array) - 1 and array[x] != 0):
                right = x

    return left, right


class Vector(np.ndarray):
    """
    Vector subclass the numpy ndarray class to benefit directly from the numpy features.
    Implement a simple 3x1 array matrix with an ability to do 90° rotations in all 3 axis centered at origin (0, 0, 0).
    """
    x_rotate_matrix = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    y_rotate_matrix = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
    z_rotate_matrix = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, (3,), dtype=int)

    def __init__(self, x=0, y=0, z=0):
        self[:] = [x, y, z]

    def __getattr__(self, item):
        # For convenience, we can access the 3 values by they name (.x, .y or .z) to avoid to use of unclear indexes
        # like [0], [1] or [2]
        try:
            if item in ['x', 'y', 'z']:
                return self[['x', 'y', 'z'].index(item)]
        except ValueError:
            raise AttributeError(f"No such attribute: {item}") from None

    def rotate(self, rotate_x_axis=0, rotate_y_axis=0, rotate_z_axis=0):
        # Rotate 90° from all 3 axis. This rotation all 3 at the same, and has many as we want
        # Handy for rotating counterclockwise on a specific axis, we just need to set 3 rotations for that axis
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
    """
    Point subclass the Vector class with nothing else because technically the needed methods and attributes are the same
    Using a class named Point for the points helps the code to be more readable
    """
    pass


class Direction:
    """
    Direction implement a direction by an identifier.
    By convention the up direction ID is set to 0. Incrementing the identifier by 1 rotate the direction
    by 90° clockwise.
    """
    DIRECTION_UP = 0
    DIRECTION_RIGHT = 1
    DIRECTION_DOWN = 2
    DIRECTION_LEFT = 3

    def __init__(self, direction=DIRECTION_UP):
        self.direction = direction

    def turn(self, direction):
        if direction == 'R':
            # If we turn right (clockwise), increment by 1
            self.direction = (self.direction + 1) % 4
        elif direction == 'L':
            # If we turn left (counterclockwise), decrement by 1
            self.direction = (self.direction - 1) % 4
        else:
            raise TypeError(f"Invalid direction {direction}")


class Edge:
    """
    Edge represent one edge of the cube, it is composed of an identifier, a point and a vector
    """
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
        # Rotate the edge according to a direction (looking from the top)
        # We rotate 3 times to do a 90° rotation counterclockwise.
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


class Cube:
    """
    Cube represent the cube, it is composed of 12 edges
    """
    def __init__(self, edges=None):
        if edges:
            self._edges = edges
        else:
            self._edges = self._init_edges()

    def __copy__(self):
        edges = [copy(e) for e in self._edges]
        return Cube(edges)

    def __repr__(self):
        return f"EdgeNet({[e for e in self._edges]})"

    def _init_edges(self):
        # Initialize the 12 edges with their points and vectors, according the convention described in
        # the preamble above.
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
        # Rotate the cube according to direction (looking from the top)
        for e in self._edges:
            e.rotate(direction)

    def find_top_edges(self):
        # Find and return the 4 edges located at the top of the cube.
        # More precisely, we are looking for edges located at z=1, with vector facing right or left for horizontal
        # edges, and with vector facing up or down for vertical edges
        # We compared to edge with identifier set to 0, because this ID does not matter for the comparison
        top_edges = []

        for e in self._edges:
            # Find the edge located at the top
            if e == Edge(0, Point(-1, 1, 1), Vector(1, 0, 0)) or \
                    e == Edge(0, Point(1, 1, 1), Vector(-1, 0, 0)):
                top_edges.append(e)

        for e in self._edges:
            # Find the edge located at the right
            if e == Edge(0, Point(1, 1, 1), Vector(0, -1, 0)) or \
                    e == Edge(0, Point(1, -1, 1), Vector(0, 1, 0)):
                top_edges.append(e)

        for e in self._edges:
            # Find the edge located at the bottom
            if e == Edge(0, Point(1, -1, 1), Vector(-1, 0, 0)) or \
                    e == Edge(0, Point(-1, -1, 1), Vector(1, 0, 0)):
                top_edges.append(e)

        for e in self._edges:
            # Find the edge located at the left
            if e == Edge(0, Point(-1, -1, 1), Vector(0, 1, 0)) or \
                    e == Edge(0, Point(-1, 1, 1), Vector(0, -1, 0)):
                top_edges.append(e)

        return top_edges


class Face:
    """
    Face represent a face from a cube net and contains:
      - its size in terms of tiles (useful to compute the coordinate on the tiles map)
      - its coordinate on the cube net (not its coordinate on the tiles map), considering the net as a grid of faces
      - its 4 edges
    """
    def __init__(self, size, coord, edges):
        self.size = size
        self.coord = coord
        self.edges = edges

    def __repr__(self):
        return f"Face(<{self.coord}>" \
               f" ^:{self.edges[Direction.DIRECTION_UP]}," \
               f" >:{self.edges[Direction.DIRECTION_RIGHT]}," \
               f" v:{self.edges[Direction.DIRECTION_DOWN]}," \
               f" <:{self.edges[Direction.DIRECTION_LEFT]})"

    def is_adjacent(self, other):
        # Find if 2 face are adjacent to each other. If this the case, the 2 face must be located either up-down or
        # left-right
        delta = abs(np.array(self.coord) - np.array(other.coord))
        return (delta[0] == 1 and delta[1] == 0) or (delta[0] == 0 and delta[1] == 1)

    def edge_id_direction(self, edge_id):
        # Find the edge which has a specific ID
        for n in range(len(self.edges)):
            if self.edges[n].id == edge_id:
                return n
        return -1

    def get_coords_from_edge(self, direction):
        # Build a list of coordinates for a specific edge whose direction si given
        # For instance, for a face of size 5 and its edge facing DOWN direted to the left, the method will
        # return the following list: [(4, 4), (3, 4), (2, 4), (1, 4), (0, 4)]
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
    """
    Face represent a tiles map
    """
    TILE_EMPTY = 0x0
    TILE_OPEN = 0X1
    TILE_FACING_UP = 0x0002
    TILE_FACING_RIGHT = 0x0102
    TILE_FACING_DOWN = 0x0202
    TILE_FACING_LEFT = 0x0302
    TILE_WALL = 0x10

    # For reading input file only and display the tiles map
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
        self.cube = Cube()
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
        # For part 1 only
        # Start with rows, get the left coordinate to the right coordinate, and the second one from the right to the
        # left coordinate. Create 2 jumps on both directions
        # Take advantage of this process to set the starting position on the first row, which is as stated:
        # the leftmost open tile of the top row
        for y in range(self.tiles.shape[1]):
            x_start, x_end = find_boundaries(self.tiles[:, y])
            if y == 0:
                self.position = (x_start, 0)
            self.jumps[(x_start, y, 3)] = (x_end, y, 0)
            self.jumps[(x_end, y, 1)] = (x_start, y, 0)

        # Same process for the columns.
        for x in range(self.tiles.shape[0]):
            y_start, y_end = find_boundaries(self.tiles[x, :])
            self.jumps[(x, y_start, 0)] = (x, y_end, 0)
            self.jumps[(x, y_end, 2)] = (x, y_start, 0)

    def set_jumps_as_cube(self):
        # For part 2 only
        # Analyse the faces and get the cube net mapping
        self.analyse_faces()

        # Process the 12 edges sequentially (edge ID 1 to 12)
        for edge_id in range(1, 13):
            faces = []
            # Find which 2 face which has this edge ID
            for face in self.faces.values():
                edge_direction = face.edge_id_direction(edge_id)
                if edge_direction != -1:
                    faces.append((face, edge_direction))

            # We SHOULD have 2 faces (otherwise the cube net is buggy)
            if len(faces) == 2:
                face1, edge_direction1 = faces[0]
                face2, edge_direction2 = faces[1]
                v1 = face1.edges[edge_direction1].vector
                v2 = face2.edges[edge_direction2].vector

                # Compute the coordinates this edge for 2 face and applied to the tiles map
                # Each pair together to build the jumps (zip() method)
                for coord1, coord2 in zip(face1.get_coords_from_edge(edge_direction1),
                                          face2.get_coords_from_edge(edge_direction2)):
                    # To optimize a little bit, we try to avoid creating jumps for faces which are adjacent
                    # because they path are continuous in the tiles map
                    if not ((v1 == v2).all() and face1.is_adjacent(face2)):
                        coord1 = (face1.size * face1.coord[0] + coord1[0],
                                  face1.size * face1.coord[1] + coord1[1])
                        coord2 = (face2.size * face2.coord[0] + coord2[0],
                                  face2.size * face2.coord[1] + coord2[1])
                        # Set the jump from coord1 to coord2
                        # The rotation is the difference between the direction of the 2 edge, but a rotation of 180°
                        # (the -2 subtraction) because we consider that we "enter" the new face from outside, so we
                        # are 180° turned compared to the edge direction (i.e. for an edge facing up, we "enter" it
                        # downward)
                        self.jumps[(coord1[0], coord1[1], edge_direction1)] = \
                            (coord2[0], coord2[1], (edge_direction2 - 2) % 4 - edge_direction1)

                        # Same for the opposite
                        self.jumps[(coord2[0], coord2[1], edge_direction2)] = \
                            (coord1[0], coord1[1], (edge_direction1 - 2) % 4 - edge_direction2)

    def analyse_faces(self):
        # Find the face size, by computing the GCD of the with and height of the tiles map
        self.face_size = np.gcd(self.tiles.shape[0], self.tiles.shape[1])

        starting_face = None

        # We start at the top because the starting face is always at this position (same statement as part 1)
        # We're looking from left to right
        for y in range(self.tiles.shape[1] // self.face_size):
            for x in range(self.tiles.shape[0] // self.face_size):
                if self.tiles[x * self.face_size, y * self.face_size] != self.TILE_EMPTY and not starting_face:
                    # The first face encountered is the starting face, so we note it
                    starting_face = (x, y)

        self.travel_through_faces(self.cube, starting_face)
        self.position = (starting_face[0] * self.face_size, starting_face[1] * self.face_size)

    def travel_through_faces(self, cube, face_coord):
        # Travel recursively using a kind of flood fill algorithm

        # Return immediately if we already have checked this face
        if face_coord in self.faces:
            return

        # If this coordinate contains a non-empty tiles, we consider this is a face, so we create a new face
        # and insert it
        if self.tiles[face_coord[0] * self.face_size, face_coord[1] * self.face_size] != self.TILE_EMPTY:
            self.faces[face_coord] = Face(self.face_size, face_coord, cube.find_top_edges())

        if 0 < face_coord[0] < (self.tiles.shape[0] // self.face_size) - 1:
            # Looking at a possible face at the right
            if self.tiles[(face_coord[0] + 1) * self.face_size, face_coord[1] * self.face_size] != self.TILE_EMPTY:
                # We copy our cube and pass it to the function because it is important to keep its state after
                # having travelled recursively
                new_cube = copy(cube)
                new_cube.rotate(Direction.DIRECTION_RIGHT)
                self.travel_through_faces(new_cube, (face_coord[0] + 1, face_coord[1]))
            # Looking at a possible face at the left
            if self.tiles[(face_coord[0] - 1) * self.face_size, face_coord[1] * self.face_size] != self.TILE_EMPTY:
                new_cube = copy(cube)
                new_cube.rotate(Direction.DIRECTION_LEFT)
                self.travel_through_faces(new_cube, (face_coord[0] - 1, face_coord[1]))

        if 0 <= face_coord[1] < (self.tiles.shape[1] // self.face_size) - 1:
            # Looking at a possible face down
            if self.tiles[face_coord[0] * self.face_size, (face_coord[1] + 1) * self.face_size] != self.TILE_EMPTY:
                new_cube = copy(cube)
                new_cube.rotate(Direction.DIRECTION_DOWN)
                self.travel_through_faces(new_cube, (face_coord[0], face_coord[1] + 1))

        # Since we started at the top of the tiles map, I considered we do not need to look upward.
        # This needs to be confirmed ...

    def get_next_position(self):
        # Get the next position considering the jumps

        # We check if we need to jump, so we build the key
        jump_key = (self.position[0], self.position[1], self.facing.direction)
        if jump_key in self.jumps:
            # If found, we return the new jump position and rotation needed
            position = (self.jumps[jump_key][0], self.jumps[jump_key][1])
            facing_delta = self.jumps[jump_key][2]

        else:
            # If not, we return the next position depending on the current direction, with no turn (delta = 0)
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
        # Travel according the directions and turns given

        for direction in self.directions:
            steps = direction[0]
            while steps > 0:

                next_position, facing_delta = self.get_next_position()
                # Set the direction on tiles map, this is not necessary to do this because it won't affect to
                # final result, but it helps a lot when debugging
                self.tiles[self.position] = 0x02 | (self.facing.direction << 8)

                if self._is_wall(self.tiles[next_position]):
                    # If the next position is the wall, we stop immediately
                    break

                if steps > 0:
                    # If we still have step to proceed, go forward (jumping or not, we don't care at this stage)
                    self.position = next_position
                    self.facing.direction += facing_delta

                steps -= 1

            # If we have to turn, then turn and update the direction on tiles map
            if direction[1]:
                self.facing.turn(direction[1])
            self.tiles[self.position] = 0x02 | (self.facing.direction << 8)

        return self.get_final_password()

    def get_final_password(self):
        # Compute the final password, we just the facing value, because the right direction has ID 0
        # (subtracting 1 mod 4 do the conversion)
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
