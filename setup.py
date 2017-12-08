# this could be used to create an executable for the game using cx_Freeze

import sys
import cx_Freeze

executables = [cx_Freeze.Executable("car_game.py")]

cx_Freeze.setup(name = "Fast and Furious - Winter is Coming",
                 options = {"build_exe": {"packages":["pygame",
                                                      "sys",
                                                      "random",
                                                      "time",
                                                      "pygame.locals"],
                                          "include_files":["background.png",
                                                           "carOpponent02.png",
                                                           "start_menu.jpg",
                                                           "carOpponent03.png",
                                                           "carPlayer.png",
                                                           "9ma.png",
                                                           "boom.png",
                                                           "star.png",
                                                           "song.wav",
                                                           "crash.wav",
                                                           "gotitem.wav",
                                                           "obstacle.wav",
                                                           "Give_Away.wav",
                                                           "win.png"]}},
                executables = executables
                )
