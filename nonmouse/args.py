#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from nonmouse.config import load_config, save_config

# Path to images directory
IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')

# Gesture data
GESTURES = [
    {
        'name': 'Move Cursor',
        'emoji': '☝️',
        'icon': '🖱️',
        'color': '#3b82f6',       # Blue
        'indicator': '🔵 Blue dot',
        'image': 'gesture_move_cursor_1769252514204.png',
        'short': 'Point with index finger',
        'steps': [
            'Extend your index finger straight',
            'Keep other fingers folded',
            'Move your hand to move cursor',
            'Blue dot follows your fingertip'
        ]
    },
    {
        'name': 'Stop Cursor',
        'emoji': '✌️',
        'icon': '⏸️',
        'color': '#6b7280',       # Gray
        'indicator': 'No dot',
        'image': None,
        'short': 'Touch index + middle tips',
        'steps': [
            'Touch index + middle fingertips together',
            'Cursor freezes in place',
            'Release to resume tracking'
        ]
    },
    {
        'name': 'Left Click',
        'emoji': '👍',
        'icon': '🖱️',
        'color': '#eab308',       # Yellow
        'indicator': '🟡 Yellow circle',
        'image': 'gesture_left_click_1769252530545.png',
        'short': 'Thumb to index 2nd joint',
        'steps': [
            'Touch thumb tip to index finger\'s 2nd joint',
            'Quick touch = single click',
            'Two quick clicks = double click',
            'Yellow circle appears on fingertip'
        ]
    },
    {
        'name': 'Right Click',
        'emoji': '✊',
        'icon': '🖱️',
        'color': '#ef4444',       # Red
        'indicator': '🔴 Red circle',
        'image': None,
        'short': 'Hold click for 1.5s',
        'steps': [
            'Hold left click position for 1.5 seconds',
            'Don\'t move cursor while holding',
            'Red circle appears when triggered',
            'Release to complete right click'
        ]
    },
    {
        'name': 'Scroll',
        'emoji': '👆',
        'icon': '📜',
        'color': '#1f2937',       # Dark
        'indicator': '⚫ Black circle',
        'image': 'gesture_scroll_1769252544618.png',
        'short': 'Fold index finger + move',
        'steps': [
            'Fold your index finger (curl it down)',
            'Move hand up/down to scroll',
            'Quick swipe then release for momentum!',
            'Black circle appears during scroll'
        ]
    },
    {
        'name': 'Zoom In / Out',
        'emoji': '🤏',
        'icon': '🔍',
        'color': '#a855f7',       # Purple
        'indicator': '🟣 Purple / 🔵 Cyan',
        'image': 'gesture_pinch_zoom_1769252559440.png',
        'short': 'Pinch or spread thumb + index',
        'steps': [
            'Pinch thumb + index together = Zoom Out',
            'Spread thumb + index apart = Zoom In',
            'Purple circle = Zoom Out',
            'Cyan circle = Zoom In'
        ]
    },
]


