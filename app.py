from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
import pulmo

class MainWindow(Screen):  # Az app első ablaka, innen lehetne továbblépni választás alapján
    pass


class GradiensWindow(Screen):
    def szamol(self):
        pass
    pass


class IzokratikusWindow(Screen):

    def szamol(self):
        try:
            izoseb = float(self.ids.izo_seb.text)
            mintaido = int(self.ids.minta_ido.text)
            mintak = int(self.ids.mintak_szama.text)
            stdido = int(self.ids.std_ido.text)
            stdk = int(self.ids.std_szama.text)

        except ValueError:
            print("faszom")

        a = (izoseb * mintaido * mintak) + (izoseb * stdido * stdk)
        self.ids.eluens.text = str(a) + " mL"


class AranyScreen(Screen):
    pass


class Hplc(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainWindow(name="MainWindow"))
        sm.add_widget(GradiensWindow(name="GradiensWindow"))
        sm.add_widget(IzokratikusWindow(name="IzokratikusWindow"))
        sm.add_widget(AranyScreen(name="AranyScreen"))
        return sm


if __name__ == '__main__':
    Hplc().run()
