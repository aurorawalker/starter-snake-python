import os
import random

import cherrypy

import global_variables
import strategy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "aurorawalker",
            "color": "#736CCB",
            "head": "pixel",
            "tail": "pixel",
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        """
        Treat this as game initialization - should only set global_variables
        here - could be dangerous elsewhere! Don't want to confuse myself.
        """
        data = cherrypy.request.json
        print(f"~~  START NEW GAME ~~~{data['game']['id']}")
        # maximum x and y coordinates are one less than the size (zero index)
        global_variables.BOARD_MAXIMUM_X = data["board"]["width"] - 1
        global_variables.BOARD_MAXIMUM_Y = data["board"]["height"] - 1

        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json

        # Data structure holds head, body, then tail
        body = data["you"]["body"]
        print(f"Data in move is: {data}")

        # Choose a random direction to move in
        possible_moves = ["up", "down", "left", "right"]

        for _ in range(10):
            # Max out at 10 tries to avoid infinite loops. :P
            move = random.choice(possible_moves)
            safe = strategy.validate_move(body, move)
            if safe:
                break

        print(f"FINAL MOVE: {move}")

        return {"move": move, "shout": "Urrah!"}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json
        print("~~~~ END GAME ~~~~")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update({"server.socket_port": int(os.environ.get("PORT", "8080"))})
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
