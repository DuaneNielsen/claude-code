#!/usr/bin/env python3
"""
Hangman MCP Server

A Model Context Protocol server that implements the classic hangman word guessing game.
Players can start games, make guesses, and get game status updates through MCP tools.

Based on the original hangman.py implementation, converted to use fastmcp.
"""

import sys
from dataclasses import dataclass, field
from random import randint
from typing import Optional, Dict, Any
from collections import namedtuple

from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("hangman-game-server")

# Type definitions from original hangman.py
PuzzleLetter = namedtuple('PuzzleLetter', ['character', 'guessed'])
Puzzle = list[PuzzleLetter]

# Global game sessions storage
game_sessions: Dict[str, 'GameState'] = {}


def get_hangman_images() -> tuple[str, ...]:
    """Return a tuple of hangman ASCII drawings."""
    return (
        r"""


    
    
    
=====""",
        r"""
    +
    |
    |
    |
    |
    |
=====""",
        r"""
 +--+
    |
    |
    |
    |
    |
=====""",
        r"""
 +--+
 |  |
    |
    |
    |
    |
=====""",
        r"""
 +--+
 |  |
 O  |
    |
    |
    |
=====""",
        r"""
 +--+
 |  |
 O  |
 |  |
    |
    |
=====""",
        r"""
 +--+
 |  |
 O  |
/|  |
    |
    |
=====""",
        r"""
 +--+
 |  |
 O  |
/|\ |
    |
    |
=====""",
        r"""
 +--+
 |  |
 O  |
/|\ |
/   |
    |
=====""",
        r"""
 +--+
 |  |
 O  |
/|\ |
/ \ |
    |
=====""",
    )


def get_word_list(category: str = 'animals') -> list[str]:
    """Return a list of quiz words."""
    category = category.lower()
    
    animal_words = """
    Dog Cat Elephant Lion Tiger Giraffe Zebra Bear Koala
    Panda Kangaroo Penguin Dolphin Eagle Owl Fox Wolf Cheetah
    Leopard Jaguar Horse Cow Pig Sheep Goat Chicken Duck Goose
    Swan Octopus Shark Whale Platypus Chimpanzee Gorilla Orangutan
    Baboon Raccoon Squirrel Bat Hedgehog Armadillo Sloth Porcupine
    Anteater Camel Dingo Kangaroo Rat Lemur Meerkat Ocelot Parrot
    Quokka Vulture Wombat Yak Iguana jaguar Kakapo Lemming
    Manatee Nutria Ostrich Pangolin Quail Rhinoceros Serval
    Wallaby Coypu Tapir Pheasant
    """
    
    word_list_dict = {'animals': animal_words}
    
    try:
        words: str = word_list_dict[category]
        return [word.upper() for word in words.split()]
    except KeyError:
        raise ValueError("Invalid category.")


def get_secret_word() -> str:
    """Return a random word from multiple options."""
    try:
        words: list[str] = get_word_list()
    except ValueError as exc:
        raise RuntimeError("Unable to retrieve word list.") from exc
    
    secret_word = words[randint(0, len(words) - 1)]
    if isinstance(secret_word, str) and len(secret_word) > 0:
        return secret_word
    raise RuntimeError("Unable to return secret word.")


