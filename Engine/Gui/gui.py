from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.widget import Widget
from Engine.Injector.injector import Injector
from Engine.Nozzle.nozzle import Nozzle
from Engine.Propellants.side_classes import Ballistic
from Engine.Propellants.fuel import Fuel
from Engine.Propellants.oxidizer import Oxidizer
from Engine.Vessel.vessel import Vessel
from Engine.engine_simulation import Engine
import matplotlib.pyplot as plt
class MyGrid(Widget):
    pass


class MyApp(App):
    # def build(self):
    #     #returns a window object with all it's widgets
    #     self.window = GridLayout()
    #     self.window.cols = 2
    #
    #     self.window.size_hint = (0.6, 0.7)
    #     self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}
    #
    #     # image widget
    #     # self.window.add_widget(Image(source="logo.png"))
    #
    #     # label widget
    #     self.greeting = Label(
    #                     text= "What's your name?",
    #                     font_size= 10,
    #                     color= '#00FFCE'
    #                     )
    #     self.window.add_widget(self.greeting)
    #
    #     # text input widget
    #     self.user = TextInput(
    #                 multiline= False,
    #                 padding_y= (20,20),
    #                 size_hint= (1, 0.5)
    #                 )
    #
    #     self.window.add_widget(self.user)
    #
    #     # button widget
    #     self.button = Button(
    #                   text= "GREET",
    #                   size_hint= (1,0.5),
    #                   bold= True,
    #                   background_color ='#00FFCE',
    #                   #remove darker overlay of background colour
    #                   # background_normal = ""
    #                   )
    #     self.button.bind(on_press=self.callback)
    #     self.window.add_widget(self.button)
    #
    #     return self.window
    #
    # def callback(self, instance):
    #     # change label text to "Hello + user name!"
    #     self.greeting.text = "Hello " + self.user.text + "!"

    def build(self):
        return MyGrid()

    def store_values(self):
        injector_hole_diam = float(self.root.ids.injector_hole_diam.text)
        injector_hole_num = float(self.root.ids.injector_holes_num.text)
        k_loss = float(self.root.ids.K_loss.text)
        inj = Injector(injector_hole_num, injector_hole_diam, k_loss)



        throat_diam = float(self.root.ids.throat_diameter.text)
        exit_diam = float(self.root.ids.exit_diameter.text)
        nozzle = Nozzle(exit_diam,throat_diam)

        fuel_len = float(self.root.ids.fuel_length.text)
        fuel_port_diam = float(self.root.ids.fuel_port_diameter.text)
        fuel_dens = float(self.root.ids.fuel_density.text)
        fuel_a = float(self.root.ids.fuel_a.text)
        fuel_n = float(self.root.ids.fuel_n.text)
        fuel_name = self.root.ids.fuel_name.text
        fuel_formula = self.root.ids.fuel_formula.text
        fuel_enth = float(self.root.ids.fuel_enth.text)
        fuel_temp = float(self.root.ids.fuel_temp.text)

        fuel = Fuel(fuel_temp, fuel_enth, fuel_name, fuel_formula, fuel_port_diam, fuel_len, fuel_dens, Ballistic(fuel_a, fuel_n))

        oxid_name = self.root.ids.oxid_name.text
        oxid_formula = self.root.ids.oxid_formula.text
        oxid_enth = float(self.root.ids.oxid_enth.text)
        oxid_temp = float(self.root.ids.oxid_temp.text)
        oxid = Oxidizer(oxid_temp, oxid_enth, oxid_name, oxid_formula)

        vessel_press = float(self.root.ids.vessel_press.text)
        vessel_vol = float(self.root.ids.vessel_vol.text) / 1000
        oxid_mass = float(self.root.ids.oxid_mass.text)
        ves = Vessel(vessel_press, vessel_vol, oxid_mass)

        engine = Engine(ves, inj, nozzle, fuel, oxid)
        data = engine.run(float(self.root.ids.time.text))

        import csv
        with open('../../Thrust.txt') as f:
            reader = csv.DictReader(f)
            t = []
            val = []
            for row in reader:
                t.append(float(row['Timestamp']))
                val.append(float(row['Value']))
                if float(row['Timestamp']) > 10:
                    break
                # print(row['Timestamp'], row['Value'])
            plt.plot(data['time'], data['thrust'],t, val )
            plt.show()

        # plt.plot(data['time'], data['pressure_combustion'])
        # plt.show()
        # print(1)
        # ves = Vessel(60, 0.015, 10)
        # nozzle = Nozzle(72, 33)
        # inj = Injector(36, 1.5, 4.2)
        # b = Ballistic(0.00772597539149796, 0.777265794840152)
        # fuel = Fuel(300, 67.69, 'nyl', 'C 6.0   H 11.0   O 1.0  N 1.0', 61, 1000, 1130, b)
        # oxid = Oxidizer(300, 75.24, 'nitrous', 'N 2 O 1')
        # engine = Engine(ves, inj, nozzle, fuel, oxid)
        # # start_time = time.time()
        # data = engine.run()
        # # print("--- %s seconds ---" % (time.time() - start_time))
        # plt.plot(data['time'], data['pressure_combustion'])
        # plt.show()






# run Say Hello App Calss
# if __name__ == "__main__":
#     SayHello().run()

if __name__ == "__main__":
    MyApp().run()