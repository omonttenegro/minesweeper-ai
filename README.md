# Minesweeper AI

A Python project developed for **CS50’s Introduction to Artificial Intelligence with Python**, focused on building an AI capable of playing Minesweeper using logical inference.

## Overview

This project combines game logic, knowledge representation, and a graphical interface to recreate the classic **Minesweeper** game.

The system includes:

- a full Minesweeper game implementation
- an AI agent that reasons about the board using logical sentences
- a graphical interface built with **Pygame**
- support for both manual play and AI-assisted moves

The AI keeps track of known safe cells, known mines, and inferred knowledge in order to make increasingly informed decisions.

## Main Features

- playable Minesweeper game
- AI that marks safe cells and mines through inference
- random move fallback when no safe move is known
- interactive graphical interface with Pygame
- support for reset and AI move actions
- visual assets for mines and flags

## Technologies Used

- **Python**
- **Pygame**
- Logical inference
- Knowledge-based AI
- Object-oriented programming

## Repository Structure

```text
minesweeper-ai/
├── README.md
├── requirements.txt
├── minesweeper.py
├── runner.py
├── assets/
│   └── images/
│       ├── flag.png
│       └── mine.png
└── .gitignore
```

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## How to Run

Run the graphical game with:

```bash
python runner.py
```

You can:

- play manually
- let the AI make moves
- reset the board and start again

## How the AI Works

The AI stores knowledge as logical sentences about sets of cells and the number of mines among them.

From that knowledge, it can:

- mark cells that are certainly safe
- mark cells that are certainly mines
- infer new sentences from existing ones
- choose a safe move when possible
- otherwise make a random valid move

This allows the AI to gradually improve its understanding of the board as the game progresses.

## Author

**André Montenegro**