@dataclass
class GameState:
    """Manage state for the hangman game."""
    player_name: str = ''
    word: str = ''
    current_guess: str = ''
    guesses: set[str] = field(default_factory=set)
    remaining_letters: set[str] = field(default_factory=set)
    puzzle: Puzzle = field(default_factory=list)
    image_idx: int = 0
    is_active: bool = False
    
    def initialize_game_state(self) -> None:
        """Post-instantiation initialization."""
        self.remaining_letters = set(self.word)
        self.puzzle = [PuzzleLetter(char, False) for char in self.word]
        self.is_active = True
    
    def update_state_on_guess(self) -> None:
        """Update the game state based on the current guess."""
        try:
            self.remaining_letters.remove(self.current_guess)
            self.update_puzzle()
        except KeyError:
            self.image_idx += 1  # Not in word
    
    def update_puzzle(self) -> None:
        """Update puzzle with correctly guessed letters."""
        self.puzzle = [
            PuzzleLetter(char, val or (char == self.current_guess))
            for char, val in self.puzzle
        ]
    
    def is_game_won(self) -> bool:
        """Check if the player has won the game."""
        return len(self.remaining_letters) == 0
    
    def is_game_lost(self) -> bool:
        """Check if the player has lost the game."""
        return self.image_idx >= len(get_hangman_images()) - 1
    
    def is_game_over(self) -> bool:
        """Check if the game is over (won or lost)."""
        return self.is_game_won() or self.is_game_lost()
    
    def get_display_word(self) -> str:
        """Get the current state of the word with guessed letters revealed."""
        return ' '.join([char if val else '_' for char, val in self.puzzle])
    
    def reset_game(self) -> None:
        """Reset the game state for a new game."""
        self.word = ''
        self.current_guess = ''
        self.guesses = set()
        self.remaining_letters = set()
        self.puzzle = []
        self.image_idx = 0
        self.is_active = False


def _start_hangman_game(player_name: str, session_id: str = "default") -> Dict[str, Any]:
    """
    Start a new hangman game.
    
    Args:
        player_name: The name of the player
        session_id: Optional session identifier for multiple concurrent games
    
    Returns:
        Dict containing game status and initial state
    """
    try:
        # Create or reset game state
        if session_id not in game_sessions:
            game_sessions[session_id] = GameState()
        
        game_state = game_sessions[session_id]
        game_state.reset_game()
        game_state.player_name = player_name
        game_state.word = get_secret_word()
        game_state.initialize_game_state()
        
        return {
            "status": "success",
            "message": f"New game started for {player_name}!",
            "word_length": len(game_state.word),
            "display_word": game_state.get_display_word(),
            "hangman_image": get_hangman_images()[0],
            "guesses_remaining": len(get_hangman_images()) - 1,
            "session_id": session_id
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to start game: {str(e)}"
        }


@mcp.tool()
def start_hangman_game(player_name: str, session_id: str = "default") -> Dict[str, Any]:
    """Start a new hangman game."""
    return _start_hangman_game(player_name, session_id)


def _make_guess(letter: str, session_id: str = "default") -> Dict[str, Any]:
    """
    Make a guess in the hangman game.
    
    Args:
        letter: The letter to guess (single character)
        session_id: The session identifier for the game
    
    Returns:
        Dict containing the result of the guess and current game state
    """
    if session_id not in game_sessions:
        return {
            "status": "error",
            "message": "No active game found. Start a new game first."
        }
    
    game_state = game_sessions[session_id]
    
    if not game_state.is_active:
        return {
            "status": "error",
            "message": "No active game. Start a new game first."
        }
    
    if game_state.is_game_over():
        return {
            "status": "error",
            "message": "Game is already over. Start a new game."
        }
    
    # Validate input
    letter = letter.upper().strip()
    if len(letter) != 1 or not letter.isalpha():
        return {
            "status": "error",
            "message": "Please provide exactly one letter."
        }
    
    if letter in game_state.guesses:
        return {
            "status": "error",
            "message": f"You've already guessed '{letter}'. Try a different letter."
        }
    
    # Process the guess
    game_state.current_guess = letter
    game_state.guesses.add(letter)
    is_correct = letter in game_state.word
    game_state.update_state_on_guess()
    
    # Prepare response
    response = {
        "status": "success",
        "letter": letter,
        "correct": is_correct,
        "display_word": game_state.get_display_word(),
        "hangman_image": get_hangman_images()[game_state.image_idx],
        "guesses_made": sorted(list(game_state.guesses)),
        "guesses_remaining": len(get_hangman_images()) - 1 - game_state.image_idx
    }
    
    # Check for game over conditions
    if game_state.is_game_won():
        response.update({
            "game_over": True,
            "won": True,
            "message": f"Congratulations {game_state.player_name}! You won! The word was '{game_state.word}'."
        })
        game_state.is_active = False
    elif game_state.is_game_lost():
        response.update({
            "game_over": True,
            "won": False,
            "message": f"Game over {game_state.player_name}! The word was '{game_state.word}'. Better luck next time!"
        })
        game_state.is_active = False
    else:
        response["game_over"] = False
        if is_correct:
            response["message"] = f"Good guess! '{letter}' is in the word."
        else:
            response["message"] = f"Sorry, '{letter}' is not in the word."
    
    return response


