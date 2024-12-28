#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2024/day/9
#

import sys
import numpy as np


class Blocks:

    BLOCK_FREE = -1

    def __init__(self):
        self.blocks = None
        self.free_blocks_index = []
        self.nonfree_blocks_index = []

    def display_blocks(self):
        # For debugging purpose, display the blocks array
        cells = [f"{self.blocks[x]}" if self.blocks[x] != -1 else '.' for x in range(self.blocks.shape[0])]
        print(''.join(cells))

    def parse_map(self, file):
        with open(file) as f:
            # Convert the map line into a list of integers representing block sizes.
            map_line = [int(x) for x in f.readline().strip()]
            # Initialize a NumPy array to represent the blocks.
            # The size of the array is the total sum of block sizes.
            self.blocks = np.ndarray((sum([block_size for block_size in map_line]),), dtype=int)

            # Fill the blocks array with the default value indicating free blocks. The array will be filled by
            # non-free blocks with their ID later on.
            self.blocks.fill(self.BLOCK_FREE)

        map_index = 0
        block_index = 0
        block_id = 0

        # Iterate over each block size in the map line.
        for block_size in map_line:
            # Create index for both and non-free blocks (will be used in part 2)
            if map_index % 2 == 0:
                # Even indices in map_line correspond to non-free blocks.
                # Append the start index and size of the non-free block to the list.
                self.nonfree_blocks_index.append([block_index, block_size])
            else:
                # Odd indices in map_line correspond to free blocks.
                if block_size > 0:
                    # Append the start index and size of the free block to the list.
                    self.free_blocks_index.append([block_index, block_size])

            # Populate the blocks array for the current block size.
            for i in range(block_size):
                if map_index % 2 == 0:
                    # Assign a block ID to non-free blocks.
                    self.blocks[block_index] = block_id

                # Increment the block index after processing each block.
                block_index += 1

            # Move to the next block in the map line.
            map_index += 1

            # Increment the block ID only after completing a non-free block.
            if map_index % 2 == 1:
                block_id += 1

    def find_first_free_block(self, offset=0):
        for i in range(offset, self.blocks.shape[0]):
            if self.blocks[i] == self.BLOCK_FREE:
                return i

        return None

    def find_first_free_block_with_size(self, size):
        for index in self.free_blocks_index:
            if index[1] >= size:
                return index[0]

        return None

    def update_free_block_index(self, offset, occupied_size):
        # Iterate through the list of free block indices to find the block at the given offset.
        for index in self.free_blocks_index:
            if index[0] == offset:
                # Reduce the size of the free block by the size of the occupied block.
                index[1] -= occupied_size
                # Update the starting position of the free block to account for the occupied space.
                index[0] += occupied_size

    def compact_blocks(self):
        # Initialize the offset to track free blocks for compaction.
        free_block_offset = 0

        # Iterate over the blocks array from the last element to the first.
        for i in range(self.blocks.shape[0] - 1, 0, -1):
            # Check if the current block is not free.
            if self.blocks[i] != self.BLOCK_FREE:
                # Find the first free block starting from the given offset. This is for time optimization only, as we're
                # filling the first free blocks one by one, there is no need to check the previous blocks
                free_block_index = self.find_first_free_block(offset=free_block_offset)

                # If a free block is found before the current block, compact the block.
                if free_block_index < i:
                    # Move the current block to the free block's position and mark the current block as free.
                    self.blocks[free_block_index] = self.blocks[i]
                    self.blocks[i] = self.BLOCK_FREE

                    # Update the offset to the index of the newly filled free block (not necessary, but for
                    # optimization as said above)
                    free_block_offset = free_block_index
                else:
                    # If no free block is found before the current block, stop compaction.
                    return

    def compact_blocks_without_frag(self):
        # Iterate over non-free block indices in reverse order, as we move in order of decreasing file ID number
        for nonfree_index in reversed(self.nonfree_blocks_index):
            # Find the first free block large enough to fit the current non-free block.
            free_block_offset = self.find_first_free_block_with_size(nonfree_index[1])

            # If a suitable free block was found and if it's located before the current non-free block.
            if free_block_offset and free_block_offset < nonfree_index[0]:
                # Move the entire non-free block to the free block's position.
                for i in range(nonfree_index[1]):
                    # Copy the value from the non-free block to the free block location and mark the original
                    # non-free block positions as free.
                    self.blocks[free_block_offset + i] = self.blocks[nonfree_index[0] + i]
                    self.blocks[nonfree_index[0] + i] = self.BLOCK_FREE

                # Update the free block index to reflect the changes after the move.
                self.update_free_block_index(free_block_offset, nonfree_index[1])

    def checksum_blocks(self):
        checksum = 0
        for i in range(self.blocks.shape[0]):
            if self.blocks[i] != self.BLOCK_FREE:
                checksum += i * self.blocks[i]

        return checksum


def day9_1(file):
    blocks = Blocks()
    blocks.parse_map(file)
    blocks.compact_blocks()
    print(blocks.checksum_blocks())


def day9_2(file):
    blocks = Blocks()
    blocks.parse_map(file)
    blocks.compact_blocks_without_frag()
    print(blocks.checksum_blocks())


if __name__ == '__main__':
    day9_1(sys.argv[1])
    day9_2(sys.argv[1])
