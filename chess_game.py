import chess
import numpy as np

class QAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_prob=0.1):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_prob = exploration_prob
        self.q_table = {}
   
    def get_legal_moves(self, state):
        board = chess.Board(fen=state)
        return [move.uci() for move in board.legal_moves]

    def choose_action(self, state):
        legal_moves = self.get_legal_moves(state)

        if not legal_moves or np.random.rand() < self.exploration_prob:
            return np.random.choice(legal_moves)
        else:
            return max(legal_moves, key=lambda a: self.get_q_value(state, a))

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def update_q_value(self, state, action, reward, next_state):
        legal_moves = self.get_legal_moves(next_state)
        a=type(reward)
        print(a)
        if legal_moves:
            best_next_action = max(legal_moves, key=lambda a: self.get_q_value(next_state, a))
            best_next_q_value = self.get_q_value(next_state, best_next_action)
            updated_q_value = (1 - self.learning_rate) * self.get_q_value(state, action) + \
                              self.learning_rate * (reward + self.discount_factor * best_next_q_value)
            self.q_table[(state, action)] = updated_q_value
        else:
            print("a")
        # Handle the case when there are no legal moves
            updated_q_value = (1 - self.learning_rate) * self.get_q_value(state, action) + \
                          self.learning_rate * reward
            self.q_table[(state, action)] = updated_q_value

def display_board(board):
    print("  abcdefgh")
    print(" +----------------")
    for rank in range(7, -1, -1):
        row = "{}|".format(rank + 1)
        for file in range(8):
            piece = board.piece_at(chess.square(file, rank))
            if piece is None:
                row += " "
            else:
                row += piece.symbol()
        print(row)
    print(" +----------------")
    print("  abcdefgh")
    turn = "White" if board.turn == chess.WHITE else "Black"
    print(f"Turn: {turn}")

def train_q_learning_agent(episodes):
    agent = QAgent()

    for _ in range(episodes):
        board = chess.Board()
        display_board(board)
        while not board.is_game_over():
            print("Board before any moves")
            current_state = board.fen()
            legal_moves = agent.get_legal_moves(current_state)
            if legal_moves:
                action = agent.choose_action(current_state) 
                print("Before Rewards function")
                reward = calculate_reward(board,action)
                print("After Rewards function")#Taking rewards after move has happened
                board.push_uci(action)#move But is it for white or black
                next_state = board.fen()
                agent.update_q_value(current_state, action, reward, next_state)
                print("After moving with"+action)
                display_board(board)
            else:
                break
    return agent
def calculate_reward(board,action):
    reward=0
    board.push_uci(action)
    if board.is_checkmate():
        print("For checkmate 1.0")
        reward= 1.0  # Checkmate reward
    elif board.is_check():
        print("check 0.4")
        reward =0.4  # Check reward
    elif board.is_stalemate() or board.is_variant_draw():
        print("For just nothing 0.0")
        reward =0.0  # Draw reward
    elif board.is_capture(chess.Move.from_uci(action)):
        captured_piece = board.piece_at()
        print(captured_piece)
        if captured_piece:
            piece_type = captured_piece.piece_type
            if piece_type == chess.QUEEN:
                print("For queen 0.3")
                reward= 0.3
            elif piece_type == chess.ROOK:
                print("For rook 0.15")
                reward =0.15
            elif piece_type == chess.BISHOP:
                print("For bishop 0.15")
                reward =0.15
            elif piece_type == chess.KNIGHT:
                print("For knight 0.15")
                reward =0.15
            elif piece_type == chess.PAWN:
                print("for pawn0.1")
                reward =0.1
    
    elif board.is_castling(chess.Move.from_uci(action)):#Castling is a key move for king safety and connecting rooks
        print("for castling 0.4")
        reward= 0.4  # Castling reward

        # Evaluate material advantage
    #white_material = sum(piece.value for piece in board.piece_map().values() if piece.color == chess.WHITE)
    white_material = sum(piece.piece_type for piece in board.piece_map().values() if piece.color == chess.WHITE)
    #black_material = sum(piece.value for piece in board.piece_map().values() if piece.color == chess.BLACK)
    black_material = sum(piece.piece_type for piece in board.piece_map().values() if piece.color == chess.BLACK)

    material_advantage = (white_material - black_material) / 100.0
    print("reward+material_advantage")
    print("material_advantage")
    print(material_advantage)
    print(reward+material_advantage)
    return material_advantage+reward

def human_vs_agent(agent,human_side):
    print(human_side)
    max_moves=1000
    print("Original game after Agent's Reinforncement Learning")
    board = chess.Board()
    display_board(board)

    for _ in range(max_moves):
        if board.is_game_over():
            print("Game Over. Result: {}".format(board.result()))
            break

        if board.turn == chess.WHITE:
            #print(board.legal_moves)
            move_uci = input("White(Your) move (in UCI format): ")
            while move_uci not in [move.uci() for move in board.legal_moves]:
                print("Invalid move. Please try again")
                print("These are the legal moves, please select from them"+board.legal_moves)
                move_uci = input("White(Your) move (in UCI format): ")
            board.push_uci(move_uci)#Move for human value
        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_variant_draw():
            print("Game Over. Result: {}".format(board.result()))
            break
       
        move_uci_agent = agent.choose_action(board.fen())
        while move_uci_agent not in [move.uci() for move in board.legal_moves]:
            print("Agent made an invalid move. Regenerating...")
            move_uci_agent = agent.choose_action(board.fen())
        print("Agent's move:", move_uci_agent)
        board.push_uci(move_uci_agent)#Agents move
        print("Board After both turns")
        display_board(board)

        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_variant_draw():
            print("Game Over. Result: {}".format(board.result()))
            break


        current_state = board.fen()
        reward = 0.0  # You may need to define a suitable reward
        next_state = board.fen()
        agent.update_q_value(current_state, move_uci_agent, reward, next_state)

if __name__ == "__main__":
    trained_agent = train_q_learning_agent(episodes=1000)
    human_side = chess.WHITE  # Set to chess.WHITE if the human is playing as White
    human_vs_agent(trained_agent, human_side)
