import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
AI_AGENT_MAPPER = {'Minimax': 'Minimax', 'AlphaBeta': 'MinimaxPruning', 'MCTS': 'MonteCarlo'}

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
                {'label': 'Monte Carlo Tree Search', 'value': 'MCTS'},
            ],
            placeholder="Select AI type for Player 1",
        )
    ], style={'display': 'none'}),
    html.Div(id='start-1', children=[
        dcc.Dropdown(
            id='ai-start-1',
            options=[
                {'label': 'AI', 'value': 1},
                {'label': 'Human', 'value': 0},
                {'label': 'Random', 'value': -1},
            ],
            placeholder="Select who is playing first - black pieces",
        )
    ], style={'display': 'none'}),
    html.Div(id='ai-selection-2', children=[
        dcc.Dropdown(
            id='ai-type-dropdown-2',
            options=[
                {'label': 'Minimax', 'value': 'Minimax'},
                {'label': 'Minimax Alpha-Beta Cut', 'value': 'AlphaBeta'},
                {'label': 'Monte Carlo Tree Search', 'value': 'MCTS'},
            ],
            placeholder="Select AI type for Player 2 (if applicable)",
        )
    ], style={'display': 'none'}),
    html.Div(id='start-2', children=[
        dcc.Dropdown(
            id='ai-start-2',
            options=[
                {'label': 'Algorithm1', 'value': 1},
                {'label': 'Algorithm2', 'value': 2},
                {'label': 'Random', 'value': 0},
            ],
            placeholder="Select who is playing first - black pieces",
        )
    ], style={'display': 'none'}),
    html.Button('Launch Game', id='launch-game-button', n_clicks=0),
])


@app.callback(
    [Output('ai-selection-1', 'style'),
     Output('ai-selection-2', 'style'),
     Output('start-2', 'style'),
     Output('start-1', 'style')],
    [Input('game-mode-dropdown', 'value')]
)
def update_ai_selection(game_mode):
    if game_mode == 'HvAI':
        return [{'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}]
    elif game_mode == 'AIvAI':
        return [{'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'none'}]
    return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]


@app.callback(
    Output('launch-game-button', 'n_clicks'),  # Dummy output
    [Input('launch-game-button', 'n_clicks')],
    [State('game-mode-dropdown', 'value'),
     State('ai-type-dropdown-1', 'value'),
     State('ai-type-dropdown-2', 'value'),
     State('ai-start-2', 'value'),
     State('ai-start-1', 'value')]
)
def launch_game(n_clicks, game_mode, ai_type_1, ai_type_2, ai_start_2, ai_start_1):
    if n_clicks > 0:
        if game_mode == 'HvH':
            v = os.system('python neutreeko.py')
            if v != 0:
                os.system('python3 neutreeko.py')
        elif game_mode == 'HvAI':
            ai_agent = AI_AGENT_MAPPER[ai_type_1]
            if ai_agent is not None:
                cmd = f'python3 neutreeko_ai.py -m {ai_agent}'
                if ai_start_1 != -1:
                    cmd += f' -s {ai_start_1}'
                print(cmd)
                v = os.system(cmd)
                if v != 0:
                    cmd = cmd.replace('python3', 'python')
                    os.system(cmd)
            else:
                raise NotImplementedError
        else:
            ai_agent1, ai_agent2 = AI_AGENT_MAPPER[ai_type_1], AI_AGENT_MAPPER[ai_type_2]
            if ai_agent1 is not None and ai_agent2 is not None:
                cmd = f'python3 neutreeko_ai_vs_ai.py -a1 {ai_agent1} -a2 {ai_agent2}'
                if ai_start_2 != 0:
                    cmd += f' -i {ai_start_2}'
                v = os.system(cmd)
                if v != 0:
                    cmd = cmd.replace('python3', 'python')
                    os.system(cmd)
            else:
                raise NotImplementedError
    return 0


if __name__ == '__main__':
    app.run_server(debug=True)
