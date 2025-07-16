from vision import ChessVision
from chess import ChessGame
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App

class MenuScreen(Screen):
    pass

class ChessApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(ChessVision(name="chessvision"))
        sm.add_widget(ChessGame(name="chessgame"))
        return sm


if __name__ == "__main__":
    ChessApp().run()
