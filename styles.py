####################################################

# MIT License

# Copyright (c) 2023 HeshamMoawad

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Contact Me 
# GitHub : github.com/HeshamMoawad
# Gmail : HeshamMoawad120120@gmail.com
# Whatsapp : +201111141853

####################################################


class Styles():

    

    @property
    def main(self):
        return self.Widget.Normal +self.Label.Normal+ self.LineEdit.Normal + self.ComboBox.Normal + self.SpinBox.Normal + self.PushButton.Normal + self.GroupBox.Normal + self.Frame.Normal

    class Colors():
        Orange = "rgb(255, 112, 16)"
        DarkOrangeToggle = "#ff7010"

    class Backgrounds():
        Transparent = f"background-color:transparent;"
        Orange = "background-color:rgb(255, 112, 16);color:black;"
        DarkOrange = """background-color: black;color:white;"""
        LineEdit = """"background-color:gray;color:black;"""

    class AnimationToggle():
        Orange = ''
    
    class LineEdit():
        Normal = """
        QLineEdit{
            font:14px;
            border-radius:4px;
            background-color:white;
            color:black;
            
        }
        """

    class Label():
        Normal = """        
        QLabel{
            background-color:transparent;
        }  
        """
    class Widget():
        Normal = """
        QWidget{
            font:14px;
            color:white;
            background-color:qlineargradient(spread:pad, x1:0.977273, y1:0.755, x2:0, y2:0.365, stop:0 rgba(7, 6, 5, 210), stop:1 rgba(124, 14, 122, 228));
        }
        """
    class ComboBox():
        Normal = """
        QComboBox{
            border-radius:4px;
            background-color:white;
            color:black;
        }
        
        
        """
    class SpinBox():
        Normal = """
        
        QSpinBox{
            background-color:white;
            border-radius:4px;
            color:black;
        }
        """

    class GroupBox():
        Normal = """
        QGroupBox{
            border:2px;
            border-radius:2px;
            background-color:transparent;
        }
        """

    class PushButton():
        Normal = """
        QToolButton{
            background-color:transparent;
            border-radius:6px;
        }
        QToolButton:hover{
            background-color:darkgray;
            color:black;
        }
        QPushButton{
            background-color:transparent;
            border-radius:6px;
        }
        QPushButton:hover{
            background-color:darkgray;
            color:black;
        }
        
        """
    class Frame():
        Normal = """
        MyQFrame{
            background-color:transparent;
        }
        QFrame{
            background-color:transparent;
        }
        """
    class TreeWidget():
        Normal = """
        MyQTreeWidget{
            color:black;
            background-color:white;
        }
        MyQTreeWidget QHeaderView{
            color:black;
            background-color:white;
        }
        """











    Button = """
    MyQToolButton{
        background-color:transparent;
        border-radius:6px;
    };

    """
