import cv2 as cv
import numpy as np
import random

# general parameters
width = 900
height = 600
n_trees = 30
ground_level = height-100

# blank image
bg = np.zeros((height, width, 3), dtype=np.uint8)

# draw background
cv.rectangle(bg,(width,0), (0, ground_level), (255, 255, 95), -1)
cv.rectangle(bg,(width,ground_level), (0, height), (70, 180, 75), -1)

# *****************************************************
class Tree:
    def __init__(self, image):
        self.img = image
        self.loc = int(np.random.choice(range(900), 1))
        self.ht = int(np.random.choice(range(200, 350), 1))
        self.radius = 50
        self.scale = np.random.choice(np.linspace(0.5, 2.5, num=8), 1)
    
    def generate_colours(self):
        green = (0, random.randint(130,200),0)
        light_green = (35, random.randint(200,250),35)
        brown = random.choice([(2,30,85), (5,55,120), (0,70,140)])
        return green, light_green, brown

    def draw(self):
        small_radius = int(self.radius*self.scale-20*self.scale)
        green, light_green, brown = self.generate_colours()

       # leafs - shadows
        cv.circle(self.img, (self.loc,ground_level-self.ht), int(self.radius*self.scale), green, -1)
        cv.circle(self.img, (self.loc-int(45*self.scale),ground_level-self.ht+small_radius), small_radius , green, -1)
        cv.circle(self.img, (self.loc+int(45*self.scale),ground_level-self.ht+small_radius), small_radius, green, -1)    
        
        # trunk
        cv.line(self.img, (self.loc,ground_level),(self.loc,ground_level-self.ht), brown, int(20*self.scale))
        cv.line(self.img, (self.loc,ground_level-self.ht+int(75*self.scale)),(self.loc+int(45*self.scale),ground_level-self.ht+small_radius), brown, int(5*self.scale))
        cv.line(self.img, (self.loc,ground_level-self.ht+int(75*self.scale)),(self.loc-int(45*self.scale),ground_level-self.ht+small_radius), brown, int(5*self.scale))
        
        # leafs - highlights
        cv.circle(self.img, (self.loc,ground_level-self.ht), int(self.radius*self.scale-10*self.scale), light_green, -1)
        cv.circle(self.img, (self.loc-int(45*self.scale),ground_level-self.ht+small_radius), small_radius-int(10*self.scale) , light_green, -1)
        cv.circle(self.img, (self.loc+int(45*self.scale),ground_level-self.ht+small_radius), small_radius-int(10*self.scale), light_green, -1)
        
        return self.img
# *****************************************************

#
# #sun
# cv.circle(img,(200,150), 60, (0, 255, 255), -1)
# cv.circle(img,(200,150), 75, (220, 255, 255), 10)

# # *** TREE 1 ***
# #tree stem
# #tree leafs
# triangle2 = np.array([[640,460],[780,460], [710,200]], dtype=np.int32)
# cv.fillPoly(img, [triangle2], (75,180,70))

# # *** TREE 2 ***
# #tree stem
# cv.line(img, (600, 500), (600, 420), (30,65,155), 25)
# #tree leafs
# triangle = np.array([[500,440],[700,440], [600,75]], dtype=np.int32)
# cv.fillPoly(img, [triangle], (75,200,70))

# #text
# font = cv.FONT_HERSHEY_SCRIPT_SIMPLEX
# cv.putText(img, "I Love Python", (120,490), font, 1.5, (255, 255, 255), 2)

# cv.imwrite("tree.png", img)

# display image
for i in range(n_trees):
    img = Tree(bg).draw()

cv.imshow("forest of objects", img)

cv.waitKey(0)
cv.destroyAllWindows()