# Final-Year-Project

> FrozenLake:
- FrozenLake_graph.py (plotting the test curve)
- FrozenLake_v0.py (qlearning script)
- state_action (dictionary of action-values; save and load using pickles)

> FlappyBird > Qlearning:
- flappy_plot.py (plotting the flight path of agent in game)
- flappy_test.py (testing the policy)
- flappy_visual.py (saving state representation of agent in game for plot)
- flappy.py (qlearning script)
- q_val_v3 (dictionary of action-values; save and load using pickles)

> FlappyBird > SemiGradient:
- flappy_vfunc_test.py (testing the policy)
- flappy_vfunc_visual.py (saving state representation of agent in game for plot)
- flappy_vfunc5_5.py (semi-gradient script)
- vfunc_v5_12_model (neural network model of value function)

> TicTacToe:
- create_image.py (plot lose/draw/win ratio)
- draw_ttt.py (draw tictactoe grid and moves and create gif or collage)

> TicTacToe > Qlearning:
- OriginalPolicy_p1_v2 (dictionary of action-values of starting player X; save and load using pickles)
- OriginalPolicy_p2_v2 (dictionary of action-values of second player O; save and load using pickles)
- state_converge_O (dictionary of opening state values as training progresses)
- tictactoe.py (qlearning script)
- ttt_plot.py (plotting opening position values)

> TicTacToe > SemiGradient > RandomPlayer:
- tictactoe_NN_vfunc6.py (semi-gradient script)
- Vmodelp1_6_v7 (neural network model of value function of starting player X when trained against random player)

> TicTacToe > SemiGradient > Minimax > epsilonMinimaxModel:
- Epo_Vmodel1_v10 (neural network model of value function of starting player X when trained against epsilon=0.3 minimax player)

> TicTacToe > SemiGradient > Minimax > MinimaxModel: 
- po_Vmodel1_round5000 (neural network model after 5,000 rounds of training of value function of starting player X when trained against minimax player)
- po_Vmodel1_round6000 (neural network model after 6,000 rounds of training of value function of starting player X when trained against minimax player)
- po_Vmodel1_v9 (final neural network model of value function of starting player X when trained against minimax player)

> TicTacToe > SemiGradient > Minimax > tictactoe: 
- ab_bot_vs_ab_bot.py (test games)	
- ab_bot_vs_randombot.py	 (test games)	
- ab_bot_vs_vfuncbot.py (test games)		
- train_vfuncbot.py (semi-gradient script)	
- train_vfuncbot_1hot.py (semi-gradient with one hot encoding script)
- train_vfuncbot_rotate.py (semi-gradient with board rotation script)
- vfuncbot_vs_human.py (test games)
- vfuncbot_vs_randombot.py (test games)

> TicTacToe > SemiGradient > Minimax > tictactoe > ttt: 
(Scripts needed to run the games and training)
