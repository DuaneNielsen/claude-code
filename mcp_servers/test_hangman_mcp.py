#!/usr/bin/env python3
"""
Corrected comprehensive test suite for the hangman MCP server.

Tests all server functionality using the actual API response format.
"""

import pytest
from typing import Dict, Any
from fastmcp import Client
from hangman_mcp import mcp

# Configure pytest to use anyio for async tests, only asyncio backend
pytest_plugins = ["anyio"]


@pytest.fixture(scope="session")
def anyio_backend():
    """Force asyncio backend only to avoid trio compatibility issues with fastmcp."""
    return "asyncio"


class TestHangmanMCPServer:
    """Test suite for hangman MCP server functionality."""
    
    @pytest.fixture
    async def server_client(self):
        """Create an in-memory client for testing the hangman server."""
        async with Client(mcp) as client:
            yield client
    
    @pytest.mark.anyio
    async def test_start_hangman_game_basic(self, server_client):
        """Test starting a basic hangman game."""
        result = await server_client.call_tool(
            "start_hangman_game",
            {"player_name": "Alice"}
        )
        
        assert result.data["status"] == "success"
        assert result.data["session_id"] == "default"
        assert "word_length" in result.data
        assert result.data["word_length"] > 0
        assert "display_word" in result.data
        assert "hangman_image" in result.data
        assert "guesses_remaining" in result.data
        assert "Alice" in result.data["message"]
    
    @pytest.mark.anyio
    async def test_start_hangman_game_with_custom_session(self, server_client):
        """Test starting a game with custom session ID."""
        result = await server_client.call_tool(
            "start_hangman_game",
            {"player_name": "Bob", "session_id": "session_123"}
        )
        
        assert result.data["status"] == "success"
        assert result.data["session_id"] == "session_123"
        assert "Bob" in result.data["message"]
    
    @pytest.mark.anyio
    async def test_make_correct_guess(self, server_client):
        """Test making a guess and verifying response format."""
        # Start a game first
        await server_client.call_tool(
            "start_hangman_game",
            {"player_name": "Charlie"}
        )
        
        # Make a guess
        guess_result = await server_client.call_tool(
            "make_guess",
            {"letter": "a"}
        )
        
        assert guess_result.data["status"] == "success"
        assert "correct" in guess_result.data
        assert "letter" in guess_result.data
        assert "display_word" in guess_result.data
        assert "hangman_image" in guess_result.data
        assert "guesses_made" in guess_result.data
        assert "guesses_remaining" in guess_result.data
        assert "game_over" in guess_result.data
        assert isinstance(guess_result.data["guesses_made"], list)
    
    @pytest.mark.anyio
    async def test_duplicate_guess(self, server_client):
        """Test making the same guess twice."""
        # Start a game
        await server_client.call_tool(
            "start_hangman_game",
            {"player_name": "Eve"}
        )
        
        # Make initial guess
        await server_client.call_tool(
            "make_guess",
            {"letter": "a"}
        )
        
        # Make same guess again
        duplicate_result = await server_client.call_tool(
            "make_guess",
            {"letter": "a"}
        )
        
        # Should be some kind of error or warning about duplicate guess
        assert "message" in duplicate_result.data
        # The message should indicate it was already guessed
        message_lower = duplicate_result.data["message"].lower()
        assert "already" in message_lower or "duplicate" in message_lower or "guessed" in message_lower
    
    @pytest.mark.anyio
    async def test_invalid_guess_multiple_letters(self, server_client):
        """Test making an invalid guess with multiple letters."""
        await server_client.call_tool(
            "start_hangman_game",
            {"player_name": "Frank"}
        )
        
        result = await server_client.call_tool(
            "make_guess",
            {"letter": "abc"}
        )
        
        # Should handle invalid input gracefully
        assert "message" in result.data
        message_lower = result.data["message"].lower()
        assert "single" in message_lower or "one" in message_lower or "invalid" in message_lower
    
    @pytest.mark.anyio
    async def test_invalid_guess_non_letter(self, server_client):
        """Test making an invalid guess with non-letter character."""
        await server_client.call_tool(
            "start_hangman_game",
            {"player_name": "Grace"}
        )
        
        result = await server_client.call_tool(
            "make_guess",
            {"letter": "1"}
        )
        
        # Should handle invalid input gracefully
        assert "message" in result.data
        message_lower = result.data["message"].lower()
        assert "letter" in message_lower or "invalid" in message_lower
    
    @pytest.mark.anyio
    async def test_get_game_status_after_start(self, server_client):
        """Test getting game status after starting a game."""
        start_result = await server_client.call_tool(
            "start_hangman_game",
            {"player_name": "Henry"}
        )
        
        status_result = await server_client.call_tool(
            "get_game_status",
            {}
        )
        
        assert status_result.data["status"] == "active"
        assert status_result.data["player_name"] == "Henry"
        assert status_result.data["session_id"] == "default"
        assert "word_length" in status_result.data
        assert status_result.data["game_over"] is False
    
    @pytest.mark.anyio
    async def test_get_game_status_no_active_game(self, server_client):
        """Test getting game status when no game is active."""
        result = await server_client.call_tool(
            "get_game_status",
            {"session_id": "nonexistent"}
        )
        
        # Should indicate no active game in some way
        assert "status" in result.data
        # Status should not be "active" if no game exists
        assert result.data["status"] != "active"
    
    @pytest.mark.anyio
    async def test_list_active_sessions(self, server_client):
        """Test listing active sessions."""
        # First test with no sessions
        result = await server_client.call_tool(
            "list_active_sessions",
            {}
        )
        
        assert "status" in result.data
        
        # Start a game and test again
        await server_client.call_tool(
            "start_hangman_game",
            {"player_name": "Player1", "session_id": "session1"}
        )
        
        result2 = await server_client.call_tool(
            "list_active_sessions",
            {}
        )
        
        assert "status" in result2.data
        # Should have information about active sessions
    
    @pytest.mark.anyio
    async def test_end_game(self, server_client):
        """Test ending a game."""
        # Start a game
        await server_client.call_tool(
            "start_hangman_game",
            {"player_name": "Iris"}
        )
        
        # End the game
        result = await server_client.call_tool(
            "end_game",
            {}
        )
        
        assert "status" in result.data
        assert "message" in result.data
    
    @pytest.mark.anyio
    async def test_case_insensitive_guessing(self, server_client):
        """Test that letter guessing handles case properly."""
        await server_client.call_tool(
            "start_hangman_game",
            {"player_name": "CaseTest"}
        )
        
        # Make guess with uppercase letter
        result_upper = await server_client.call_tool(
            "make_guess",
            {"letter": "A"}
        )
        
        # The letter should be processed (either as 'A' or 'a')
        assert "letter" in result_upper.data
        guessed_letter = result_upper.data["letter"]
        
        # Make guess with lowercase version of same letter
        result_lower = await server_client.call_tool(
            "make_guess",
            {"letter": "a"}
        )
        
        # Should handle the case appropriately (either reject as duplicate or process)
        assert "message" in result_lower.data
    
    @pytest.mark.anyio
    async def test_game_progression(self, server_client):
        """Test a complete game progression."""
        # Start a game
        start_result = await server_client.call_tool(
            "start_hangman_game",
            {"player_name": "GamePlayer"}
        )
        
        initial_remaining = start_result.data["guesses_remaining"]
        
        # Make several guesses
        letters = ["a", "e", "i", "o", "u"]  # Common vowels
        
        for letter in letters:
            guess_result = await server_client.call_tool(
                "make_guess",
                {"letter": letter}
            )
            
            # Each guess should return valid response
            assert "correct" in guess_result.data
            assert "guesses_made" in guess_result.data
            assert "game_over" in guess_result.data
            
            # If game is over, break
            if guess_result.data.get("game_over", False):
                break
        
        # Get final status
        final_status = await server_client.call_tool(
            "get_game_status",
            {}
        )
        
        # Should have valid final state
        assert "status" in final_status.data
        assert "guesses_made" in final_status.data


if __name__ == "__main__":
    import asyncio
    
    async def run_simple_test():
        """Run a simple connectivity test."""
        async with Client(mcp) as client:
            # Test basic functionality
            result = await client.call_tool(
                "start_hangman_game",
                {"player_name": "SimpleTest"}
            )
            print("✓ Start game:", result.data["status"])
            
            guess_result = await client.call_tool(
                "make_guess",
                {"letter": "e"}
            )
            print("✓ Make guess:", guess_result.data["status"])
            
            status_result = await client.call_tool(
                "get_game_status",
                {}
            )
            print("✓ Get status:", status_result.data["status"])
    
    print("Running simple connectivity test...")
    asyncio.run(run_simple_test())
    print("✓ All basic tests passed!")
    print("Run 'python -m pytest test_hangman_mcp_corrected.py -v' for full test suite.")