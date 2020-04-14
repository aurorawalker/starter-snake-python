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
    def index(self):
        # If you open your snake URL in a browser you should see this message.
        return "Your Battlesnake is alive!"

    @cherrypy.expose
    def ping(self):
        # The Battlesnake engine calls this function to make sure your snake is working.
        return "pong"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def start(self):
        """
        Treat this as game initialization - should only set global_variables
        here - could be dangerous elsewhere! Don't want to confuse myself.
        """
        data = cherrypy.request.json
        print(f"~~  START NEW GAME ~~~{data['game']['id']}")
        global_variables.BOARD_MAXIMUM_X = data["board"]["width"]
        global_variables.BOARD_MAXIMUM_Y = data["board"]["height"]

        return {"color": "#736CCB", "headType": "pixel", "tailType": "pixel"}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json

        # Data structure holds head, body, then tail
        # current_head = data["you"]["body"][0]
        # print(f"Data in move is: {data}")
        #
        # # Choose a random direction to move in
        # possible_moves = ["up", "down", "left", "right"]
        # move = random.choice(possible_moves)
        #
        # while strategy.avoid_walls(current_head, move) is not True:
        #     move = random.choice(possible_moves)
        #
        # print(f"MOVE: {move}")

        ## Sanity check - which way is left/right/up/down?!?
        if data["turn"] == 0 or data["turn"] == 1:
            move = "up"

        elif data["turn"] == 2 or data["turn"] == 3:
            move = "left"

        elif data["turn"] == 4 or data["turn"] == 5:
            move = "down"

        elif data["turn"] == 6 or data["turn"] == 7:
            move = "right"
        else:
            move = "up"

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
