    def restart_game(self):
        """
        Restart the game from the beginning.

        This method clears all game state and re-initializes 
        the entire game as if it were started fresh.
        """
        # Clear the screen and all turtles
        self.screen.clear()
        # Re-initialize the game controller
        self.__init__()