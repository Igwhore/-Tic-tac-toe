import numpy as np
import random
import matplotlib.pyplot as plt


class RandomAgent:
    def choose_action_from_txt(self, state, possible_actions):
        return random.choice(possible_actions)


class QLearningAgent:
    def __init__(self, epsilon=0.1, alpha=0.2, gamma=0.9):
        self.epsilon = epsilon  # параметр исследования
        self.alpha = alpha  # скорость обучения
        self.gamma = gamma  # дисконт-фактор
        #self.q_values = {}  # Q-значения
        self.Q = {}
        self.x = []
        self.y = []
    def write_q(self):
        file = open('info.txt', 'w')
        for key, value in self.Q.items():
            file.write(f'{key}, {value}\n')
        file.close()
    def get_q(self):
        file = open('test.txt', 'r')
        for line in file:
            key = int(line.rstrip('\n').split(',')[0])
            value = float(line.rstrip('\n').split(',')[1])
            self.Q[key] = float(value)
        file.close()
    def getQ(self, a1, a2, a3, b1, b2, b3, c1, c2, c3):
        Id = ((((((((a1 * 3) + a2) * 3 + a3) * 3 + b1) * 3 + b2) * 3 + b3) * 3 + c1) * 3 + c2) * 3 + c3
        return Id
    """def get_q_value(self, state, action):
        return self.q_values.get((state, action), 0.0)"""

    """def choose_action(self, state, possible_actions):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(possible_actions)  # случайное действие с вероятностью epsilon
        else:
            q_values = [self.get_q_value(state, a) for a in possible_actions]
            max_q = max(q_values)
            best_actions = [a for a, q in zip(possible_actions, q_values) if q == max_q]
            return random.choice(best_actions)"""

    def choose_action_from_txt(self, state, possible_actions):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(possible_actions)  # случайное действие с вероятностью epsilon
        else:
            q_values = [self.Q.get(self.getQ(state[0][0], state[0][1], state[0][2], state[1][0], state[1][1], state[1][2], state[2][0], state[2][1], state[2][2])) for a in possible_actions]
            max_q = max(q_values)
            best_actions = [a for a, q in zip(possible_actions, q_values) if q == max_q]
            return random.choice(best_actions)

    """def update_q_value(self, state, action, reward, next_state):
        possible_actions_next = self.get_possible_actions(next_state)
        if not possible_actions_next:
            max_q_next = 0  # если действий нет, считаем максимальное Q-значение равным 0
        else:
            max_q_next = max([self.get_q_value(next_state, a) for a in possible_actions_next])

        new_q = (1 - self.alpha) * self.get_q_value(state, action) + \
                self.alpha * (reward + self.gamma * max_q_next)
        self.q_values[(state, action)] = new_q"""

    def update_q_value_from_txt(self, state, action, reward, next_state):
        possible_actions_next = self.get_possible_actions(next_state)
        if not possible_actions_next:
            max_q_next = 0  # если действий нет, считаем максимальное Q-значение равным 0
        else:
            max_q_next = max([self.Q.get(self.getQ(state[0][0], state[0][1], state[0][2], state[1][0], state[1][1], state[1][2], state[2][0], state[2][1], state[2][2])) for a in possible_actions_next])

        new_q = (1 - self.alpha) * self.Q.get(self.getQ(state[0][0], state[0][1], state[0][2], state[1][0], state[1][1], state[1][2], state[2][0], state[2][1], state[2][2])) + \
                self.alpha * (reward + self.gamma * max_q_next)
        self.Q[self.Q.get(self.getQ(state[0][0], state[0][1], state[0][2], state[1][0], state[1][1], state[1][2], state[2][0], state[2][1], state[2][2]))] = new_q

    def get_possible_actions(self, state):
        return [i for i, val in enumerate(state) if val == 0]


def print_board(board):
    for row in board:
        row_str = " | ".join(map(str, row))
        print(row_str)
        print("-" * len(row_str))


def check_winner(board):
    for row in board:
        if len(set(row)) == 1 and row[0] != 0:
            return row[0]

    for col in range(3):
        if len(set([board[row][col] for row in range(3)])) == 1 and board[0][col] != 0:
            return board[0][col]

    if len(set([board[i][i] for i in range(3)])) == 1 and board[0][0] != 0:
        return board[0][0]

    if len(set([board[i][2 - i] for i in range(3)])) == 1 and board[0][2] != 0:
        return board[0][2]

    return 0


def train_agents(smart_agent, random_agent, num_episodes=200000):
    wins = 0
    loses = 0
    smart_agent.get_q()

    for match in range(num_episodes):
        board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        current_agent = smart_agent

        while True:
            state = tuple(map(tuple, board))
            possible_actions = [(i, j) for i in range(3) for j in range(3) if board[i][j] == 0]

            action = current_agent.choose_action_from_txt(state, possible_actions)
            row, col = action
            board[row][col] = 1  # Ход текущего агента

            next_state = tuple(map(tuple, board))
            winner = check_winner(board)

            if winner:
                reward = 1 if winner == 1 else -1
                if current_agent == smart_agent:
                    wins += 1
            else:
                reward = 0
                if current_agent == smart_agent:
                    loses += 1

            if current_agent == smart_agent:
                current_agent.update_q_value_from_txt(state, action, reward, next_state)

            if winner:
                board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Начать новую игру
                break

            if current_agent == smart_agent:
                current_agent = random_agent

            else:
                if current_agent == random_agent:
                    current_agent = smart_agent

        if match % 10000 == 0:
            smart_agent.x.append(match)
            smart_agent.y.append(wins)
            wins = 0



def main():
    smart_agent = QLearningAgent()
    random_agent = RandomAgent()
    # Обучение умного агента с глупым
    train_agents(smart_agent, random_agent, num_episodes=200000)
    plt.plot(smart_agent.x, smart_agent.y)
    plt.show()

    # Игра с обученным ботом
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    """while True:
        state = tuple(map(tuple, board))
        possible_actions = [(i, j) for i in range(3) for j in range(3) if board[i][j] == 0]
        action = smart_agent.choose_action_from_txt(state, possible_actions)
        row, col = action
        board[row][col] = 1  # Ход бота

        winner = check_winner(board)
        if winner:
            print_board(board)
            print("Бот", "Победил!" if winner == 1 else "Проиграл!")
            break
        print_board(board)
        row = int(input("Введите номер строки (0-2): "))
        col = int(input("Введите номер столбца (0-2): "))
        if board[row][col] == 0:
            board[row][col] = -1  # Ход игрока
        else:
            print("Неверный ход, попробуйте снова.")
            continue

        winner = check_winner(board)
        if winner:
            print_board(board)
            print("Игрок", "Победил!" if winner == -1 else "Проиграл!")
            break"""


if __name__ == "__main__":
    main()
