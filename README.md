# ♟️ Real-Time AI Chess with Alpha-Beta Pruning

This project is a Python-based chess game where a human player can compete against an AI opponent using real-time decision-making powered by the **Alpha-Beta Pruning** optimization of the Minimax algorithm.

---

## 🚀 Features

- 🔁 **Real-time Gameplay** with Pygame  
- 🧠 **AI Opponent** using Alpha-Beta Pruning for decision-making  
- 🏁 Includes chess logic such as:
  - Castling
  - En Passant
  - Pawn Promotion
  - Check Detection
  - Captured Piece Display  
- 🎨 Graphical interface with interactive piece movements  
- 🎮 Human vs AI gameplay (You play as White, AI plays as Black)

---

## 🧠 How It Works

The AI module (`ai.py`) implements:
- **Board Evaluation** based on classic piece values
- **Minimax Algorithm** with Alpha-Beta Pruning to optimize decision making
- **Move Generation** for all pieces
- **Depth-limited Search** (currently set to depth = 3)

The GUI is built using `pygame`, and the game renders piece positions, valid moves, and handles user input for turn-based play.

---