def tk_arg():
    config = load_config()
    
    # Skip setup if config exists and skip_setup is True
    if config.get('skip_setup', False):
        root = tk.Tk()
        screenRes = (root.winfo_screenwidth(), root.winfo_screenheight())
        root.destroy()
        return config['camera'], config['mode'], config['sensitivity']/10, screenRes
    
    root = tk.Tk()
    root.title("NonMouse Setup")
    
    # ── Color palette ──
    BG_DARK = '#1a1a2e'
    BG_PANEL = '#16213e'
    BG_CARD = '#0f3460'
    ACCENT = '#00ff88'
    ACCENT2 = '#00d4ff'
    TEXT_PRIMARY = '#e0e0e0'
    TEXT_DIM = '#8892a4'
    TEXT_BRIGHT = '#ffffff'
    BORDER = '#2a3a5c'
    HOVER_BG = '#1a3a6e'
    
    # Window setup
    win_w, win_h = 920, 600
    root.geometry(f"{win_w}x{win_h}")
    root.configure(bg=BG_DARK)
    root.resizable(False, False)
    
    # Center window
    root.update_idletasks()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w - win_w) // 2
    y = (screen_h - win_h) // 2
    root.geometry(f"{win_w}x{win_h}+{x}+{y}")
    
    screenRes = (screen_w, screen_h)
    
    Val1 = tk.IntVar(value=config['camera'])
    Val2 = tk.IntVar(value=config['mode'])
    Val4 = tk.IntVar(value=config['sensitivity'])
    Val5 = tk.IntVar(value=config.get('skip_setup', False))
    
    place = ['Normal', 'Above', 'Behind']
    
    # ══════════════════════════════════════════════
    #  HEADER BAR
    # ══════════════════════════════════════════════
    header = tk.Frame(root, bg=BG_PANEL, height=50)
    header.pack(fill='x')
    header.pack_propagate(False)
    
    # Logo area
    logo_frame = tk.Frame(header, bg=BG_PANEL)
    logo_frame.pack(side='left', padx=20)
    
    tk.Label(logo_frame, text="●", bg=BG_PANEL, fg=ACCENT,
             font=('Segoe UI', 14)).pack(side='left')
    tk.Label(logo_frame, text=" NonMouse", bg=BG_PANEL, fg=TEXT_BRIGHT,
             font=('Segoe UI', 16, 'bold')).pack(side='left')
    tk.Label(logo_frame, text="  Setup", bg=BG_PANEL, fg=TEXT_DIM,
             font=('Segoe UI', 12)).pack(side='left')
    
    # Header right - version
    tk.Label(header, text="Camera Mouse Controller", bg=BG_PANEL, fg=TEXT_DIM,
             font=('Segoe UI', 9)).pack(side='right', padx=20)
    
    # Accent line
    tk.Frame(root, bg=ACCENT, height=2).pack(fill='x')
    
    # ══════════════════════════════════════════════
    #  MAIN CONTENT AREA (split left / right)
    # ══════════════════════════════════════════════
    content = tk.Frame(root, bg=BG_DARK)
    content.pack(fill='both', expand=True, padx=0, pady=0)
    
    # ── LEFT PANEL: Settings ──
    left_panel = tk.Frame(content, bg=BG_DARK, width=400)
    left_panel.pack(side='left', fill='both', padx=(20, 10), pady=15)
    left_panel.pack_propagate(False)
    
    # Section title helper
    def section_title(parent, text, emoji=''):
        frame = tk.Frame(parent, bg=BG_DARK)
        frame.pack(fill='x', pady=(12, 6))
        tk.Label(frame, text=f"{emoji} {text}", bg=BG_DARK, fg=ACCENT,
                 font=('Segoe UI', 11, 'bold')).pack(side='left')
        # Decorative line
        line_frame = tk.Frame(frame, bg=BG_DARK)
        line_frame.pack(side='left', fill='x', expand=True, padx=(10, 0))
        tk.Frame(line_frame, bg=BORDER, height=1).pack(fill='x', pady=8)
        return frame
    
    # Card frame helper
    def card_frame(parent, **kwargs):
        f = tk.Frame(parent, bg=BG_PANEL, highlightbackground=BORDER,
                     highlightthickness=1, **kwargs)
        f.pack(fill='x', pady=4, ipady=6, ipadx=8)
        return f
    
    # ── Camera Selection ──
    section_title(left_panel, 'Camera Device', '📷')
    cam_card = card_frame(left_panel)
    cam_inner = tk.Frame(cam_card, bg=BG_PANEL)
    cam_inner.pack(padx=10, pady=4)
    for i in range(4):
        rb = tk.Radiobutton(cam_inner, value=i, variable=Val1, text=f'  #{i}',
                           bg=BG_PANEL, fg=TEXT_PRIMARY, selectcolor=BG_CARD,
                           activebackground=BG_PANEL, activeforeground=ACCENT,
                           font=('Consolas', 10), indicatoron=True)
        rb.pack(side='left', padx=8)
    
    # ── Camera Position ──
    section_title(left_panel, 'Camera Position', '📍')
    pos_card = card_frame(left_panel)
    pos_inner = tk.Frame(pos_card, bg=BG_PANEL)
    pos_inner.pack(padx=10, pady=4)
    pos_icons = ['🖥️', '⬆️', '🔙']
    for i in range(3):
        rb = tk.Radiobutton(pos_inner, value=i, variable=Val2,
                           text=f'  {pos_icons[i]} {place[i]}',
                           bg=BG_PANEL, fg=TEXT_PRIMARY, selectcolor=BG_CARD,
                           activebackground=BG_PANEL, activeforeground=ACCENT,
                           font=('Segoe UI', 10), indicatoron=True)
        rb.pack(side='left', padx=6)
    
    # ── Sensitivity ──
    section_title(left_panel, 'Sensitivity', '🎯')
    sens_card = card_frame(left_panel)
    sens_inner = tk.Frame(sens_card, bg=BG_PANEL)
    sens_inner.pack(fill='x', padx=10, pady=4)
    
    # Sensitivity label with dynamic value
    sens_val_label = tk.Label(sens_inner, text=f"Value: {Val4.get()}", bg=BG_PANEL,
                              fg=ACCENT2, font=('Consolas', 9))
    sens_val_label.pack(side='right', padx=5)
    
    def on_sens_change(val):
        v = int(float(val))
        if v <= 30:
            desc = "Precise"
        elif v <= 60:
            desc = "Balanced"
        else:
            desc = "Fast"
        sens_val_label.config(text=f"{desc} ({v})")
    
    scale = tk.Scale(sens_inner, orient='h', from_=1, to=100, variable=Val4,
                     length=220, bg=BG_PANEL, fg=ACCENT, troughcolor=BG_CARD,
                     highlightthickness=0, sliderrelief='flat',
                     command=on_sens_change)
    scale.pack(side='left')
    
    # ── Options ──
    section_title(left_panel, 'Options', '⚙️')
    opt_card = card_frame(left_panel)
    tk.Checkbutton(opt_card, text="  Skip this dialog next time", variable=Val5,
                   bg=BG_PANEL, fg=TEXT_PRIMARY, selectcolor=BG_CARD,
                   activebackground=BG_PANEL, activeforeground=ACCENT,
                   font=('Segoe UI', 10)).pack(padx=10, pady=2, anchor='w')
    
    # ── Start Button ──
    btn_frame = tk.Frame(left_panel, bg=BG_DARK)
    btn_frame.pack(fill='x', pady=(15, 5))
    
    def on_continue():
        new_config = {
            'camera': Val1.get(),
            'mode': Val2.get(),
            'sensitivity': Val4.get(),
            'smoothing': config.get('smoothing', 3),
            'dead_zone': config.get('dead_zone', 2),
            'skip_setup': bool(Val5.get())
        }
        save_config(new_config)
        root.destroy()
    
    start_btn = tk.Button(btn_frame, text="▶  Start NonMouse", command=on_continue,
                          bg='#00aa44', fg='white', font=('Segoe UI', 13, 'bold'),
                          activebackground=ACCENT, relief='flat', cursor='hand2',
                          width=22, height=2)
    start_btn.pack()
    
    # Hover effects for button
    def on_enter(e):
        start_btn.config(bg=ACCENT, fg=BG_DARK)
    def on_leave(e):
        start_btn.config(bg='#00aa44', fg='white')
    start_btn.bind('<Enter>', on_enter)
    start_btn.bind('<Leave>', on_leave)
    
    # Tip label
    tk.Label(left_panel, text="💡 CapsLock = Toggle hand tracking",
             bg=BG_DARK, fg=TEXT_DIM, font=('Segoe UI', 9)).pack(pady=(5, 0))
    
    # ── SEPARATOR ──
    sep = tk.Frame(content, bg=BORDER, width=1)
    sep.pack(side='left', fill='y', pady=15)
    
    # ══════════════════════════════════════════════
    #  RIGHT PANEL: Gesture Guide
    # ══════════════════════════════════════════════
    right_panel = tk.Frame(content, bg=BG_DARK, width=480)
    right_panel.pack(side='left', fill='both', expand=True, padx=(10, 20), pady=15)
    right_panel.pack_propagate(False)
    
    # Title
    guide_title_frame = tk.Frame(right_panel, bg=BG_DARK)
    guide_title_frame.pack(fill='x')
    tk.Label(guide_title_frame, text="🖐️ Hand Gesture Guide", bg=BG_DARK, fg=ACCENT2,
             font=('Segoe UI', 13, 'bold')).pack(side='left')
    
    # Gesture selector buttons (horizontal tabs)
    tabs_frame = tk.Frame(right_panel, bg=BG_DARK)
    tabs_frame.pack(fill='x', pady=(10, 5))
    
    selected_gesture = tk.IntVar(value=0)
    tab_buttons = []
    
    # Detail display area
    detail_frame = tk.Frame(right_panel, bg=BG_PANEL, highlightbackground=BORDER,
                            highlightthickness=1)
    detail_frame.pack(fill='both', expand=True, pady=(5, 0))
    
    # Pre-load images
    gesture_images = {}
    for g in GESTURES:
        if g['image'] and os.path.exists(os.path.join(IMAGES_DIR, g['image'])):
            try:
                img = Image.open(os.path.join(IMAGES_DIR, g['image']))
                img = img.resize((140, 140), Image.LANCZOS)
                gesture_images[g['name']] = ImageTk.PhotoImage(img)
            except Exception:
                gesture_images[g['name']] = None
        else:
            gesture_images[g['name']] = None
    
    def show_gesture(idx):
        """Display gesture detail for index"""
        selected_gesture.set(idx)
        g = GESTURES[idx]
        
        # Update tab button appearances
        for i, btn in enumerate(tab_buttons):
            if i == idx:
                btn.config(bg=g['color'], fg=TEXT_BRIGHT, relief='solid')
            else:
                btn.config(bg=BG_CARD, fg=TEXT_DIM, relief='flat')
        
        # Clear detail frame
        for w in detail_frame.winfo_children():
            w.destroy()
        
        # ── Top section: title + indicator ──
        top = tk.Frame(detail_frame, bg=BG_PANEL)
        top.pack(fill='x', padx=15, pady=(12, 5))
        
        # Gesture name with emoji
        tk.Label(top, text=f"{g['icon']}  {g['name']}", bg=BG_PANEL, fg=TEXT_BRIGHT,
                 font=('Segoe UI', 16, 'bold')).pack(side='left')
        
        # Color indicator badge
        indicator_badge = tk.Label(top, text=f"  {g['indicator']}  ", bg=BG_CARD,
                                   fg=g['color'], font=('Segoe UI', 9),
                                   relief='flat', padx=8, pady=2)
        indicator_badge.pack(side='right')
        
        # Short description
        tk.Label(detail_frame, text=g['short'], bg=BG_PANEL, fg=ACCENT,
                 font=('Segoe UI', 10, 'italic')).pack(padx=15, anchor='w')
        
        # ── Middle section: image + steps side by side ──
        mid = tk.Frame(detail_frame, bg=BG_PANEL)
        mid.pack(fill='both', expand=True, padx=15, pady=(10, 10))
        
        # Image (left side of mid)
        img_tk = gesture_images.get(g['name'])
        if img_tk:
            img_container = tk.Frame(mid, bg=BG_CARD, highlightbackground=BORDER,
                                     highlightthickness=1)
            img_container.pack(side='left', padx=(0, 12), pady=5)
            img_label = tk.Label(img_container, image=img_tk, bg=BG_CARD)
            img_label.image = img_tk  # Keep reference
            img_label.pack(padx=6, pady=6)
        else:
            # No image - show large emoji placeholder
            placeholder = tk.Frame(mid, bg=BG_CARD, width=152, height=152,
                                   highlightbackground=BORDER, highlightthickness=1)
            placeholder.pack(side='left', padx=(0, 12), pady=5)
            placeholder.pack_propagate(False)
            tk.Label(placeholder, text=g['emoji'], bg=BG_CARD,
                     font=('Segoe UI', 48)).pack(expand=True)
        
        # Steps (right side of mid)
        steps_frame = tk.Frame(mid, bg=BG_PANEL)
        steps_frame.pack(side='left', fill='both', expand=True, pady=5)
        
        tk.Label(steps_frame, text="How to:", bg=BG_PANEL, fg=TEXT_DIM,
                 font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=(0, 6))
        
        for j, step in enumerate(g['steps']):
            step_row = tk.Frame(steps_frame, bg=BG_PANEL)
            step_row.pack(fill='x', pady=2)
            
            # Step number circle
            tk.Label(step_row, text=f" {j+1} ", bg=g['color'], fg=TEXT_BRIGHT,
                     font=('Consolas', 8, 'bold'), width=3).pack(side='left', padx=(0, 8))
            
            # Step text
            tk.Label(step_row, text=step, bg=BG_PANEL, fg=TEXT_PRIMARY,
                     font=('Segoe UI', 9), wraplength=230, justify='left',
                     anchor='w').pack(side='left', fill='x')
        
        # ── Bottom: navigation hint ──
        nav = tk.Frame(detail_frame, bg=BG_PANEL)
        nav.pack(fill='x', padx=15, pady=(0, 8))
        
        # Prev/Next buttons
        if idx > 0:
            prev_name = GESTURES[idx - 1]['name']
            prev_btn = tk.Label(nav, text=f"◀ {prev_name}", bg=BG_PANEL, fg=TEXT_DIM,
                               font=('Segoe UI', 9), cursor='hand2')
            prev_btn.pack(side='left')
            prev_btn.bind('<Button-1>', lambda e, i=idx-1: show_gesture(i))
            prev_btn.bind('<Enter>', lambda e, w=prev_btn: w.config(fg=ACCENT))
            prev_btn.bind('<Leave>', lambda e, w=prev_btn: w.config(fg=TEXT_DIM))
        
        if idx < len(GESTURES) - 1:
            next_name = GESTURES[idx + 1]['name']
            next_btn = tk.Label(nav, text=f"{next_name} ▶", bg=BG_PANEL, fg=TEXT_DIM,
                               font=('Segoe UI', 9), cursor='hand2')
            next_btn.pack(side='right')
            next_btn.bind('<Button-1>', lambda e, i=idx+1: show_gesture(i))
            next_btn.bind('<Enter>', lambda e, w=next_btn: w.config(fg=ACCENT))
            next_btn.bind('<Leave>', lambda e, w=next_btn: w.config(fg=TEXT_DIM))
    
    # Create tab buttons
    for i, g in enumerate(GESTURES):
        btn = tk.Button(tabs_frame, text=f"{g['emoji']}",
                       bg=BG_CARD, fg=TEXT_DIM, font=('Segoe UI', 12),
                       relief='flat', cursor='hand2', width=3, height=1,
                       command=lambda idx=i: show_gesture(idx))
        btn.pack(side='left', padx=2)
        
        # Tooltip on hover
        def make_enter(b, gesture):
            def fn(e):
                if selected_gesture.get() != GESTURES.index(gesture):
                    b.config(bg=HOVER_BG)
            return fn
        def make_leave(b, gesture):
            def fn(e):
                idx = GESTURES.index(gesture)
                if selected_gesture.get() != idx:
                    b.config(bg=BG_CARD)
            return fn
        
        btn.bind('<Enter>', make_enter(btn, g))
        btn.bind('<Leave>', make_leave(btn, g))
        tab_buttons.append(btn)
    
    # Gesture name labels under tabs
    names_frame = tk.Frame(right_panel, bg=BG_DARK)
    names_frame.pack(fill='x', pady=(0, 3))
    for g in GESTURES:
        short_name = g['name'].split('/')[0].strip()  # Take first part if "X / Y"
        if len(short_name) > 8:
            short_name = short_name[:7] + '..'
        tk.Label(names_frame, text=short_name, bg=BG_DARK, fg=TEXT_DIM,
                 font=('Segoe UI', 7), width=7).pack(side='left', padx=2)
    
    # Show first gesture by default
    show_gesture(0)
    
    # ══════════════════════════════════════════════
    #  FOOTER
    # ══════════════════════════════════════════════
    footer = tk.Frame(root, bg=BG_PANEL, height=28)
    footer.pack(fill='x', side='bottom')
    footer.pack_propagate(False)
    tk.Label(footer, text="NonMouse — Webcam-based virtual gesture mouse  |  Use CapsLock to toggle",
             bg=BG_PANEL, fg=TEXT_DIM, font=('Segoe UI', 8)).pack(pady=5)
    
    root.mainloop()
    
    # Return values
    cap_device = Val1.get()
    mode = Val2.get()
    kando = Val4.get()/10
    return cap_device, mode, kando, screenRes
