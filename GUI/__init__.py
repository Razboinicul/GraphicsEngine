import PySimpleGUI as sg
import sys, os
from text import *
from pys import *
from lua_interpreter import interpret_code
import vars
vars.win = lambda: start()
vars.main = lambda: main_win()
lua_init = """function _ready ()
    print("Ready")
end
function _process ()
    print("Process")
end"""

def start():
    layout = [[sg.Button(button_text="New Project", key="NP")],
              [sg.Button(button_text="Load Project", key="LP")]]
    window = sg.Window("Pysudo Engine", layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED: sys.exit()
        if event == "NP": 
            vars.win = lambda: new_project()
            break
        if event == "LP": 
            vars.win = lambda: load_project()
            break
    window.close()

def new_project():
    layout = [[sg.Text("Project Name:"), sg.Input(key='P_NAME')],
            [sg.Text("Project Path:"), sg.Input(key='P_PATH', change_submits=True), sg.FolderBrowse(key="P_BROWSE")],
            [sg.Button('Create'), sg.Button('Quit')]]
    window = sg.Window('New Project', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            sys.exit()
        if event == "Create":
            vars.p_name = values["P_NAME"]
            vars.p_path = values["P_PATH"]
            write_pys_file()
            f = open(vars.p_path+"/main.lua", "w+")
            f.writelines(lua_init)
            f.close()
            vars.win = lambda: main_win()
            break
    window.close()

def load_project():
    layout = [[sg.Text("Project Path:"), sg.Input(key='P_PATH'), sg.FolderBrowse(key="P_BROWSE")],
            [sg.Button('Load')]]
    window = sg.Window('Load Project', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            sys.exit()
        if event == "Load":
            vars.p_path = values["P_PATH"]
            read_pys_file()
            vars.win = lambda: main_win()
            break
    window.close()

def test():
    layout = []
    window = sg.Window('Test', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            sys.exit()
    window.close()

def main_win():
    vars.win = lambda: main_win()
    layout = [[sg.Button('Sprites', key="SP")],
              [sg.Button("Code Editor", key="CE")],
              [sg.Button("Run Game", key="Run")],
              [sg.Button('Quit')]]
    window = sg.Window(vars.p_name, layout)
    print(vars.p_name, vars.p_path)
    while True:
        event, values = window.read()
        if event == "CE": 
            vars.win = lambda: text_editor()
            break
        if event == "Run":
            interpret_code(vars.p_path+"/main.lua")
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            sys.exit()
    window.close()

if __name__ == "__main__":
    while True:
        vars.win()
