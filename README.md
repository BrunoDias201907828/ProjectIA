#  Neutreeko App with Adversarial Search Algorithms 

## How to Run the App

This project builds an application to play the Neutreeko game.

It supports 3 Modes: Human vs Human, Human vs AI and AI vs AI.

Most effort was put into the AI algorithms. There are 4 different AI levels, from easy to extreme. They all use Minimax
with Alpha-Beta Cuts, but they have different depths or heuristics.

Additionally, there is an option to decide who starts the game and a way to restart the game with same configs.

### Launch Application
To launch the application, you need to have Python installed. You will also need 3rd party libraries, although we do 
not have a requirement file at the moment. Then, you can run the following command in the terminal, from the ProjectAI 
folder:

```python options_menu.py```.

An url will appear in the terminal for a dashboard. Open it in a browser (you can click or ctrl + click the link).

On the dashboard, you will choose the game mode you want to play, the difficulty of the AI algorithms and who starts to
play. Then, you can click the "Launch" button to start the game.

### Common to all game modes
Human plays show the possible moves with green dots. 

Message in the bottom part displaying if an AI is thinking. 

On the middle top of the screen, there is a message displaying the current player (black or white).

Once you reach a terminal state, a message will appear to show the winner or draw.

To restart the game click on the key "r".

### Human vs Human

Here you can play against another human. The game will only end when a player wins or there is a draw.

### Human vs AI

Here you can play against an AI. Once you click on the board, the game starts. If its the AI's turn, you will see the
message at the bottom of the screen informing you that the AI is thinking. Once that message disappears, it is your turn.

### AI vs AI

Here you can watch two AI algorithms playing against each other. A play happens when you click anywhere in the 
application window. If you click multiple times, it stacks and the plays can happen almost at the same time.

## Code Structure

The options_menu.py is the main script to run the application. It uses the dash library to create the dashboard.

Additionally, there are 3 different packages:
- algorithms: here you can find the code regarding ai here. Both the algorithms and the heuristics codes are here.
- compare_algorithms_and_heuristics: here you can find the code to compare the algorithms and heuristics. It is used to
  generate results for the report.
- app: here you can find the code to create the game window. The game is created using the arcade library.




