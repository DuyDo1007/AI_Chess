# AI_Chess

A modern, interactive chess game powered by AI.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [Testing](#testing)
- [License](#license)

---

## Overview

**AI_Chess** is a Python-based chess application that lets you play against a computer opponent. It is designed for both casual players and developers interested in chess AI or game development. The project emphasizes ease of use, a clean interface, and robust move validation.

---

## Demo Video

https://youtu.be/TeifJeOFReA

## Features

- **Easy Game Setup:** Start a new game instantly with a single click.
- **Intuitive Interface:** Click to select and move pieces, with visual highlights for valid moves.
- **AI Opponent:** Challenge a built-in AI that makes intelligent moves.
- **Move Validation:** All moves are checked for legality according to chess rules.
- **Undo/Redo:** Step back through your move history.
- **Save/Load:** Save your game progress and resume later.
- **Pawn Promotion:** Choose your promotion piece when a pawn reaches the last rank.
- **Check and Checkmate Detection:** Get clear notifications for check and checkmate situations.
- **Move History & AI Thinking Time:** View a log of moves and see how long the AI takes to think.

---

## Getting Started

### Prerequisites

- **Python 3.7+**
- **pip** (Python package manager)
- (Optional) **conda** if you prefer environment management

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DuyDo1007/AI_Chess.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd AI_Chess
   ```
3. **Install dependencies:**
   - If using pip:
     ```bash
     pip install -r requirements.txt
     ```
   - Or with conda:
     ```bash
     conda env create -f environment.yml
     conda activate <your_env_name>
     ```

### Usage

1. **Run the application:**
   - To play the standard PvP game (no AI opponent), run:
     ```bash
     python main.py
     ```
   - To play against the AI, run:
     ```bash
     python main_ai.py
     ```
2. **Controls:**
   - Click on a piece to select it, then click a highlighted square to move.
   - Use the "Save" and "Load" buttons to manage your game state.
   - Press `Ctrl+Z` to undo your last move.
   - When a pawn reaches the last rank, select the piece for promotion.

---

## Testing

# To run tests (if available):

3.  Install the dependencies:
    (Note: The exact command depends on how dependencies are managed, e.g., requirements.txt or environment.yml. Common commands are:)
    ```
    pip install -r requirements.txt
    ```
    or
    ```
    conda env create -f environment.yml
    conda activate <your_env_name>
    ```
