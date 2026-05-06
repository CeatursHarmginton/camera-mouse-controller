#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from nonmouse.config import load_config, save_config


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
    root.geometry("400x400")
    root.configure(bg='#2b2b2b')
    
    screenRes = (root.winfo_screenwidth(), root.winfo_screenheight())
    
    Val1 = tk.IntVar(value=config['camera'])
    Val2 = tk.IntVar(value=config['mode'])
    Val4 = tk.IntVar(value=config['sensitivity'])
    Val5 = tk.IntVar(value=config.get('skip_setup', False))
    
    place = ['Normal', 'Above', 'Behind']
    
    # Styles
    label_style = {'bg': '#2b2b2b', 'fg': '#00ff00', 'font': ('Arial', 11, 'bold')}
    radio_style = {'bg': '#2b2b2b', 'fg': '#ffffff', 'selectcolor': '#1a1a1a', 
                   'activebackground': '#2b2b2b', 'activeforeground': '#00ff00'}
    
    # Title
    tk.Label(root, text="NonMouse Configuration", bg='#2b2b2b', fg='#00ff00', 
             font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=8, pady=10)
    
    # Camera
    tk.Label(root, text='📷 Camera', **label_style).grid(row=1, column=0, columnspan=8, pady=(10,5))
    for i in range(4):
        tk.Radiobutton(root, value=i, variable=Val1, text=f'Device {i}', 
                       **radio_style).grid(row=2, column=i*2, padx=5)
    
    # Place
    tk.Label(root, text='📍 Camera Position', **label_style).grid(row=4, column=0, columnspan=8, pady=(15,5))
    for i in range(3):
        tk.Radiobutton(root, value=i, variable=Val2, text=f'{place[i]}',
                       **radio_style).grid(row=5, column=i*2+1, padx=5)
    
    # Sensitivity
    tk.Label(root, text='🎯 Sensitivity', **label_style).grid(row=7, column=0, columnspan=8, pady=(15,5))
    tk.Scale(root, orient='h', from_=1, to=100, variable=Val4, length=200,
             bg='#2b2b2b', fg='#00ff00', troughcolor='#1a1a1a', 
             highlightthickness=0).grid(row=8, column=0, columnspan=8)
    
    # Skip setup checkbox
    tk.Checkbutton(root, text="Skip this dialog next time", variable=Val5,
                   bg='#2b2b2b', fg='#ffffff', selectcolor='#1a1a1a',
                   activebackground='#2b2b2b', activeforeground='#00ff00'
                   ).grid(row=10, column=0, columnspan=8, pady=(20,5))
    
    # Continue button
    def on_continue():
        # Save config
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
    
    tk.Button(root, text="▶ Start NonMouse", command=on_continue,
              bg='#00aa00', fg='white', font=('Arial', 12, 'bold'),
              activebackground='#00ff00', width=15, height=2
              ).grid(row=11, column=0, columnspan=8, pady=20)
    
    # Info label
    tk.Label(root, text="💡 Tip: Use CapsLock to toggle hand tracking", 
             bg='#2b2b2b', fg='#888888', font=('Arial', 9)
             ).grid(row=12, column=0, columnspan=8)
    
    root.mainloop()
    
    # Return values
    cap_device = Val1.get()
    mode = Val2.get()
    kando = Val4.get()/10
    return cap_device, mode, kando, screenRes
