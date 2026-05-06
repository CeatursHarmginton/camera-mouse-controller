#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Camera Mouse Controller
# Author: CeatursHarmginton
# Based on NonMouse by Yuki Takeyama

import cv2
import time
import keyboard
import platform
import numpy as np
import mediapipe as mp
import ctypes
from pynput.mouse import Button, Controller

from nonmouse.args import *
from nonmouse.utils import *
from nonmouse.config import load_config
from nonmouse.overlay import start_overlay, stop_overlay, add_action

mouse = Controller()
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

pf = platform.system()

# Function to check if Caps Lock is ON (Windows)
def is_capslock_on():
    if pf == 'Windows':
        # VK_CAPITAL = 0x14 (Caps Lock key)
        return ctypes.windll.user32.GetKeyState(0x14) & 1
    elif pf == 'Darwin':
        # For macOS, fallback to keyboard check
        return keyboard.is_pressed('caps lock')
    else:
        return True  # Linux: always active

if pf == 'Windows':
    hotkey = 'CapsLock'  # Display name only
elif pf == 'Darwin':
    hotkey = 'CapsLock'
elif pf == 'Linux':
    hotkey = 'XXX'              # hotkeyはLinuxでは無効


def main():
    cap_device, mode, kando, screenRes = tk_arg()
    dis = 0.7                           # くっつける距離の定義
    preX, preY = 0, 0
    nowCli, preCli = 0, 0               # 現在、前回の左クリック状態
    norCli, prrCli = 0, 0               # 現在、前回の右クリック状態
    douCli = 0                          # ダブルクリック状態
    i, k, h = 0, 0, 0
    LiTx, LiTy, list0x, list0y, list1x, list1y, list4x, list4y, list6x, list6y, list8x, list8y, list12x, list12y = [
    ], [], [], [], [], [], [], [], [], [], [], [], [], []   # 移動平均用リスト
    moving_average = [[0] * 3 for _ in range(3)]
    nowUgo = 1
    cap_width = 1280
    cap_height = 720
    start, c_start = float('inf'), float('inf')
    c_text = 0
    
    # Load config for dead zone
    config = load_config()
    dead_zone = config.get('dead_zone', 2)  # pixels
    
    # Advanced gesture state tracking
    gesture_state = {
        'last_click_time': 0,
        'click_cooldown': 0.15,      # 150ms between clicks
        'last_zoom_time': 0,
        'zoom_cooldown': 0.1,
        'last_scroll_time': 0,
        'scroll_cooldown': 0.05,
        'pinch_start_dist': None,
        'is_pinching': False,
        'swipe_velocity': [0, 0],
        'swipe_decay': 0.85,         # Momentum decay
        'last_gesture': None,
        'gesture_hold_frames': 0,
        'required_hold_frames': 3,   # Frames to hold before trigger
    }
    
    # Additional landmark tracking for new gestures
    list5x, list5y = [], []   # Index finger MCP
    list9x, list9y = [], []   # Middle finger MCP
    list17x, list17y = [], [] # Pinky MCP
    list20x, list20y = [], [] # Pinky tip
    
    # Start floating overlay for action history
    start_overlay()
    
    # Webカメラ入力, 設定
    window_name = 'NonMouse'
    cv2.namedWindow(window_name)
    cap = cv2.VideoCapture(cap_device)
    cap.set(cv2.CAP_PROP_FPS, 60)
    cfps = int(cap.get(cv2.CAP_PROP_FPS))
    if cfps < 30:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)
        cfps = int(cap.get(cv2.CAP_PROP_FPS))
    # スムージング量（小さい:カーソルが小刻みに動く 大きい:遅延が大）
    # Increased smoothing for less jitter (original: cfps/10)
    ran = max(int(cfps/3), 3)
    hands = mp_hands.Hands(
        min_detection_confidence=0.8,   # 検出信頼度
        min_tracking_confidence=0.9,    # 追跡信頼度 (increased for stability)
        max_num_hands=1                 # 最大検出数
    )
    # メインループ ###############################################################################
    while cap.isOpened():
        p_s = time.perf_counter()
        success, image = cap.read()
        if not success:
            continue
        if mode == 1:                   # Mouse
            image = cv2.flip(image, 0)  # 上下反転
        elif mode == 2:                 # Touch
            image = cv2.flip(image, 1)  # 左右反転

        # 画像を水平方向に反転し、BGR画像をRGBに変換
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False   # 参照渡しのためにイメージを書き込み不可としてマーク
        results = hands.process(image)  # mediapipeの処理
        image.flags.writeable = True    # 画像に手のアノテーションを描画
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image_height, image_width, _ = image.shape

        if results.multi_hand_landmarks:
            # 手の骨格描画
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if pf == 'Linux':           # Linuxだったら、常に動かす
                can = 1
                c_text = 0
            else:                       # Check Caps Lock state instead of holding Alt
                if is_capslock_on():    # Caps Lock is ON -> tracking active
                    can = 1
                    c_text = 0          # Caps Lock ON - no message
                else:                   # Caps Lock is OFF -> tracking disabled
                    can = 0
                    c_text = 1          # Show "Turn ON CapsLock"
                    # i = 0
            # グローバルホットキーが押されているとき ##################################################
            if can == 1:
                # print(hand_landmarks.landmark[0])
                # preX, preYに現在のマウス位置を代入 1回だけ実行
                if i == 0:
                    preX = hand_landmarks.landmark[8].x
                    preY = hand_landmarks.landmark[8].y
                    i += 1

                # 以下で使うランドマーク座標の移動平均計算
                landmark0 = [calculate_moving_average(hand_landmarks.landmark[0].x, ran, list0x), calculate_moving_average(
                    hand_landmarks.landmark[0].y, ran, list0y)]
                landmark1 = [calculate_moving_average(hand_landmarks.landmark[1].x, ran, list1x), calculate_moving_average(
                    hand_landmarks.landmark[1].y, ran, list1y)]
                landmark4 = [calculate_moving_average(hand_landmarks.landmark[4].x, ran, list4x), calculate_moving_average(
                    hand_landmarks.landmark[4].y, ran, list4y)]
                landmark6 = [calculate_moving_average(hand_landmarks.landmark[6].x, ran, list6x), calculate_moving_average(
                    hand_landmarks.landmark[6].y, ran, list6y)]
                landmark8 = [calculate_moving_average(hand_landmarks.landmark[8].x, ran, list8x), calculate_moving_average(
                    hand_landmarks.landmark[8].y, ran, list8y)]
                landmark12 = [calculate_moving_average(hand_landmarks.landmark[12].x, ran, list12x), calculate_moving_average(
                    hand_landmarks.landmark[12].y, ran, list12y)]
                
                # Additional landmarks for zoom gesture
                landmark5 = [calculate_moving_average(hand_landmarks.landmark[5].x, ran, list5x), calculate_moving_average(
                    hand_landmarks.landmark[5].y, ran, list5y)]
                landmark20 = [calculate_moving_average(hand_landmarks.landmark[20].x, ran, list20x), calculate_moving_average(
                    hand_landmarks.landmark[20].y, ran, list20y)]

                # 指相対座標の基準距離、以後mediapipeから得られた距離をこの値で割る
                absKij = calculate_distance(landmark0, landmark1)
                # 人差し指の先端と中指の先端間のユークリッド距離
                absUgo = calculate_distance(landmark8, landmark12) / absKij
                # 人差し指の第２関節と親指の先端間のユークリッド距離
                absCli = calculate_distance(landmark4, landmark6) / absKij
                # Pinch distance (thumb tip to index tip) for zoom
                absPinch = calculate_distance(landmark4, landmark8) / absKij

                posx, posy = mouse.position
                current_time = time.time()

                # 人差し指の先端をカーソルに対応
                # カメラ座標をマウス移動量に変換
                nowX = calculate_moving_average(
                    hand_landmarks.landmark[8].x, ran, LiTx)
                nowY = calculate_moving_average(
                    hand_landmarks.landmark[8].y, ran, LiTy)

                dx = kando * (nowX - preX) * image_width
                dy = kando * (nowY - preY) * image_height

                if pf == 'Windows' or pf == 'Linux':     # Windows,linuxの場合、マウス移動量に0.5を足して補正
                    dx = dx+0.5
                    dy = dy+0.5
                preX = nowX
                preY = nowY
                
                # Dead zone filter - ignore micro-movements
                if abs(dx) < dead_zone and abs(dy) < dead_zone:
                    dx, dy = 0, 0
                
                # print(dx, dy)
                if posx+dx < 0:  # カーソルがディスプレイから出て戻ってこなくなる問題の防止
                    dx = -posx
                elif posx+dx > screenRes[0]:
                    dx = screenRes[0]-posx
                if posy+dy < 0:
                    dy = -posy
                elif posy+dy > screenRes[1]:
                    dy = screenRes[1]-posy

                # ============ PINCH ZOOM GESTURE ============
                # Two fingers (thumb + index) spread apart or pinch together
                zoom_threshold_close = 0.4   # Fingers close = zoom out
                zoom_threshold_far = 1.2     # Fingers far = zoom in
                
                if absPinch < zoom_threshold_close and current_time - gesture_state['last_zoom_time'] > gesture_state['zoom_cooldown']:
                    # Pinch close = Zoom Out (Ctrl + -)
                    if not gesture_state['is_pinching'] or gesture_state['pinch_start_dist'] is None:
                        gesture_state['pinch_start_dist'] = absPinch
                        gesture_state['is_pinching'] = True
                    elif gesture_state['pinch_start_dist'] - absPinch > 0.1:
                        keyboard.press_and_release('ctrl+-')
                        add_action("Zoom Out")
                        gesture_state['last_zoom_time'] = current_time
                        gesture_state['pinch_start_dist'] = absPinch
                        draw_circle(image, (landmark4[0] + landmark8[0]) / 2 * image_width,
                                   (landmark4[1] + landmark8[1]) / 2 * image_height, 30, (255, 0, 255))
                                   
                elif absPinch > zoom_threshold_far and current_time - gesture_state['last_zoom_time'] > gesture_state['zoom_cooldown']:
                    # Spread = Zoom In (Ctrl + +)
                    if gesture_state['is_pinching'] and gesture_state['pinch_start_dist'] is not None:
                        if absPinch - gesture_state['pinch_start_dist'] > 0.2:
                            keyboard.press_and_release('ctrl+=')
                            add_action("Zoom In")
                            gesture_state['last_zoom_time'] = current_time
                            gesture_state['pinch_start_dist'] = absPinch
                            draw_circle(image, (landmark4[0] + landmark8[0]) / 2 * image_width,
                                       (landmark4[1] + landmark8[1]) / 2 * image_height, 30, (0, 255, 255))
                else:
                    gesture_state['is_pinching'] = False
                    gesture_state['pinch_start_dist'] = None

                # ============ CLICK DETECTION WITH COOLDOWN ============
                # Increased threshold and added cooldown
                click_threshold = 0.65  # Increased from 0.7 for better accuracy
                
                if absCli < click_threshold:
                    nowCli = 1          # nowCli:左クリック状態(1:click  0:non click)
                    draw_circle(image, hand_landmarks.landmark[8].x * image_width,
                                hand_landmarks.landmark[8].y * image_height, 20, (0, 250, 250))
                elif absCli >= click_threshold:
                    nowCli = 0
                    
                if np.abs(dx) > 7 and np.abs(dy) > 7:
                    k = 0                           # 「動いている」ときk=0
                    
                # 右クリック状態 １秒以上クリック状態&&カーソルを動かさない
                # 「動いていない」ときでクリックされたとき
                if nowCli == 1 and np.abs(dx) < 7 and np.abs(dy) < 7:
                    if k == 0:          # k:クリック状態&&カーソルを動かしてない。113, 140行目でk=0にする
                        start = time.perf_counter()
                        k += 1
                    end = time.perf_counter()
                    if end-start > 1.5:
                        norCli = 1
                        draw_circle(image, hand_landmarks.landmark[8].x * image_width,
                                    hand_landmarks.landmark[8].y * image_height, 20, (0, 0, 250))
                else:
                    norCli = 0

                # 動かす###########################################################################
                # cursor
                if absUgo >= dis and nowUgo == 1:
                    mouse.move(dx, dy)
                    draw_circle(image, hand_landmarks.landmark[8].x * image_width,
                                hand_landmarks.landmark[8].y * image_height, 8, (250, 0, 0))
                                
                # left click with cooldown
                if nowCli == 1 and nowCli != preCli:
                    if current_time - gesture_state['last_click_time'] > gesture_state['click_cooldown']:
                        if h == 1:                                  # 右クリック終わった直後状態：左クリックしない
                            h = 0
                        elif h == 0:                                # 普段の状態
                            mouse.press(Button.left)
                            add_action("Left Click")
                            gesture_state['last_click_time'] = current_time
                    # print('Click')
                    
                # left click release
                if nowCli == 0 and nowCli != preCli:
                    mouse.release(Button.left)
                    k = 0
                    # print('Release')
                    if douCli == 0:                             # 1回目のクリックが終わったら、時間測る
                        c_start = time.perf_counter()
                        douCli += 1
                    c_end = time.perf_counter()
                    if 10*(c_end-c_start) > 5 and douCli == 1:  # 0.5秒以内にもう一回クリックしたらダブルクリック
                        mouse.click(Button.left, 2)             # double click
                        add_action("Double Click")
                        douCli = 0
                        
                # right click
                if norCli == 1 and norCli != prrCli:
                    # mouse.release(Button.left)                # 何故か必要
                    mouse.press(Button.right)
                    mouse.release(Button.right)
                    add_action("Right Click")
                    h = 1                                       # 右クリック終わった直後状態 h=1
                    # print("right click")
                    
                # ============ SWIPE SCROLLING WITH MOMENTUM ============
                # Folded index finger = scroll mode
                scroll_mode = hand_landmarks.landmark[8].y - hand_landmarks.landmark[5].y > -0.06
                
                if scroll_mode:
                    # Build up velocity for momentum
                    gesture_state['swipe_velocity'][0] = dx * 0.3
                    gesture_state['swipe_velocity'][1] = dy * 0.8  # More sensitive vertical
                    
                    if abs(dy) > 1 and current_time - gesture_state['last_scroll_time'] > gesture_state['scroll_cooldown']:
                        add_action("Scroll")
                        gesture_state['last_scroll_time'] = current_time
                        
                    mouse.scroll(0, -dy/30)  # Faster scrolling
                    draw_circle(image, hand_landmarks.landmark[8].x * image_width,
                                hand_landmarks.landmark[8].y * image_height, 20, (0, 0, 0))
                    nowUgo = 0
                else:
                    # Apply momentum when released
                    if abs(gesture_state['swipe_velocity'][1]) > 0.5:
                        mouse.scroll(0, -gesture_state['swipe_velocity'][1] / 10)
                    gesture_state['swipe_velocity'][0] *= gesture_state['swipe_decay']
                    gesture_state['swipe_velocity'][1] *= gesture_state['swipe_decay']
                    nowUgo = 1

                preCli = nowCli
                prrCli = norCli

        # 表示 #################################################################################
        # Status indicator (top-right corner)
        if c_text == 1:
            # INACTIVE - Red background
            cv2.rectangle(image, (image_width - 220, 10), (image_width - 10, 60), (0, 0, 150), -1)
            cv2.putText(image, "INACTIVE", (image_width - 200, 45),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(image, "Turn ON CapsLock", (20, 450),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            # ACTIVE - Green background
            cv2.rectangle(image, (image_width - 180, 10), (image_width - 10, 60), (0, 150, 0), -1)
            cv2.putText(image, "ACTIVE", (image_width - 160, 45),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv2.putText(image, "cameraFPS:"+str(cfps), (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        p_e = time.perf_counter()
        fps = str(int(1/(float(p_e)-float(p_s))))
        cv2.putText(image, "FPS:"+fps, (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        
        dst = cv2.resize(image, dsize=None, fx=0.4,
                         fy=0.4)         # HDの0.4倍で表示
        cv2.imshow(window_name, dst)
        if (cv2.waitKey(1) & 0xFF == 27) or (cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) == 0):
            break
    
    # Cleanup
    stop_overlay()
    cap.release()


if __name__ == "__main__":
    main()
