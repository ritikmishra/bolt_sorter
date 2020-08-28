bolt_sorter
===========

*Note: This project is on hold for the duration of the pandemic as the hardware/electronics this software is supposed to run on is stuck in a university lab that is closed for the duration of the pandemic*

A Python 3.6.8 to control a double-jointed arm on a turret to (hopefully!) sort bolts by thread 
pitch and outer diameter. 



[![a black line and a red line represent the double-jointed arm. they move around and stuff.](https://i.imgur.com/o0BvekX.png "a screenshot from the simulator. just the double jointed arm, no turret")](https://youtu.be/3xcRSK5T1yQ)

#### some info 
- `stepper_motor`
    - contains code that directly interfaces with the stepper motor
    - describes a simulated stepper motor!
- `superstructure.py`
    - contains kinematics stuff
- `units.py`
    - custom types for type hinting
- `utils.py`
    - common funcs e.g angle bounding
- `visualizer.py`
    - click the picture above to see what it does!
