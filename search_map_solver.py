import heapq
import sys
from dataclasses import dataclass, field
from typing import Tuple, List
from collections import defaultdict
import random
from pacman_map import PacmanMap


@dataclass(order=True)
class SearchNode:
    priority: int
    score: int
    distance: int
    position: Tuple[int, int] = field(compare=False)
    path: List[Tuple[int, int]] = field(compare=False)
    food: set = field(compare=False)
    power_pellets: set = field(compare=False)

class ClockSolver:
    ADJACENT = ((-1, 0), (1, 0), (0, -1), (0, 1))
    def __init__(self, map: PacmanMap, time):
        self.map = map
        self.solution = []
        self.to_avoid = set()
        self.efficient_adjacency = defaultdict(set)

        self.can_visit = self.map.food.union(self.map.power_pellets)
        self.can_visit.add(self.map.start)
        self.can_visit.add(self.map.end)

        self.compress_graph()

        self.find_to_consume(time)

    def find_to_consume(self, time_digits):
        for time_digit, position in zip(time_digits, self.map.digit_positions):
            for digit_position in self.map.digits[time_digit].positions:
                self.to_avoid.add((position[0] + digit_position[0], position[1] + digit_position[1]))

    def compress_graph(self):
        search_stack = []
        search_stack.append(self.map.start)
        while search_stack:
            current_position = search_stack.pop()

            if current_position in self.efficient_adjacency:
                continue
            for direction in self.ADJACENT:
                check_position = current_position
                while (check_position[0] + direction[0], check_position[1] + direction[1]) in self.can_visit:
                    for trace_direction in self.ADJACENT:
                        if (trace_direction[0] != direction[0] and trace_direction[1] != direction[1]) and (check_position[0] + trace_direction[0], check_position[1] + trace_direction[1]) in self.can_visit:
                            self.efficient_adjacency[current_position].add((check_position[0], check_position[1]))
                            search_stack.append(check_position)
                    check_position = (check_position[0] + direction[0], check_position[1] + direction[1])
                if check_position in self.can_visit and check_position != current_position:
                    self.efficient_adjacency[current_position].add(check_position)
                    search_stack.append(check_position)

    def get_points(self, start, end):
        start_x = start[0]
        start_y = start[1]
        end_x = end[0]
        end_y = end[1]
        if end_x < start_x:
            start_x, end_x = end_x, start_x
        if end_y < start_y:
            start_y, end_y = end_y, start_y
        if start_x == end_x:
            return ((start_x, y) for y in range(start_y, end_y + 1))
        if start_y == end_y:
            return ((x, start_y) for x in range(start_x, end_x + 1))

    def solve(self):
        search_queue = []
        heapq.heappush(search_queue, SearchNode(0, 0, 0, self.map.start, ((self.map.start, self.map.start),), self.map.food, self.map.power_pellets))

        seen_boards = set()
        while search_queue:
            current_node = heapq.heappop(search_queue)
            #sys.stdout.write(f'{len(current_node.path):3} {len(search_queue)} {len(seen_boards)}\n')

            if current_node.position == self.map.end:
                if len(current_node.power_pellets - self.to_avoid) == 0:  # the pellets to avoid and the pellets on the board are identical
                    self.solution = current_node.path
                    print('found solution')
                    return
            shuffled_adjacency = list(self.efficient_adjacency[current_node.position])
            random.shuffle(shuffled_adjacency)
            for adjacent in shuffled_adjacency:
                new_node_food = set(current_node.food)
                new_node_power_pellets = set(current_node.power_pellets)
                new_score = current_node.score
                new_path = current_node.path + ((current_node.position, adjacent),)
                # add manhattan distance to the score
                new_distance = current_node.distance + abs(adjacent[0] - current_node.position[0]) + abs(adjacent[1] - current_node.position[1])
                should_avoid = False
                power_pellet = False
                for step in self.get_points(current_node.position, adjacent):
                    if step in self.to_avoid:
                        should_avoid = True
                        break
                    elif step in new_node_food:
                        new_node_food.remove(step)
                    elif step in new_node_power_pellets:
                        new_node_power_pellets.remove(step)
                        power_pellet = True

                if should_avoid:
                    continue
                elif power_pellet:
                    new_score -= 20

                board_data = (tuple(new_node_food), tuple(new_node_power_pellets), adjacent)
                if board_data in seen_boards:
                    continue
                seen_boards.add(board_data)
                new_search_node = SearchNode(new_distance + new_score, new_score, new_distance, adjacent, new_path, new_node_food, new_node_power_pellets)
                heapq.heappush(search_queue, new_search_node)

