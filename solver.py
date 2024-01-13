import heapq
from puzzle import Application  # Make sure 'puzzle' is the correct module name

class PuzzleSolver:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_state = self.get_goal_state()
        self.moves = self.solve()

    def get_goal_state(self):
        goal_state = []
        for x in range(self.initial_state.board_grid):
            for y in range(self.initial_state.board_grid):
                goal_state.append((x, y))
        return tuple(goal_state)

    def heuristic(self, state):
        # Manhattan Distance Heuristic
        distance = 0
        for i in range(len(state)):
            x1, y1 = state[i]
            x2, y2 = self.goal_state[i]
            distance += abs(x1 - x2) + abs(y1 - y2)
        return distance

    def get_neighbors(self, state):
        neighbors = []
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                neighbor = list(state)
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(tuple(neighbor))
        return neighbors

    def solve(self):
        start_state = tuple(piece['pos_a'] for piece in self.initial_state.board if piece['visible'])
        priority_queue = [(self.heuristic(start_state), start_state, [])]
        visited_states = set()

        while priority_queue:
            _, current_state, moves = heapq.heappop(priority_queue)

            if current_state == self.goal_state:
                return moves

            if current_state in visited_states:
                continue

            visited_states.add(current_state)

            for neighbor in self.get_neighbors(current_state):
                if neighbor not in visited_states:
                    heapq.heappush(priority_queue, (len(moves) + self.heuristic(neighbor), neighbor, moves + [neighbor]))

        return None

if __name__ == "__main__":
    try:
        solver_app = Application("spider.jpg", 4)
        solver = PuzzleSolver(solver_app)
        print("Solution Moves:", solver.moves)
    except Exception as e:
        print("Error:", str(e))
