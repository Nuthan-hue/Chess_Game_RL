# Chess_Game_RL
Q-Learning Chess Agent User Manual
1. Overview:
The provided Python code implements a Q-learning-based chess-playing agent. Q-learning is a reinforcement learning algorithm used for making decisions in an environment based on learning from experiences.

2. Classes:
QAgent:

This class represents the Q-learning agent. It has methods for initializing the agent, choosing actions, getting legal moves, calculating Q-values, and updating Q-values.

3. Functions:

__init__(self, learning_rate=0.1, discount_factor=0.9, exploration_prob=0.1):

Initializes the QAgent with default or user-defined values for learning rate, discount factor, and exploration probability.
get_legal_moves(self, state):

Returns a list of legal moves in the given chess state.
choose_action(self, state):

Chooses an action based on Q-values or exploration.
get_q_value(self, state, action):

Returns the Q-value for a given state-action pair.
update_q_value(self, state, action, reward, next_state):

Updates the Q-value based on the Q-learning update rule.
display_board(board):

Function to display the chessboard and the current turn.
train_q_learning_agent(episodes):

Trains the Q-learning agent over a specified number of episodes.
calculate_reward(board, action):

Calculates the reward for a given action in the current board state.
human_vs_agent(agent, human_side):

Allows a human to play against the trained Q-learning agent.


4. Training the Agent:
To train the agent, call the train_q_learning_agent function with the desired number of episodes (training iterations).
python
Copy code
trained_agent = train_q_learning_agent(episodes=1000)


5. Playing Against the Agent:
Use the human_vs_agent function to play against the trained agent.
Set human_side to chess.WHITE if the human wants to play as White.
python
Copy code
human_side = chess.WHITE  # Set to chess.WHITE if the human is playing as White
human_vs_agent(trained_agent, human_side)


6. Playing Moves:
When playing moves, use [UCI (Universal Chess Interface)](https://en.wikipedia.org/wiki/Universal_Chess_Interface) format for move input.


7. Observing Rewards:
The calculate_reward function defines the rewards for different scenarios (checkmate, check, capture, castling, material advantage). Adjustments to the reward function can be made as needed.


8. Display:
The display_board function shows the current state of the chessboard.


9. Notes:
The code uses the python-chess library for chess-related functionalities.


10. Dependencies:
The code depends on the chess library. Install it using:
Copy code
pip install python-chess


11. Further Customization:
Users can customize learning parameters, reward functions, and other aspects of the code to experiment and improve the agent's performance.
Feel free to experiment with different parameters, reward functions, and training episodes to observe how the agent learns to play chess.
