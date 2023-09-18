# LaPizzaO'Sei Ordering System presentation
# A program that will create the visual presentation of the ordering system
# Written by Luca Pograri

#Imports
#Importing functions and classes from Order_System.py, which is the data and logic layers
from Order_System import runTest as tst
from Order_System import tableNumber as tableNum
from Order_System import currentMenuCategories as menuCategories
from Order_System import currentMenuObjects as menuObjects
from Order_System import menuItem
from Order_System import createOrder as newOrder
from Order_System import currentOrder as currentOrder
from Order_System import stockData as stockData

#Importing Kivy functionality classes
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App

#Importing Kivy behaviours, properties and functions
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleview import RecycleView

#Variables
itemsInCategory = []                                                                            #Global variables to store what items are in each category - unused in current version
instanceList = []                                                                               #list of instances to allow this program to call kivy created instances
appList = []                                                                                    #List of app instances to allow program to call kivy's app functions
inCategory = False                                                                              #Unused in current version
mainMenu = True                                                                                 #Stores if the current screen is the main menu - unused in current version

#Classes
class FrontScreen(Screen):                                                                      #Defines the opening frontscreen for Kivy to create
    currentTableNum = tableNum

    def start(self):                                                                            #Creates a new order
        newOrder()

class MainOrderMenu(Screen):                                                                    #Defines the main menu order screen for kivy to create
    def __init__(self, **kwargs):                                                               #Adding recognise self to kivy Screen's init function
        super(Screen, self).__init__(**kwargs)
        self.recogniseSelf()

    def FullTest(self, instance):                                                               #Test function for debugging
        tst()
        self.processOrder()

    def processOrder(self):                                                                     #Function that processes current order
        if len(currentOrder[0].currentOrder) < 1:                                               #Check to see if current order is empty before processing
            print("Order empty, order canceled")
        else:
            currentOrder[0].processOrder()

    def recogniseSelf(self):                                                                    #Adds instance to instance list to allow program to call it's functions
        instanceList.append(self)

    def removeItem(self):                                                                       #Removes item from current order - unused on this creen in current version
        currentOrder[0].removeItem()

class CategoryOrderMenu(Screen):                                                                #Defines the 'category order screen' - utilised as a full order screen in current version - for kivy to create
    def __init__(self, **kwargs):                                                               #Adding recognise self to kivy Screen's init function
        super(Screen, self).__init__(**kwargs)
        self.recogniseSelf()

    def recogniseSelf(self):                                                                    #Adds instance to instance list to allow program to call it's functions
        instanceList.append(self)

    def FullTest(self, instance):                                                               #Test function for debugging
        tst()
    
    def processOrder(self):                                                                     #Function that processes current order
        if len(currentOrder[0].currentOrder) < 1:                                               #Check to see if current order is empty before processing
            print("Order empty, order canceled")
        else:
            currentOrder[0].processOrder()

    def removeItem(self):                                                                       #Removes item from current order
        currentOrder[0].removeItem()

class MainMenu(Screen):                                                                         #Defining the main menu screen for kivy to create
    def FullTest(self, instance):                                                               #testing function for debugging
        tst()

    def processOrder(self):                                                                     #Function that processes current order
        if len(currentOrder[0].currentOrder) < 1:                                               #Check to see if current order is empty before processing
            print("Order empty, order canceled")
        else:
            currentOrder[0].processOrder()

class OrderComplete(Screen):                                                                    #Defining Order complete screen for kivy
    def updateStock(self):                                                                      #Updating external stock after order completed
        stockData.updateExternalStock()

class SelectableRecycleGridLayout(FocusBehavior,LayoutSelectionBehavior, RecycleGridLayout):    #defining kivy's selectable recycle view
    pass

class SelectableLabel(RecycleDataViewBehavior, Label):
    index = None                                                                                #Defining which object is being referenced and if it is selected
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):                                              #refreshing the recycle view list's labels
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):                                                             #Defining what happens when an object is touched within kivy
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)


    def apply_selection(self, rv, index, is_selected):                                          #defining what happens when the user selects an object
        self.selected = is_selected
        if is_selected:                                                                         #Adding selected item to order when item is selected
            for x in menuObjects:
                if "{'text': '" + x.category + "'}" == "{0}".format(rv.data[index]):
                    global itemsInCategory
                    itemsInCategory.append(x)
            global currentOrder
            currentOrder[0].addItem(menuObjects[index])
            print("[Order ] Added " + menuObjects[index].name + " to order")
        else:
            pass                                                                                #Doing nothing if an object is de-selected

class RV(RecycleView):                                                                          #Defining the properties of a recycle view list widget for kivy
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
        for x in menuObjects:                                                                   #Adding available menu objects to recycle view
            self.data.append({"text":x.name})

class WindowManager(ScreenManager):                                                             #Defining the window manager nkivy will use
    pass

#Loading Kivy design language
kv = Builder.load_file("Design.kv")                                                             #Creates the object that will build the app utilising the kivy design language file design.kv

class MainApp(App):                                                                             #defines the main app's build process for kivy
    def build(self):
        appList.append(self)

        return kv

#Starting the main app loop
if __name__ == "__main__":
    MainApp().run()