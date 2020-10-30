import json
import threading
import time
import tkinter
import sys

from pynput import mouse
from pynput.mouse import Controller as mouseController, Button
from pynput import keyboard
from pynput.keyboard import Controller as keyController, KeyCode



file_name = r'D:\mouse_action.txt'

def mouse_action_template():
    return {
        "name": "mouse",
        "event": "default",
        "target": "default",
        "action": "default",
        "location": {
            "x": "0",
            "y": "0"
        }
    }

def keyboard_action_template():
    return {
        "name": "keyboard",
        "event": "default",
        "vk": "default"
    }

def start_monitor():
	global flag
	print('开始录制')
	startListenerBtn['text'] = '录制中'
	startListenerBtn['state'] = 'disabled'
	stopListenerBtn['state'] = 'active'
	exitProcessBtn['state'] = 'disabled'
	with open(file_name, 'w', encoding='utf-8') as file:
		pass
	def on_move(x, y):
		print('move')
		print('Pointer moved to {0}'.format(
        (x, y)))
		if flag == 2:
			return False
		with open(file_name, 'a', encoding='utf-8') as file:
			template = mouse_action_template()
			template['event'] = 'move'
			template['location']['x'] = x
			template['location']['y'] = y
			file.writelines(json.dumps(template) + "\n")
			file.flush()
	def on_click(x, y, button, pressed):
		print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
		if flag == 2:
			if pressed:
				return False
		with open(file_name, 'a', encoding='utf-8') as file:
		    template = mouse_action_template()
		    template['event'] = 'click'
		    template['target'] = button.name
		    template['action'] = pressed
		    template['location']['x'] = x
		    template['location']['y'] = y
		    file.writelines(json.dumps(template) + "\n")
		    file.flush()
	def on_scroll(x, y, dx, dy):
		print('scroll')
		print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up',(x, y)))
		if flag == 2:
			return False
		with open(file_name, 'a', encoding='utf-8') as file:
		    template = mouse_action_template()
		    template['event'] = 'scroll'
		    template['location']['x'] = dx
		    template['location']['y'] = dy
		    file.writelines(json.dumps(template) + "\n")
		    file.flush()

	def  on_press(key):
		if flag == 2:
			return False
		with open(file_name, 'a', encoding='utf-8') as file:
			template = keyboard_action_template()
			template['event'] = 'press'
			try:
			    template['vk'] = key.vk
			except AttributeError:
			    template['vk'] = key.value.vk
			finally:
			    file.writelines(json.dumps(template) + "\n")
			    file.flush()

	def on_release(key):
		if flag == 2:
			return False
		with open(file_name, 'a', encoding='utf-8') as file:
			template = keyboard_action_template()
			template['event'] = 'release'
			try:
			    template['vk'] = key.vk
			except AttributeError:
			    template['vk'] = key.value.vk
			finally:
			    file.writelines(json.dumps(template) + "\n")
			    file.flush()

	mouse_listener = mouse.Listener(
	    on_move=on_move,
	    on_click=on_click,
	    on_scroll=on_scroll)
	key_listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
	mouse_listener.start()
	key_listener.start()

def stop_monitor():
	global flag
	flag = 2
	print('停止录制')
	startListenerBtn['text'] = '开始录制'
	startListenerBtn['state'] = 'active'
	stopListenerBtn['state'] = 'disabled'
	exitProcessBtn['state'] = 'active'

def exit_process():
	print('退出程序')
	sys.exit()

def execute():
    with open(file_name, 'r', encoding='utf-8') as file:
        mouse_exec = mouseController()
        keyboard_exec = keyController()
        line = file.readline()
        time.sleep(0.01)
        while line:
            obj = json.loads(line)
            if obj['name'] == 'mouse':
                if obj['event'] == 'move':
                    mouse_exec.position = (obj['location']['x'], obj['location']['y'])
                    time.sleep(0.01)
                elif obj['event'] == 'click':
                    if obj['action']:
                        if obj['target'] == 'left':
                            mouse_exec.press(Button.left)
                        else:
                            mouse_exec.press(Button.right)
                    else:
                        if obj['target'] == 'left':
                            mouse_exec.release(Button.left)
                        else:
                            mouse_exec.release(Button.right)
                    time.sleep(0.01)
                elif obj['event'] == 'scroll':
                    mouse_exec.scroll(obj['location']['x'], obj['location']['y'])
                    time.sleep(0.01)
            elif obj['name'] == 'keyboard':
                if obj['event'] == 'press':
                    keyboard_exec.press(KeyCode.from_vk(obj['vk']))
                    time.sleep(0.1)

                elif obj['event'] == 'release':
                    keyboard_exec.release(KeyCode.from_vk(obj['vk']))
                    time.sleep(0.1)
            line = file.readline()


if __name__ == "__main__":
	root = tkinter.Tk()
	root.title('录制精灵')
	root.geometry('250x300+600+200')
	flag = 1
	startListenerBtn = tkinter.Button(root, text="开始录制", command=lambda: start_monitor())
	startListenerBtn.place(x=10, y=10, width=100, height=50)

	stopListenerBtn = tkinter.Button(root, text="停止录制", command=lambda: stop_monitor())
	stopListenerBtn.place(x=10, y=80, width=100, height=50)

	exitProcessBtn = tkinter.Button(root, text="退出程序", command=lambda: exit_process())
	exitProcessBtn.place(x=10, y=150, width=100, height=50)

	executeProcessBtn = tkinter.Button(root, text="回放", command=lambda: execute())
	executeProcessBtn.place(x=10, y=220, width=100, height=50)
	root.mainloop()