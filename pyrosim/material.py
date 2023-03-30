from pyrosim.commonFunctions import Save_Whitespace
import random

class MATERIAL: 

    def __init__(self, green, idx):

        self.depth  = 3

        if green == 1:
            randomRed = random.randint(1, 9)
            randomGreen = random.randint(1, 9)
            randomBlue = random.randint(1, 9)
            red = str(randomRed/10)
            greenC = str(randomGreen/10)
            blue = str(randomBlue/10)
            self.string1 = '<material name="a">'
            self.string2 = '    <color rgba="' + red + " " + greenC + " " + blue + " " + '0.95"/>'

        elif green == 2:
            randomRed = random.randint(1, 9)
            randomGreen = random.randint(1, 9)
            randomBlue = random.randint(1, 9)
            red = str(randomRed/10)
            greenC = str(randomGreen/10)
            blue = str(randomBlue/10)
            self.string1 = '<material name="b">'
            self.string2 = '    <color rgba="' + red + " " + greenC + " " + blue + " " + '0.95"/>'
            #self.string2 = '    <color rgba="0 0 1.0 1.0"/>'

        elif green == 3:
            randomRed = random.randint(1, 9)
            randomGreen = random.randint(1, 9)
            randomBlue = random.randint(1, 9)
            red = str(randomRed/10)
            greenC = str(randomGreen/10)
            blue = str(randomBlue/10)
            self.string1 = '<material name="c">'
            self.string2 = '    <color rgba="' + red + " " + greenC + " " + blue + " " + '0.95"/>'

        elif green == 4:
            randomRed = random.randint(1, 9)
            randomGreen = random.randint(1, 9)
            randomBlue = random.randint(1, 9)
            red = str(randomRed/10)
            greenC = str(randomGreen/10)
            blue = str(randomBlue/10)
            self.string1 = '<material name="d">'
            self.string2 = '    <color rgba="' + red + " " + greenC + " " + blue + " " + '0.95"/>'

        elif green == 5:
            randomRed = random.randint(1, 9)
            randomGreen = random.randint(1, 9)
            randomBlue = random.randint(1, 9)
            red = str(randomRed/10)
            greenC = str(randomGreen/10)
            blue = str(randomBlue/10)
            self.string1 = '<material name="e">'
            self.string2 = '    <color rgba="' + red + " " + greenC + " " + blue + " " + '0.95"/>'

        elif green == 6:
            randomRed = random.randint(1, 9)
            randomGreen = random.randint(1, 9)
            randomBlue = random.randint(1, 9)
            red = str(randomRed/10)
            greenC = str(randomGreen/10)
            blue = str(randomBlue/10)
            self.string1 = '<material name="f">'
            self.string2 = '    <color rgba="' + red + " " + greenC + " " + blue + " " + '0.95"/>'

        else:
            randomRed = random.randint(1, 9)
            randomGreen = random.randint(1, 9)
            randomBlue = random.randint(1, 9)
            red = str(randomRed/10)
            greenC = str(randomGreen/10)
            blue = str(randomBlue/10)
            self.string1 = '<material name="g">'
            self.string2 = '    <color rgba="' + red + " " + greenC + " " + blue + " " + '0.95"/>'


        self.string3 = '</material>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
