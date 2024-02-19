import os

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from neutreeko import Neutreeko
from neutreeko_ai import NeutreekoAI
import multiprocessing

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Game Mode and AI Selection"),
    dcc.Dropdown(
        id='game-mode-dropdown',
        options=[
            {'label': 'Human vs Human', 'value': 'HvH'},
            {'label': 'Human vs AI', 'value': 'HvAI'},
            {'label': 'AI vs AI', 'value': 'AIvAI'},
        ],
        placeholder="Select a game mode",
    ),
    html.Div(id='ai-selection-1', children=[
        dcc.Dropdown(
            id='ai-type-dropdown-1',
            options=[
                {'label': 'Minimax', 'value': 'Minimax'},
                {'label': 'Minimax Alpha-Beta Cut', 'value': 'AlphaBeta'},
                {'label': 'MCTS', 'value': 'MCTS'},
            ],
            placeholder="Select AI type for Player 1",
        )
    ], style={'display': 'none'}),
    html.Div(id='ai-selection-2', children=[
        dcc.Dropdown(
            id='ai-type-dropdown-2',
            options=[
                {'label': 'Minimax', 'value': 'Minimax'},
                {'label': 'Minimax Alpha-Beta Cut', 'value': 'AlphaBeta'},
                {'label': 'MCTS', 'value': 'MCTS'},
            ],
            placeholder="Select AI type for Player 2 (if applicable)",
        )
    ], style={'display': 'none'}),
    html.Button('Launch Game', id='launch-game-button', n_clicks=0),
])


@app.callback(
    [Output('ai-selection-1', 'style'),
     Output('ai-selection-2', 'style')],
    [Input('game-mode-dropdown', 'value')]
)
def update_ai_selection(game_mode):
    if game_mode == 'HvAI':
        return [{'display': 'block'}, {'display': 'none'}]
    elif game_mode == 'AIvAI':
        return [{'display': 'block'}, {'display': 'block'}]
    return [{'display': 'none'}, {'display': 'none'}]


@app.callback(
    Output('launch-game-button', 'n_clicks'),  # Dummy output
    [Input('launch-game-button', 'n_clicks')],
    [State('game-mode-dropdown', 'value'),
     State('ai-type-dropdown-1', 'value'),
     State('ai-type-dropdown-2', 'value')]
)
def launch_game(n_clicks, game_mode, ai_type_1, ai_type_2):
    if n_clicks > 0:
        if game_mode == 'HvH':
            os.system('python neutreeko.py')
        elif game_mode == 'HvAI':
            ai_agent = {'Minimax': 'minimax', 'AlphaBeta': 'minimax_pruning', 'MCTS': None}[ai_type_1]
            if ai_agent is not None:
                os.system(f'python neutreeko_ai.py -m {ai_agent}')
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError
    return 0


if __name__ == '__main__':
    app.run_server(debug=True)