@mcp.tool()
def make_guess(letter: str, session_id: str = "default") -> Dict[str, Any]:
    """Make a guess in the hangman game."""
    return _make_guess(letter, session_id)


def _get_game_status(session_id: str = "default") -> Dict[str, Any]:
    """
    Get the current status of the hangman game.
    
    Args:
        session_id: The session identifier for the game
    
    Returns:
        Dict containing current game state and status
    """
    if session_id not in game_sessions:
        return {
            "status": "no_game",
            "message": "No game session found. Start a new game first."
        }
    
    game_state = game_sessions[session_id]
    
    if not game_state.is_active and not game_state.is_game_over():
        return {
            "status": "no_active_game",
            "message": "No active game. Start a new game first."
        }
    
    return {
        "status": "active" if game_state.is_active else "finished",
        "player_name": game_state.player_name,
        "word_length": len(game_state.word),
        "display_word": game_state.get_display_word(),
        "hangman_image": get_hangman_images()[game_state.image_idx],
        "guesses_made": sorted(list(game_state.guesses)),
        "guesses_remaining": len(get_hangman_images()) - 1 - game_state.image_idx,
        "game_over": game_state.is_game_over(),
        "won": game_state.is_game_won() if game_state.is_game_over() else None,
        "session_id": session_id
    }


@mcp.tool()
def get_game_status(session_id: str = "default") -> Dict[str, Any]:
    """Get the current status of the hangman game."""
    return _get_game_status(session_id)


def _list_active_sessions() -> Dict[str, Any]:
    """
    List all active hangman game sessions.
    
    Returns:
        Dict containing information about all active sessions
    """
    sessions = []
    for session_id, game_state in game_sessions.items():
        sessions.append({
            "session_id": session_id,
            "player_name": game_state.player_name,
            "active": game_state.is_active,
            "word_length": len(game_state.word) if game_state.word else 0,
            "guesses_made": len(game_state.guesses),
            "game_over": game_state.is_game_over()
        })
    
    return {
        "status": "success",
        "sessions": sessions,
        "total_sessions": len(sessions)
    }


@mcp.tool()
def list_active_sessions() -> Dict[str, Any]:
    """List all active hangman game sessions."""
    return _list_active_sessions()


def _end_game(session_id: str = "default") -> Dict[str, Any]:
    """
    End the current hangman game session.
    
    Args:
        session_id: The session identifier for the game to end
    
    Returns:
        Dict containing confirmation of game termination
    """
    if session_id not in game_sessions:
        return {
            "status": "error",
            "message": "No game session found."
        }
    
    game_state = game_sessions[session_id]
    word = game_state.word
    player_name = game_state.player_name
    
    # Clean up the session
    del game_sessions[session_id]
    
    return {
        "status": "success",
        "message": f"Game ended for {player_name}. The word was '{word}'. Thanks for playing!"
    }


@mcp.tool()
def end_game(session_id: str = "default") -> Dict[str, Any]:
    """End the current hangman game session."""
    return _end_game(session_id)


if __name__ == "__main__":
    # Check Python version
    if sys.version_info < (3, 9):
        print("Hangman MCP Server requires Python 3.9 or later.")
        print("Please update your Python version.")
        sys.exit(1)
    
    # Run the MCP server
    mcp.run()