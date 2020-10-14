# Tricopter
The goal of this project it to build a tricopter which can fly around and then land on a persons shoulder and hook onto a shoulder pad.

So far I am still working on the flight control system to allow the drone to hover in one place.

![Current build](/firstIteration1.jpg | width=50%) ![Current build](/firstIteration2.jpg | width=50%)

## Progress
- [x] Research tricopters, types of batteries, types of motors, how to use ESC's
- [x] Select and buy parts
- [x] Create AutoCAD drawing of the frame
- [x] Laser cut frame
- [x] Solder all components together
- [x] Assemble frome and add components
- [x] Ensure the raspberry pi can run on the stand-alone power from the Li-Po battery 
- [X] Ensure the motors can be controled with a python script running on the raspberry pi
- [x] Ensure the program can read the accelerometer data and adjust the motor speeds
- [x] Test motors at various speeds: can take off but then tilts and crashes
- [ ] Improve stability by upgrading the auto-balance thread and checking center of mass
- [ ] Add simple flight path, probably a circle
- [ ] Add hook, maybe controlled by a servo or just a static hook
- [ ] Program a take off sequence so it can take off while hooked onto someones shoulder
- [ ] Program a landing sequence so it can land on a shoulder hook
