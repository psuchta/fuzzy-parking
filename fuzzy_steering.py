import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class FuzzySteering:
  def __init__(self):
    self.steering_ctrl = self.init_fuzzy_logic()

  def init_fuzzy_logic(self):
    xa = ctrl.Antecedent(np.arange(-0.5, 9, 0.01), 'xa')
    ya = ctrl.Antecedent(np.arange(-0.3, 9, 0.01), 'ya')
    angle = ctrl.Antecedent(np.arange(-44.6, 121, 0.01), 'angle')
    steering = ctrl.Consequent(np.arange(-35, 37.38, 0.01), 'steering')

    # Custom membership functions 
    xa['S'] = fuzz.trimf(xa.universe, [-0.23, 0.20, 0.57])
    xa['B'] = fuzz.trimf(xa.universe, [0.4, 0.7, 1])
    xa['P'] = fuzz.trimf(xa.universe, [0.93, 1.47, 1.92])
    xa['PB'] = fuzz.trapmf(xa.universe, [1.74, 2.14, 9, 9])
    # xa.view()
    # plt.show()
    ya['S'] = fuzz.trimf(ya.universe, [-0.3, 0.4, 1.21])
    ya['B'] = fuzz.trimf(ya.universe, [0.94, 1.65, 2.24])
    ya['PM'] = fuzz.trimf(ya.universe, [2.18, 2.52, 2.75])
    ya['PB'] = fuzz.trapmf(ya.universe, [2.75, 3.23, 9, 9])
    # ya.view()
    # plt.show()
    angle['N'] = fuzz.trapmf(angle.universe, [-44.6, -27.6, -17.6, -2.3])
    angle['Z'] = fuzz.trimf(angle.universe, [-4.46, 0, 2.03])
    angle['P'] = fuzz.trapmf(angle.universe, [0.11, 7.37, 56.3, 91])
    angle['PM'] = fuzz.trimf(angle.universe, [88, 90, 93.2])
    angle['PB'] = fuzz.trapmf(angle.universe, [92.45, 97, 120, 120])
    # angle.view()
    # plt.show()
    steering['NB'] = fuzz.trimf(steering.universe, [-35, -32.14, -29.15])
    steering['NM'] = fuzz.trimf(steering.universe, [-29.77, -20.43, -11.09])
    steering['N'] = fuzz.trimf(steering.universe, [-20.43, -11.71, -2.87])
    steering['Z'] = fuzz.trimf(steering.universe, [-3.85, 0, 4.12])
    steering['P'] = fuzz.trimf(steering.universe, [2.87, 11.71, 20.43])
    steering['PM'] = fuzz.trimf(steering.universe, [4.98, 14.95, 24.91])
    steering['PB'] = fuzz.trapmf(steering.universe, [23.67, 26.16, 37.37, 37.37])
    # steering.view()
    # plt.show()

    # When xa is S
    rule1 = ctrl.Rule(xa['S'] & ya['S'] & angle['P'], steering['NB'])
    rule2 = ctrl.Rule(xa['S'] & ya['B'] & angle['P'], steering['NB'])
    rule21 = ctrl.Rule(xa['S'] & ya['B'] & angle['PM'], steering['Z'])
    rule22 = ctrl.Rule(xa['S'] & ya['B'] & angle['PB'], steering['P'])
    rule3 = ctrl.Rule(xa['S'] & ya['S'] & angle['PM'], steering['Z'])

    # When xa is B
    rule4 = ctrl.Rule(xa['B'] & ya['B'] & angle['P'], steering['NB'])
    rule41 = ctrl.Rule(xa['B'] & ya['S'] & angle['PM'], steering['Z'])
    rule42 = ctrl.Rule(xa['B'] & ya['B'] & angle['PM'], steering['Z'])

    # When xa is P
    rule5 = ctrl.Rule(xa['P'] & ya['B'] & angle['Z'], steering['NM'])
    rule6 = ctrl.Rule(xa['P'] & ya['B'] & angle['P'], steering['NM'])

    # When xa is PB
    rule7 = ctrl.Rule(xa['PB'] & ya['B'] & angle['N'], steering['NB'])
    rule8 = ctrl.Rule(xa['PB'] & ya['B'] & angle['Z'], steering['Z'])
    rule9 = ctrl.Rule(xa['PB'] & ya['B'] & angle['P'], steering['PB'])
    # rule1.view()
    # plt.show()
    steering_ctrl = ctrl.ControlSystem(
      [
        rule1,
        rule2,
        rule21,
        rule3,
        rule4,
        rule41,
        rule42,
        rule5,
        rule6,
        rule7,
        rule8,
        rule9
      ]
    )
    return ctrl.ControlSystemSimulation(steering_ctrl)

  def get_steering(self, xa_input, ya_input, angle_input):

    print('xa ', xa_input)
    print('ya ', ya_input)
    print('angle ', -angle_input)

    xa_input = round(xa_input, 2)
    ya_input = round(ya_input, 2)
    angle_input = round(angle_input, 2)

    self.steering_ctrl.input['xa'] = xa_input
    self.steering_ctrl.input['ya'] = ya_input
    self.steering_ctrl.input['angle'] = -angle_input

    # # Crunch the numbers
    self.steering_ctrl.compute()
    return -self.steering_ctrl.output['steering']
