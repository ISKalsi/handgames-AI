import cv2
from handgames import cricket


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    match = cricket.Match(is_batting_first=True, video_capture=cap)
    for didPlayBall in match.start_match():
        if didPlayBall:
            print(match.current_innings.last_move)
    cap.release()
    