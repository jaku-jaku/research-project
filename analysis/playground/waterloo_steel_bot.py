# %%
import numpy as np
import roboticstoolbox as rtb
from roboticstoolbox.robot.ET import ET
from roboticstoolbox.robot.ETS import ETS
from roboticstoolbox.robot.ERobot import ERobot
from roboticstoolbox.robot.Link import Link

import spatialgeometry as sg
import spatialmath as sm

class Waterloo_steel(ERobot):
    """
    Create model of Waterloo Steel Mobile manipulator
    """

    def __init__(self):

        deg = np.pi / 180
        mm = 1e-3
        tool_offset = (103) * mm
        
        l, w, h = 0.409, 0.445, 0.127

        b0 = Link(ETS(ET.Rz()), name="base0", parent=None, qlim=[-1000, 1000])

        b1 = Link(ETS(ET.tx()), name="base1", parent=b0, qlim=[-1000, 1000])

        b2 = Link(ETS(ET.ty()), name="base2", parent=b1, qlim=[-1000, 1000])
        
        b2.geometry = sg.Cuboid(
            [l, w, h], base=sm.SE3(0, 0, h / 2), color=(163, 157, 134)
        )

        l0 = Link(ET.tx(0.139) * ET.tz(0.272) * ET.Rz(), name="wam_base", parent=b2)

        l1 = Link(ET.tz(0.346) * ET.Rx(), name="wam_shoulder_pitch", parent=l0)

        l2 = Link(ET.Rz(), name="wam_shoulder_yaw", parent=l1)

        l3 = Link(ET.tx(0.045) * ET.tz(0.55) * ET.Rx(), name="wam_elbow_pitch", parent=l2)
        
        l4 = Link(ET.tx(-0.045) * ET.tz(0.3) * ET.Rz(), name="wam_wrist_yaw", parent=l3)

        l5 = Link(ET.Rx(), name="wam_wrist_pitch", parent=l4)
        
        l6 = Link(ET.tz(0.06) * ET.Rz(), name="wam_palm_yaw", parent=l5)
        
        ee = Link(ET.tz(tool_offset), name="ee", parent=l6)

        elinks = [b0, b1, b2, l0, l1, l2, l3, l4, l5, l6, ee]

        super(Waterloo_steel, self).__init__(elinks, name="Waterloo_steel", manufacturer="UWaterloo")

        self.qr = np.zeros(3+7)
        self.qz = np.zeros(3+7)

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)



robot = Waterloo_steel()
print(robot)

qt = rtb.jtraj(robot.qz, [0,0,0,1.3,1.3,0,0,0,0,0], 50)
robot.plot(qt.q, backend="pyplot", movie="../output/waterloo_steel.gif")
# %%
