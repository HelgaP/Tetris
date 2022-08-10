# 1. Generate object and show it on the screen anywhere: DONE
# 1.1 Consider thick frame of the playgound (its size and increase size of playground accordingly): DONE
# 2. Change the position of the object on the screen with every second: DONE
# 3. Create a new object randomly out of prepared options.
# Until the object hits the ground, don't create any new objects.
# As soon as a new object hits the ground, update stack and pick a new object: DONE
# 4. Write a method to present an object, not through initialization: DONE
# 5. Write a func to represent stack objects on the screen: DONE
# 6. Write a func to delete lines which are completely filled. Pick just one bottom line to check, if it's filled in, check for the next line, and so on and delete them all: IN PROGRESS
# 7. Check when game is over: DONE
# 8. Incorporate matrix (a two-dimensional array which will represent what cells are taken and what are free. Update it every time when a new object hits the ground: DONE
# 10. Probably Stack object will be replaced fully by Matrix object: YES, DELETED
# 11. To test deleteLine function in a separate file because it works super weird: DONE
# 12. To understand when objects appear and more importantly disappear from the screen: DONE
# 13. Incorporate user input to move the blocks: DONE
# 14. For every object at every point in the game there should be right, left and down limitations (where a user can move it) based on matrix values: CANCELLED
# 15. Create a resume button: DONE
# 16. When paused, brick should be visible and stay on the same Y coordinate: DONE
# 16.1 Write a property decorator: DONE
# 17. Rewrite present, delete funcs and create all necessaey figures: DONE
# 17.1 Fix present func: DONE
# 17.2 Figure out how to check if turn is pissible:DONE
# 17.3 Add coords for clockwise and counterclockwise turns: TO DO
# 18. Rewrite checking for collision with matrix and walls: DONE
# 19. Write a func to cancel the game while on pause: DONE
# 20. Write a func that only half a figure goes down @ the start of the game: CANCELLED
# 21. When there are muliple lines to be deleted, they should be deleted at once, not when a next reachBottom method is triggered: DONE
# 22. Keep the table grid when lines are deleted: DONE


# 17.3 Write coords for all states of left and right side Twist: DONE
# 17.3.1 Continue checking createNewObject method: DONE
# 17.4 Write a separate method in Twist class how to check if turn is allowed: DONE OR CANCELLED
# 17.4.1 Check and correct all other funcs and methods which use Twist to make sure everything worls with the changes (like createNewObject func, etc): DONE
# 17.5 Add all necessary coordinates for all positions of Log: DONE
# 17.6 Write a separate method to check if Log turn is allowed: DONE

# Adapt new crossSMTH methods for Log object: seemingly done
# Проверить, почему объект исчезает при перемещении, исправить: DONE
## maybe should present new object first and then delete old one?
# Проверить crossedLeftLimit method для правого твиста: looks ok to me
# Сделать белую огранку фигур толстые по краям и без полос или с тонкими полосами внутри: DONE
# проверить логику стека, почему-то исчезает больше, чем нужно: DONE
# add sound effects: DONE
# check that when new objects are created, they don't hit current stack of piles (matrix): DONE
# add explicit comments to understand game flow later: DONE
# upload on github
# make a web-based version after completing Django course

# maybe add score and levels later (when put on server) to make a game more interesting for users

