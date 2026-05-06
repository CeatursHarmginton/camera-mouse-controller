#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Floating overlay window for NonMouse action history
Always on top, semi-transparent, draggable
Improved: Consolidated gestures, modern minimal design
"""

import tkinter as tk
import time
import threading
from collections import OrderedDict


class ActionOverlay:
    def __init__(self):
        self.root = None
        self.actions = OrderedDict()  # {action_name: (count, last_timestamp)}
        self.ACTION_DISPLAY_TIME = 1.5  # seconds
        self.running = False
        self.drag_data = {"x": 0, "y": 0}
        
    def start(self):
        """Start the overlay in a separate thread"""
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop the overlay"""
        self.running = False
        if self.root:
            try:
                self.root.quit()
            except:
                pass
    
    def add_action(self, action_name):
        """Add an action - consolidates same actions"""
        current_time = time.time()
        
        # Normalize scroll actions
        if 'Scroll' in action_name:
            action_name = 'Scroll'  # Consolidate all scrolls
        
        # If action exists and is recent, increment count
        if action_name in self.actions:
            count, last_time = self.actions[action_name]
            if current_time - last_time < 0.5:  # Within 500ms, increment
                self.actions[action_name] = (count + 1, current_time)
            else:
                self.actions[action_name] = (1, current_time)
        else:
            self.actions[action_name] = (1, current_time)
        
        # Move to end (most recent)
        self.actions.move_to_end(action_name)
        
        # Keep only last 4 unique actions
        while len(self.actions) > 4:
            self.actions.popitem(last=False)
        
    def _run(self):
        """Main overlay loop"""
        self.root = tk.Tk()
        self.root.title("")
        
        # Window properties
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.92)
        
        # Colors
        self.bg_color = '#0d0d0d'
        self.accent = '#00ff88'
        
        self.root.configure(bg=self.bg_color)
        
        # Position at bottom-left
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 180
        window_height = 160
        x = 20
        y = screen_height - window_height - 60
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Main container with rounded corners effect
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Header bar (draggable)
        self.header = tk.Frame(self.main_frame, bg='#1a1a1a', height=28)
        self.header.pack(fill='x')
        self.header.pack_propagate(False)
        
        # Status indicator dot
        self.status_dot = tk.Label(self.header, text="●", 
                                   bg='#1a1a1a', fg=self.accent,
                                   font=('Segoe UI', 8))
        self.status_dot.pack(side='left', padx=6)
        
        # Title
        title = tk.Label(self.header, text="NonMouse", 
                        bg='#1a1a1a', fg='#888888',
                        font=('Segoe UI', 9))
        title.pack(side='left')
        
        # Drag grip
        grip = tk.Label(self.header, text="≡", 
                       bg='#1a1a1a', fg='#444444',
                       font=('Segoe UI', 10))
        grip.pack(side='right', padx=8)
        
        # Bind drag events to header elements
        for widget in [self.header, title, grip, self.status_dot]:
            widget.bind('<Button-1>', self._start_drag)
            widget.bind('<B1-Motion>', self._do_drag)
        
        # Separator line
        sep = tk.Frame(self.main_frame, bg='#333333', height=1)
        sep.pack(fill='x')
        
        # Actions container
        self.actions_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.actions_frame.pack(fill='both', expand=True, padx=8, pady=6)
        
        # Pre-create action labels
        self.action_labels = []
        for i in range(4):
            frame = tk.Frame(self.actions_frame, bg=self.bg_color)
            frame.pack(fill='x', pady=3)
            
            icon = tk.Label(frame, text="", bg=self.bg_color, 
                           font=('Segoe UI', 10), width=2)
            icon.pack(side='left')
            
            text = tk.Label(frame, text="", bg=self.bg_color,
                           font=('Consolas', 10), anchor='w')
            text.pack(side='left', fill='x', expand=True)
            
            count = tk.Label(frame, text="", bg=self.bg_color,
                            fg='#555555', font=('Consolas', 9))
            count.pack(side='right')
            
            self.action_labels.append((icon, text, count))
        
        # Start update loop
        self._update_display()
        self.root.mainloop()
    
    def _start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
    
    def _do_drag(self, event):
        x = self.root.winfo_x() + (event.x - self.drag_data["x"])
        y = self.root.winfo_y() + (event.y - self.drag_data["y"])
        self.root.geometry(f'+{x}+{y}')
    
    def _update_display(self):
        if not self.running:
            return
            
        current_time = time.time()
        
        # Remove expired actions
        expired = [k for k, (c, t) in self.actions.items() 
                   if current_time - t > self.ACTION_DISPLAY_TIME]
        for k in expired:
            del self.actions[k]
        
        # Action styling
        action_styles = {
            'Left Click': ('◉', '#ffcc00'),      # Yellow dot
            'Right Click': ('◎', '#ff6666'),     # Red ring
            'Double Click': ('⚡', '#00ccff'),    # Cyan bolt
            'Scroll': ('↕', '#aaaaaa'),          # Gray arrows
            'Zoom In': ('🔍', '#66ff66'),         # Green magnify
            'Zoom Out': ('🔎', '#ff9966'),        # Orange magnify
        }
        
        # Update labels (most recent first)
        items = list(reversed(self.actions.items()))
        
        for i, (icon_label, text_label, count_label) in enumerate(self.action_labels):
            if i < len(items):
                action, (count, timestamp) = items[i]
                age = current_time - timestamp
                alpha = max(0.4, 1 - (age / self.ACTION_DISPLAY_TIME))
                
                icon, color = action_styles.get(action, ('•', '#00ff88'))
                
                # Apply alpha to color
                faded_color = self._fade_color(color, alpha)
                
                icon_label.config(text=icon, fg=faded_color)
                text_label.config(text=action, fg=faded_color)
                
                # Show count only if > 1
                if count > 1:
                    count_label.config(text=f"×{count}", fg=self._fade_color('#666666', alpha))
                else:
                    count_label.config(text="")
            else:
                icon_label.config(text="")
                text_label.config(text="")
                count_label.config(text="")
        
        # Update status dot based on activity
        if self.actions:
            self.status_dot.config(fg=self.accent)
        else:
            self.status_dot.config(fg='#333333')
        
        if self.running and self.root:
            self.root.after(50, self._update_display)
    
    def _fade_color(self, hex_color, alpha):
        """Fade color towards background"""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        bg_r, bg_g, bg_b = 13, 13, 13  # #0d0d0d
        
        r = int(bg_r + (r - bg_r) * alpha)
        g = int(bg_g + (g - bg_g) * alpha)
        b = int(bg_b + (b - bg_b) * alpha)
        
        return f'#{r:02x}{g:02x}{b:02x}'


# Global instance
_overlay = None

def start_overlay():
    global _overlay
    if _overlay is None:
        _overlay = ActionOverlay()
        _overlay.start()
    return _overlay

def stop_overlay():
    global _overlay
    if _overlay:
        _overlay.stop()
        _overlay = None

def add_action(action_name):
    global _overlay
    if _overlay:
        _overlay.add_action(action_name)


if __name__ == "__main__":
    # Test
    overlay = start_overlay()
    import time as t
    t.sleep(1)
    for _ in range(5):
        add_action("Scroll Up")
        t.sleep(0.1)
    t.sleep(0.5)
    add_action("Left Click")
    t.sleep(0.3)
    add_action("Left Click")
    t.sleep(0.5)
    add_action("Right Click")
    t.sleep(5)
