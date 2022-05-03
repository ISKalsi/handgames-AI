import cv2
from handgames import cricket
import PySimpleGUI as sg


KEY_NUM_PLAYER = '-NUM-PLAYER-'
KEY_NUM_CPU = '-NUM-CPU-'
KEY_INNINGS = '-INNINGS-'
KEY_RUNS = '-RUNS-'
KEY_TARGET = '-TARGET-'
KEY_MSG = '-MSG-'
KEY_LEFT_MSG = '-LEFT-MSG-'
KEY_RIGHT_MSG = '-RIGHT-MSG-'

COLOR_GREEN = "#3BD955"
COLOR_BLUE = "#87A9F3"

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.


def score_board(key):
    return sg.Column(layout=[[sg.Text('0',key=key, font="def 50")]],
                     size=(60, 150))


def player_msg(key):
    return sg.Text('', key=key, font="def 14", text_color=COLOR_BLUE)


layout = [[sg.Column(layout=[[sg.Text('Player')],
                             [player_msg(KEY_LEFT_MSG)],
                             [score_board(KEY_NUM_PLAYER)]],
                     vertical_alignment="top",
                     element_justification="center"),
           sg.Column(layout=[[sg.Text('Inn.: 1', key=KEY_INNINGS)],
                             [sg.Text("START", key=KEY_MSG, text_color=COLOR_GREEN)],
                             [sg.Text("Runs\n0", key=KEY_RUNS)],
                             [sg.Text("", key=KEY_TARGET, text_color=COLOR_GREEN)]],
                     vertical_alignment="top",
                     element_justification="center"),
           sg.Column(layout=[[sg.Text('CPU')],
                             [player_msg(KEY_RIGHT_MSG)],
                             [score_board(KEY_NUM_CPU)]],
                     vertical_alignment="top",
                     element_justification="center")],
          [sg.Button('Exit')]]


def update_batting_and_bowling(match, window):
    if match.current_innings.batter.name == "Player":
        batterKey, bowlerKey = KEY_LEFT_MSG, KEY_RIGHT_MSG
    else:
        batterKey, bowlerKey = KEY_RIGHT_MSG, KEY_LEFT_MSG
        
    window[batterKey].update("BATTING")
    window[bowlerKey].update("BOWLING")

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    match = cricket.Match(is_batting_first=True, video_capture=cap)
    window = sg.Window('Hand Cricket', layout,
                       font="default 24",
                       text_justification="center", 
                       element_justification="right",
                       finalize=True)
        
    update_batting_and_bowling(match, window)
    
    for didPlayBall in match.start_match():
        if didPlayBall:
            print(match.current_innings.last_move)

        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        updateWindow = True
        if match.current_innings.last_move is not None:
            if match.is_second_innings:
                ball, bat = match.current_innings.last_move
            else:
                bat, ball = match.current_innings.last_move
            window[KEY_MSG].update('')
            window[KEY_RUNS].update('Runs\n' + str(match.current_innings.runs))
        elif match.is_second_innings:
            window[KEY_INNINGS].update('Inn.: 2')
            update_batting_and_bowling(match, window)
            bat, ball = match.previous_innings.last_move
            window[KEY_MSG].update('OUT!', text_color="red")
            window[KEY_TARGET].update(
                'Target\n'+str(match.previous_innings.runs))
        else:
            updateWindow = False

        if updateWindow:
            window[KEY_NUM_PLAYER].update(str(bat))
            window[KEY_NUM_CPU].update(str(ball))

    window[KEY_MSG].update("FINISH!")
    if match.winner.name == "Player":
        winnerKey = KEY_NUM_PLAYER
        loserKey = KEY_NUM_CPU
    else:
        winnerKey = KEY_NUM_CPU
        loserKey = KEY_NUM_PLAYER

    window[winnerKey].update("W\nI\nN", font="def 28", text_color=COLOR_GREEN)
    window[loserKey].update("")

    cap.release()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
            break

    window.close()
