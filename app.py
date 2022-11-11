from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window


Window.clearcolor = (0.098, 0.2549, 0.48627, 0.6625)
Builder.load_file('Hplc.kv')
sm = ScreenManager()

class NameScreen(Screen):
    megadott_nev = StringProperty(None)

    '''def mérés_gomb(self):
        pulmo.nev = self.megadott_nev
        print(pulmo.nev)
'''

class MainWindow(Screen):  # Az app első ablaka, innen lehet továbblépni választás alapján
    pass


class GradiensWindow(Screen):
    idok = ObjectProperty(None)
    ido_lista = ListProperty([])

    def g_szamol(self):
        
        grad_seb = float(self.ids.grad_seb.text)
        gmintak_szama = int(self.ids.gmintak_szama.text)
        gstd_szama = int(self.ids.gstd_szama.text)
        a_arany = []
        b_arany = []
        idok = []
        for i in range(5):
            a_arany.append(int(sm.get_screen('AranyScreen').ids[f"a_arany_in{i}"].text))
            b_arany.append(int(sm.get_screen('AranyScreen').ids[f"b_arany_in{i}"].text))
            idok.append(int(self.ids[f"idok_in{i}"].text))
        a = 0
        b = 0
        for _ in range(int(gmintak_szama + gstd_szama)):
            for i, j in zip(a_arany, idok):
                a += i / 100 * j * grad_seb
            for i, j in zip(b_arany, idok):
                b += i / 100 * j * grad_seb
        a = round(a, 4)
        b = round(b, 4)
        self.ids.a_eluens.text = f"{str(a)} mL"
        self.ids.b_eluens.text = f"{str(b)} mL"
    pass

    
class IzokratikusWindow(Screen):
    
    
    def i_szamol(self):
        # DRY nem érvényesül, sok try except blokk, rövidithető lenne itt a kód.
        try:
            izo_seb = float(self.ids.izo_seb.text)
        except ValueError:
            self.ids.izo_seb.text = '0'
            izo_seb = float(self.ids.izo_seb.text)
        try:
            int(self.ids.minta_ido.text).is_integer
        except ValueError:
            self.ids.minta_ido.text = '0'
            minta_ido = int(self.ids.minta_ido.text)
        try:
            mintak_szama = int(self.ids.mintak_szama.text)
        except ValueError:
            self.ids.mintak_szama.text = '0'
            mintak_szama = int(self.ids.mintak_szama.text)
        try:
            std_ido = int(self.ids.std_ido.text)
        except ValueError:
            self.ids.std_ido.text = '0'
            std_ido = int(self.ids.std_ido.text)
        try:
            std_szama = int(self.ids.std_szama.text)
        except ValueError:
            self.ids.std_szama.text = '0'
            std_szama = int(self.ids.std_szama.text)

        a = (izo_seb * minta_ido * mintak_szama) + (izo_seb * std_ido * std_szama)
        self.ids.eluens.text = str(a) + " mL"


class AranyScreen(Screen):
    def automatikus_szamolo(self):
        pass
    pass


class Hplc(App):

    def build(self):
        sm.add_widget(MainWindow(name="MainWindow"))
        sm.add_widget(GradiensWindow(name="GradiensWindow"))
        sm.add_widget(IzokratikusWindow(name="IzokratikusWindow"))
        sm.add_widget(AranyScreen(name="AranyScreen"))
        sm.add_widget(NameScreen(name="NameScreen"))

        return sm


if __name__ == '__main__':
    Hplc().run()
