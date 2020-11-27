from funcs import *
from copy import deepcopy
import random
from heapq import *
import sys

class AIPlayer:

    def __init__(self):
        pass

    def get_top_side_positions(self, board):
        side_positions = []
        for c in range(len(board)):
            side_positions.append([0,c])
        return side_positions

    def get_bottom_side_positions(self, board):
        side_positions = []
        for c in range(len(board)):
            side_positions.append([len(board)-1, c])
        return side_positions

    def get_left_side_positions(self, board):
        side_positions = []
        for c in range(len(board)):
            side_positions.append([c,0])
        return side_positions

    def get_right_side_positions(self, board):
        side_positions = []
        for c in range(len(board)):
            side_positions.append([c, len(board)-1])
        return side_positions

    def get_side_positions(self, board, color):
        if color == 1:
            return self.get_top_side_positions(board) + self.get_bottom_side_positions(board)
        elif color == 2:
            return self.get_left_side_positions(board) + self.get_right_side_positions(board)            

    def is_empty(self, board, r, c):
        return board[r][c] == 0

    def get_legal_moves(self, board):
        moves = []
        for r in range(len(board)):
            for c in range(len(board)):
                if self.is_empty(board, r, c):
                    moves.append([r,c])
        return moves

    def get_opponent_player(self, current_player):
        return 3 - current_player
    
    def undo(self, board, r, c):
        board[r][c] = 0
        self.current_player = self.get_opponent_player(self.current_player)

    def play_move(self, board, r, c):
        board[r][c] = self.current_player
        self.current_player = self.get_opponent_player(self.current_player)

    def check_win(self, board):
        '''checks if any of the players have won'''
        for y in range(len(board)):
            if board[y][0] == 2:
                if DFS(Point(y, 0), board, lambda v: (v.Y == len(board)-1), 2):
                    return 2
        for x in range(len(board)):
            if board[0][x] == 1:
                if DFS(Point(0, x), board, lambda v: (v.X == len(board)-1), 1):
                    return 1
        return 0

    def random_player(self, board):
        moves = self.get_legal_moves(board)
        return random.choice(moves)

    def simulation_play_out(self, board):
        result = self.check_win(board)
        simulation_moves = []
        while result == 0:
            moves = self.get_legal_moves(board)
            play_move = random.choice(moves)
            self.play_move(board, play_move[0], play_move[1])
            simulation_moves.append(play_move)
            result = self.check_win(board)
        for move in simulation_moves[::-1]:
            self.undo(board, move[0], move[1])
        if result == self.current_player:
            return -1
        else:
            return 1

    def gen_move_by_simulation_based_strategy(self, board, color):
        """
        Evaluation each move by simulate numbers of random playouts:
            win_count / visit_count
        """
        moves = self.get_legal_moves(board)
        if len(moves) == len(board)*len(board):
            # open move: to play near center
            return self.get_center_move(board)
        board = deepcopy(board)
        self.current_player = color
        best_move = None
        best_result = -1
        win_count = [0]*len(moves)
        visit_count = [0]*len(moves)
        for i in range(500):
            # iterations of simulation runs for every legal moves
            for i, move in enumerate(moves):
                self.play_move(board, move[0], move[1])
                if self.check_win(board) == color:
                    # if this move just leads to win
                    return move
                result = self.simulation_play_out(board)
                win_count[i] += result
                visit_count[i] += 1
                self.undo(board, move[0], move[1])
        for i in range(len(moves)):
            if win_count[i] / visit_count[i] > best_result:
                best_result = win_count[i] / visit_count[i]
                best_move = moves[i]
        return best_move

    def get_positions(self, board, color):
        positions = []
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] == color:
                    positions.append([r, c])
        return positions

    def get_neighbours(self, board, r, c):
        positions = []
        if r-1 >= 0:
            positions.append([r-1, c])
        if c-1 >= 0:
            positions.append([r, c-1])
        if r+1 < len(board) and c-1 >=0:
            positions.append([r+1, c-1])
        if r+1 < len(board):
            positions.append([r+1, c])
        if r-1 >= 0 and c+1 < len(board):
            positions.append([r-1, c+1])
        if c+1 < len(board):
            positions.append([r, c+1])
        return positions

    def get_neighbours_with_this_color(self, board, r, c, color):
        neighbours = self.get_neighbours(board, r, c)
        positions = []
        for pos in neighbours:
            if board[pos[0]][pos[1]] == color:
                positions.append(pos)
        return positions

    def get_bridge_positions(self, board, r, c):
        bridges = []
        board_size = len(board)
        if r+2 < board_size and c-1 >= 0:
            # bottom
            bridges.append([r+2,c-1])
        if r+1 < board_size and c-2 >= 0:
            #
            bridges.append([r+1,c-2])
        if r-1 >= 0 and c-1 >= 0:
            #
            bridges.append([r-1,c-1])
        if r-2 >= 0 and c+1 < board_size:
            #
            bridges.append([r-2,c+1])
        if r-1 >= 0 and c+2 < board_size:
            #
            bridges.append([r-1,c+2])
        if r+1 < board_size and c+1 < board_size:
            #
            bridges.append([r+1,c+1])
        return bridges

    def get_center_move(self, board):
        # ai play first
        size = len(board)
        return [size//2, size//2]

    def bfs_build_path(self, board, current, targets, unwanted, path, paths):
        if current in path:
            return
        if current in unwanted:
            return
        path.append(current)
        if current in targets:
            path.sort()
            if path not in paths:
                paths.append(path)
            return
        neighbours = self.get_neighbours(board, current[0], current[1])
        for neighbour in neighbours:
            if neighbour not in path:
                path_copy = deepcopy(path)
                self.bfs_build_path(board, neighbour, targets, unwanted, path_copy, paths)
            

    def rebuild_path(self, board, came_from, cost_so_far, paths, path, cost_left, current_node):
        if cost_left == -1:
            paths.append(path)
        else:
            for pos_string, cost in cost_so_far.items():
                pos = self.decode_move(pos_string)
                if cost == cost_left and current_node in self.get_neighbours(board, pos[0], pos[1]):
                    p_copy = deepcopy(path)
                    p_copy.append(pos)
                    self.rebuild_path(board, came_from, cost_so_far, paths, p_copy, cost_left-1, pos)

    def rebuild_a_star_path(self, pos, came_from):
        path = []
        while pos != None:
            path.append(pos)
            pos = came_from[self.encode_move(pos[0], pos[1])]
        return path

    def get_all_shortest_path_a_star(self, board, start, end):
        heap = [(-1, start)]
        came_from = {}
        cost_so_far = {}
        came_from[self.encode_move(start[0], start[1])] = None
        cost_so_far[self.encode_move(start[0], start[1])] = 0
        paths = []
        while len(heap) > 0:
            current = heappop(heap)[1]
            if current == end:
                break
            neighbours = self.get_neighbours(board, current[0], current[1])
            for pos in neighbours:
                new_cost = cost_so_far[self.encode_move(current[0], current[1])] + 1 # always cost 1
                if self.encode_move(pos[0], pos[1]) not in cost_so_far or new_cost < cost_so_far[self.encode_move(pos[0], pos[1])]:
                    cost_so_far[self.encode_move(pos[0], pos[1])] = new_cost
                    priority = new_cost + self.compute_manhattan_distance(pos[0], pos[1], end[0], end[1])
                    heappush(heap, (priority, pos))
                    came_from[self.encode_move(pos[0], pos[1])] = current
        paths.append(self.rebuild_a_star_path(end, came_from))
        return paths

    def get_all_shortest_path_dijstra(self, board, start, end, color):
        heap = [(0, start)]
        cost_so_far = {}
        came_from = {}
        came_from[self.encode_move(start[0], start[1])] = None
        cost_so_far[self.encode_move(start[0], start[1])] = 0
        paths = []
        path_exist = False
        while len(heap) > 0:
            current = heappop(heap)[1]
            if current == end:
                path_exist = True
                break
            neighbours = []
            neighbours1 = self.get_neighbours_with_this_color(board, current[0], current[1], 0)
            for neighbour in neighbours1:
                neighbours.append(neighbour)
            neighbours2 = self.get_neighbours_with_this_color(board, current[0], current[1], color)
            for neighbour in neighbours2:
                if neighbour not in neighbours:
                    neighbours.append(neighbour)
            for pos in neighbours:
                new_cost = cost_so_far[self.encode_move(current[0], current[1])] + 1
                if self.encode_move(pos[0], pos[1]) not in cost_so_far or new_cost < cost_so_far[self.encode_move(pos[0], pos[1])]:
                    cost_so_far[self.encode_move(pos[0], pos[1])] = new_cost
                    heappush(heap, (new_cost, pos))
                    came_from[self.encode_move(pos[0], pos[1])] = current
        if path_exist:
            min_cost = cost_so_far[self.encode_move(end[0], end[1])]
            self.rebuild_path(board, came_from, cost_so_far, paths, [end], min_cost-1, end)
        return paths

    def encode_move(self, r, c):
        return "%s-%s"%(r,c)

    def decode_move(self, move_string):
        return [ int(i) for i in move_string.split("-")]

    def compute_manhattan_distance(self, x1, y1, x2, y2):
        return abs(x1-x2) + abs(y1-y2)

    def get_distance_to_the_side(self, board, r, c, targets):
        distances = []
        for target in targets:
            distances.append(self.compute_manhattan_distance(r, c, target[0], target[1]))
        return min(distances)

    # def alphaBeta(self, board):
    #     max_score = -1000000000
    #     moves = self.get_legal_moves(board)
    #     board_copy = deepcopy(board)
    #     self.current_player = 3-self.current_player
    #     for move in moves:
    #         print(move)
    #         board_copy[move[0]][move[1]] = self.current_player
    #         score = self.evaluate(board, move)
    #         board_copy[move[0]][move[1]] = 0
    #         if score > max_score:
    #             max_score = score
    #     self.current_player = 3-self.current_player
    #     return max_score

    def find_all_possible_paths_contain_current_move(self, board, color, current_move, moves_so_far, opponent_moves_so_far, target_side1, target_side2):
        """
        This finds all possible paths that are generated from the existing moves and contains the current move
        """
        paths = []
        top_side_positions = self.get_top_side_positions(board)
        bottom_side_positions = self.get_bottom_side_positions(board)
        for move in moves_so_far:
            to_target1 = []
            to_target2 = []
            for pos in target_side1:
                ps = self.get_all_shortest_path_dijstra(board, move, pos, color)
                for p in ps:
                    p.sort()
                    if p not in to_target1:
                        to_target1.append(p)
            for pos in target_side2:
                ps = self.get_all_shortest_path_dijstra(board, move, pos, color)
                for p in ps:
                    p.sort()
                    if p not in to_target2:
                        to_target2.append(p)
            for path1 in to_target1:
                for path2 in to_target2:
                    p = path1 + path2
                    path = []
                    for pos in p:
                        if pos not in path:
                            path.append(pos)
                    path.sort()
                    if path not in paths and not self.is_opponent_occupy_in_this_path(path, opponent_moves_so_far) and current_move in path:
                        paths.append(path)
        return paths        

    def evaluate(self, board, current_move, color):
        """
        This is a heuristic function that evaluate the board state if this current_move is played
        and return a score for this current_move
        """
        if self.check_win(board) == color:
            # if game end
            return 1000
        moves_so_far = self.get_positions(board, color)
        opponent_moves_so_far = self.get_positions(board, 3-color)
        score = 0
        paths = []
        if color == 1:
            # green player (1st player)
            top_side_positions = self.get_top_side_positions(board)
            bottom_side_positions = self.get_bottom_side_positions(board)
            paths = self.find_all_possible_paths_contain_current_move(board, color, current_move, moves_so_far, opponent_moves_so_far, top_side_positions, bottom_side_positions)
        elif color == 2:
            # blue player
            left_side_positions = self.get_left_side_positions(board)
            right_side_positions = self.get_right_side_positions(board)
            paths = self.find_all_possible_paths_contain_current_move(board, color, current_move, moves_so_far, opponent_moves_so_far, left_side_positions, right_side_positions)
        min_move = 1000 # this keeps the minimum number of moves to finish the shortest path 
        for path in paths:
            # calculate number of move that are still needed to finish this path
            num_of_moves = self.compute_number_of_move_to_finish_this_path(path, moves_so_far)
            if num_of_moves < min_move:
                # update min move if there is a smaller
                min_move = num_of_moves
        # determine whehter or give bonus to bridge positions
        score -= min_move
        bonus = self.compute_number_of_bridge(board, current_move, moves_so_far, color)
        score += bonus
        return score
    
    def is_existing_move_occupied_two_sides(self, board, current_move, moves_so_far, color):
        if color == 1:
            top = False
            bottom = False
            top_positions = self.get_top_side_positions(board)
            bottom_positions = self.get_bottom_side_positions(board)
            for move in moves_so_far:
                if move != current_move:
                    if move in top_positions:
                        top = True
                    if move in bottom_positions:
                        bottom = True
            return top and bottom
        elif color == 2:
            left = False
            right = False
            left_positions = self.get_left_side_positions(board)
            right_positions = self.get_right_side_positions(board)
            for move in moves_so_far:
                if move != current_move:
                    if move in left_positions:
                        left = True
                    if move in right_positions:
                        right = True
            return left and right

    def is_opponent_occupy_in_this_path(self, path, opponent_moves):
        for move in opponent_moves:
            if move in path:
                return True
        return False

    def compute_number_of_bridge(self, board, current_move, moves, color):
        bonus = 0
        for move in moves:
            bridges = self.get_bridge_positions(board, move[0], move[1])
            if current_move in bridges:
                current_move_neighbours = self.get_neighbours(board, current_move[0], current_move[1])
                move_neighbours = self.get_neighbours(board, move[0], move[1])
                common_neighbours = []
                for current_move_neighbour in current_move_neighbours:
                    if current_move_neighbour in move_neighbours:
                        common_neighbours.append(current_move_neighbour)
                if self.is_empty(board, common_neighbours[0][0], common_neighbours[0][1]) and self.is_empty(board, common_neighbours[1][0], common_neighbours[1][1]):
                    bonus += 0.01
                    return bonus
        return bonus

    def compute_number_of_move_to_finish_this_path(self, path, moves):
        count = len(path)
        for move in moves:
            if move in path:
                count -= 1
        return count

    def strategy_move(self, board, color):
        center_move = self.get_center_move(board)
        if self.is_empty(board, center_move[0], center_move[1]):
            # if center move is empty play a move there
            #self.play_move(board, center_move[0], center_move[1])
            return center_move
        board_copy = deepcopy(board)
        moves = self.get_legal_moves(board)
        scores = []
        for move in moves:
            # evaluate if this is your move
            board_copy[move[0]][move[1]] = color
            score1 =  self.evaluate(board_copy, move, color)
            board_copy[move[0]][move[1]] = 0
            #scores.append([score, move])
            # evaluate if this is opponent move
            board_copy[move[0]][move[1]] = 3 - color
            score2 = self.evaluate(board_copy, move, 3-color)
            board_copy[move[0]][move[1]] = 0
            scores.append([score2+score1, move])
        scores.sort(key=lambda x: x[0])
        return scores[-1][1]
