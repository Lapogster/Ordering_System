# LaPizzaO'Sei Ordering System
# A program that will allow customers to place orders and send orders to the kitchen
# Written by Luca Pograri

# --- GLOBAL VARIABLES --- #                                                                                                                                                            #Comments about each important line/section
# - INTERNAL DATA - #
stock = {}                                                                                                                                                                              #Global Variable used to internally track stock

latestOrder = 0                                                                                                                                                                         #Global Variable that tracks the order number of the most recent order
fileLatestOrder = 0                                                                                                                                                                     #Global variable to track the order number currently recorded in the save file

tableNumber = 0                                                                                                                                                                         #Global variable of the current table number

currentMenuItems = []                                                                                                                                                                   #Global variable to track all items available on the menu
currentMenuObjects = []                                                                                                                                                                 #Global variable to track Menu Item class instances for all items on menu
currentMenuCategories = []                                                                                                                                                              #Global variable to track all menu categories

userOrder = ""                                                                                                                                                                          #Creating a blank version of variable that will be used to store current order instance
currentOrder = ["blank"]                                                                                                                                                                #Global variable to store  all items in the current order
pastOrders = []                                                                                                                                                                         #Stores old order instances

fileSelfSync = False                                                                                                                                                                    #Stores if internal data is confirmed to be up-to-date with file

# - EXTERNAL DATA SETTINGS - #
stockFilePath = "Saved_Data.xml"                                                                                                                                                        #Stores name of file to read/write save data to and from
stockFileEncoding = "UTF-8"                                                                                                                                                             #Encoding type of the file used

# --- CLASSES --- #
#Class for managing data import/saving
class dataManagement():
    #Initiating the class
    def __init__(self, FilePath, encoding):                                                                                                                                             #Initialising data management object and setting local variables pointing to the file in use
        self.stockFilePath = FilePath
        self.stockEncoding = encoding
    
    # - IMPORTING EXTERNAL DATA - #
    #Import stock data from file
    def updateInternalStock(self):                                                                                                                                                      #reading the xml file to import all stock data
        stockFileOver = False
        midThroughItem = False
        self.stockFile = open(file=self.stockFilePath, encoding=self.stockEncoding)
        for line in self.stockFile:                                                                                                                                                     #Reading each line in the xml file for relevant data to save internally as stock
            if stockFileOver == False:
                line = line.strip()
                if midThroughItem == True:
                    if "<quantity" in line:
                        elementStartQ = line.find("<quantity")
                        startQ = line.find(">", int(elementStartQ))
                        endQ = line.find("<", int(startQ) + 1)

                        stockNum = line[startQ + 1:endQ]
                        stock[stockItem] = stockNum

                        midThroughItem = False
                    else:
                        print("ERROR: Failed to read " + stockItem + "'s quantity.")
                        midThroughItem = False 
                else:
                    if "<name" in line:
                        elementStart = line.find("<name")
                        start = line.find(">", int(elementStart))
                        end = line.find("<", int(start) + 1)

                        stockItem = line[start + 1:end]

                        midThroughItem = True
                if "</stock>" in line:
                    stockFileOver = True
        self.stockFile.close()
        stockFileOver = False                                                                                                                                                           #Resetting stockfileover to allow future uses of function
        
    #import latest order number from file
    def updateInternalOrderCount(self):
        self.stockFile = open(file=self.stockFilePath, encoding=self.stockEncoding)
        for line in self.stockFile:                                                                                                                                                     #reading each line in xml file to identify the saved latest order number
            line = line.strip()
            if "latest_order>" in line:
                elementStart = line.find("latest_order")
                start = line.find(">", int(elementStart))
                end = line.find("<", int(start))
    
                global latestOrder
                latestOrder = int(str(line[start + 1:end]))
        self.stockFile.close()
        global fileSelfSync
        if fileSelfSync == False:                                                                                                                                                       #Syncing order number with file
            global fileLatestOrder
            fileLatestOrder = latestOrder
            fileSelfSync = True
    
    #import all available menu items from file
    def importMenuItems(self):                                                                                                                                                          #Importing all menu items from xml file
        importingMenu = False
        readingItem = False
        self.stockFile = open(file=self.stockFilePath, encoding=self.stockEncoding)
        for line in self.stockFile:                                                                                                                                                     #Reading each line in the xml file to search for relbamt data and store each item 
            line = line.strip()
            if importingMenu == True:
                if "<item>" in line:
                    readingItem = True
            if readingItem == True:
                if "<name>" in line:
                    elementStart = line.find("<name")
                    start = line.find(">", int(elementStart))
                    end = line.find("<", int(start) + 1)

                    itemName = line[int(start) + 1:end]

                    global currentMenuItems
                    currentMenuItems.append(itemName)

                    readingItem = False
            if "<menu_items>" in line:
                importingMenu = True
            elif "</menu_items>" in line:
                importingMenu = False
            if "<category>" in line:
                elementStart = line.find("<category")
                start = line.find(">", int(elementStart))
                end = line.find("<", int(start) + 1)

                menuCategory = line[int(start) + 1:end]

                global currentMenuCategories
                if menuCategory not in currentMenuCategories:
                    currentMenuCategories.append(menuCategory)
        self.stockFile.close()

        self.updateMenuObjects()

    # - EXPORTING INTERNAL DATA - #
    #update stock saved in file
    def updateExternalStock(self):                                                                                                                                                      #updating stock data within the file to the stock saved locally
        newStockXML = ""                                                                                                                                                                #variables to handle writing data
        originalXMLPreStock = ""
        originalXMLPostStock = ""
        itemsLen = ""
        itemsInStock = []
        newStockFile = ""

        for x in stock:
            itemsInStock.append(x)

        self.stockFile = open(self.stockFilePath, 'r')
        readingRelevant = True
        for line in self.stockFile:                                                                                                                                                     #Saving old xml file sections that aren't affected by changes
            if readingRelevant == True:
                if "<stock>" in line:
                    readingRelevant = False
                else:
                    originalXMLPreStock += line
        self.stockFile.close()

        self.stockFile = open(self.stockFilePath, 'r')
        readingRelevant = False
        for line in self.stockFile:                                                                                                                                                     #Saving old xml file sections that aren't affected by changes
            if readingRelevant == True:
                originalXMLPostStock += line
            else:
                if "</stock>" in line:
                    readingRelevant = True
        self.stockFile.close()

        newStockXML += '\t' + "<stock>" + '\n'
        itemsLen = len(stock)
        i = 0
        while i < itemsLen:                                                                                                                                                             #Writing new stock data to xml file
            i += 1
            
            newStockXML += '\t' + '\t' + "<item>" + '\n'
            newStockXML += '\t' + '\t' + '\t' + "<name>" + itemsInStock[i - 1] + "</name>" + '\n'
            newStockXML += '\t' + '\t' + '\t' + "<quantity>" + str(stock[itemsInStock[i - 1]]) + "</quantity>" + '\n'
            newStockXML += '\t' + '\t' + "</item>" + '\n'

        newStockXML += '\t' + "</stock>" + '\n'

        newStockFile += originalXMLPreStock + newStockXML + originalXMLPostStock

        self.stockFile = open(self.stockFilePath, "w")
        self.stockFile.write(newStockFile)
        self.stockFile.close()

    #update latest order number in file
    def updateExternalOrderCount(self):                                                                                                                                                 #Updating the order number stored in the file
        self.stockFile = open(self.stockFilePath, 'r')
        currentstr = ""
        for line in self.stockFile:                                                                                                                                                     #saving string of copy of xml file in entirity
            currentstr += line
            
        currentstr = currentstr.replace( '\t'+'\t'+"<latest_order>" + f"{fileLatestOrder}" + "</latest_order>", '\t'+'\t'+"<latest_order>" + str(latestOrder) + "</latest_order>")      #Replacing part of copy of xml file with new updated data
        
        self.stockFile.close()
        self.stockFile = open(self.stockFilePath, "w")                                                                                                                                  #Writing updated data to xml file
        self.stockFile.write(currentstr)

        self.stockFile.close()

    #Setting This Device's Table Number
    def setTableNumber(self, table):                                                                                                                                                    #Changing table number of device to specified number
        global tableNumber
        tableNumber = table

    # - UPDATING INTERNAL STORAGE/SETTINGS - #
    def updateMenuObjects(self):                                                                                                                                                        #creates a menu item class instance for every item on the menu
        global currentMenuItems
        global currentMenuObjects

        for x in currentMenuItems:
            x = menuItem(x, self.stockFilePath, self.stockEncoding)
            currentMenuObjects.append(x)

    #next 3 functions allow admin with cmd access to change the file the program reads
    def reloadFilePath(self):
        global stockFilePath
        global stockFileEncoding

        self.__init__(stockFilePath, stockFileEncoding)

    def updateFilePath(self):
        global stockFilePath
        stockFilePath = input("Please enter the new file path: " + '\n')

        self.reloadFilePath()

    def updateFileEncoding(self):
        global stockFileEncoding
        stockFileEncoding = input("Please enter the new file path: " + '\n')

        self.reloadFilePath()

#Class to define properties of any item available on the menu
class menuItem():
    #Initiating the Class
    def __init__(self, name, stockFilePath, encoding):                                                                                                                                  #Initialising a menu item object that will define what is available on the menu
        self.stockFilePath = stockFilePath
        self.stockEncoding = encoding

        self.name = name                                                                                                                                                                #Setting name of menu item
        self.ingredients = {}                                                                                                                                                           #Creating varaible to store required ingredients
        self.category = ""                                                                                                                                                              #Creating variable to store which category this item falls into
        self.price = 0.0                                                                                                                                                                #Creating variable to store price of item

        lookingInMenu = False                                                                                                                                                           #Creating booleans that will be ised yo define which part of the xml file is currently being read
        lookingAtSelf = False
        lookingAtIngredients = False
        midThroughIngredient = False

        self.stockFile = open(file=self.stockFilePath, encoding=self.stockEncoding)
        for line in self.stockFile:                                                                                                                                                     #Reading each line in the xml file for relevant sections and importing any relevant data to previously created variables
            if "<menu_items>" in line:
                lookingInMenu = True
            if lookingInMenu == True:
                if f"<name>{self.name}<" in line:
                    lookingAtSelf = True
            if lookingAtSelf == True:
                if "<ingredients>" in line:
                    lookingAtIngredients = True
                if "<category>" in line:
                    elementStart = line.find("<category>")
                    start = line.find(">", int(elementStart))
                    end = line.find("<", int(start) + 1)

                    self.category = line[start + 1:end]
                if "<price>" in line:
                    elementStart = line.find("<price")
                    start = line.find(">", int(elementStart))
                    end = line.find("<", int(start) + 1)

                    self.price = line[start + 1:end]
            if lookingAtIngredients == True:
                if midThroughIngredient == True:
                    if "<quantity_required>" in line:
                        elementStart = line.find("<quantity_required")
                        start = line.find(">", int(elementStart))
                        end = line.find("<", int(start) + 1)

                        ingredientQuantity = line[start + 1:end]
                        self.ingredients[ingredientName] = ingredientQuantity

                        midThroughIngredient = False
                    else:
                        print("ERROR: Failed to read " + ingredientName + "'s quantity.")
                        midThroughIngredient = False
                else:
                    if "<name>" in line:
                        elementStart = line.find("<name")
                        start = line.find(">", int(elementStart))
                        end = line.find("<", int(start) + 1)

                        ingredientName = line[start + 1:end]

                        midThroughIngredient = True
                if "</ingredients>" in line:
                    lookingAtIngredients = False
            if "</menu_items>" in line:
                lookingInMenu = False
            if "</item>" in line:
                lookingAtSelf = False
        self.stockFile.close()

    #Identify each menu item and their unique properties - used for testing purposes
    def identify(self):                                                                                                                                                                 #function used for testing that will output all information about a menu item object for debugging
        print("Name of Item: ")
        print(self.name)

        print("Category of Item: ")
        print(self.category)

        print("Ingredients Required: ")
        print(self.ingredients)

        print("Price of Item: ")
        print("$" + self.price)

#Class to define the properties of an order
class Order():
    #Initiating Class
    def __init__(self, table):                                                                                                                                                          #Initialising a blank order and coresponding table number
        global latestOrder
        self.orderNumber = int(latestOrder) + 1
        latestOrder += 1
        self.currentOrder = []
    
    #Identify the current order information and items ordered - used for testing purposes
    def identify(self):                                                                                                                                                                 #Function used for testing that will output all information about an order object for debugging
        print("Order Number -> " + str(self.orderNumber))
        print("Table number " + str(tableNumber))
        print()
        print("Items Ordered: ")
        for x in self.currentOrder:
            x.identify()
            print()

    #Add an item from the menu into the current order
    def addItem(self, item):                                                                                                                                                            #Adds specified item to order
        self.currentOrder.append(item)

    def removeItem(self):                                                                                                                                                               #Removes most recent item ordered
        print("Removed " + self.currentOrder[len(self.currentOrder) - 1].name + "from order")
        self.currentOrder.pop()
    
    #Process the current order's price and deduct stock from current stock
    def processOrder(self):                                                                                                                                                             #Processes current order by removing unavailable items and providing final order + price
        overallPrice = 0.0                                                                                                                                                              #Determins the total pricxe of all selected items
        for x in self.currentOrder:
            overallPrice += float(x.price)

        print()
        print("Price = $" + str(overallPrice))                                                                                                                                          #Outputs total price of selected items

        self.currentOrderNames = []                                                                                                                                                     #Creates a list of the names of each item selected
        for x in self.currentOrder:
            self.currentOrderNames.append(x.name)

        print("You ordered - " + str(self.currentOrderNames))                                                                                                                           #Outputs the name of each item selected

        global stock
        print("Original Stock - " + str(stock))                                                                                                                                         #Outputs the stock available proor to the current order making changes
        newStock = stock                                                                                                                                                                #creating a duplicate of available stock info
        i = 0                                                                                                                                                                           #Setting a counter to track items being processed
        itemsProcessed = []
        for x in self.currentOrder:                                                                                                                                                     #Checking each item ordered, if there is enough stock, the item will be added to the processed list, if not, the item will be removed
            ingredientsRequired = {

            }

            ingredientsRequired.update(x.ingredients)
            n = 0
            for y in ingredientsRequired:
                n += 1

            for y in ingredientsRequired:
                if int(ingredientsRequired[y]) > int(newStock[y]):
                    print("Insufficient stock for " + y)                                                                                                                                #Outputs which items are unavailable due to lack of stock
                    #self.currentOrder.pop(i)
                    #self.currentOrderNames.pop(i)
                    #missingStock = True
                    #missingStockPos = i
                    #missingStockItems.append(missingStockPos)
                    break
                else:
                    newAmount = int(newStock[y]) - int(ingredientsRequired[y])
                    newStock[y] = newAmount
                    if n == 1:
                        itemsProcessed.append(self.currentOrder[i])
                    n += -1
            
            i += 1

        itemsProcessedNames = []                                                                                                                                                        #creating a list of the names of each item succesfully processed
        for x in itemsProcessed:
            itemsProcessedNames.append(x.name)

        overallPrice = 0.0                                                                                                                                                              #Calculating total final price of order
        for x in itemsProcessed:
            overallPrice += float(x.price)

        stock = newStock
        print("New Stock - " + str(stock))                                                                                                                                              #Outputs updated stock with ordered items deducted from the original stock
        print()

        print("Items Processed - " + str(itemsProcessedNames))                                                                                                                          #Outputs list of items processed names and final price
        print("Final Price - " + str(overallPrice))

#Creating the manager that will load/save data
stockData = dataManagement(stockFilePath, stockFileEncoding)                                                                                                                            #Creating the object instance that will store data and manage local data, as well as data read/write from file

#Calling Initial Stock Data Import - calling functions that will import current stock, latest order count and available menu items from file
stockData.updateInternalStock()
stockData.updateInternalOrderCount()
stockData.importMenuItems()

#Create a new blank order
def createOrder():                                                                                                                                                                      #Creates a new empty order instance that will now be used as the current order - saves old order to archive array
    global userOrder
    if not userOrder == "":
        pastOrders.append(userOrder)
    #Creating the Order
    userOrder = Order(tableNumber)
    currentOrder.pop()
    currentOrder.append(userOrder)

# --- TESTING --- #
#function that will test most vital elements of program's functionality and report results - used for testing
def runTest():
    print(tableNumber)

    print()
    print(stock)
    print(currentMenuItems)
    print(currentMenuObjects)
    print(currentMenuCategories)
    print()

    for x in currentMenuObjects:
        x.identify()
        print()

    print(latestOrder)
    print()

    if not userOrder == "":
        print("Current Order:")
        print(userOrder.currentOrder)
        print()

    if not pastOrders == []:
        print("All previous orders: ")
        print(pastOrders)
        print()

# --- CMD COMMANDS --- #
# - used for testing - #
cmdAvailable = False #<-- ENABLE FOR DEBUGGING AND TERMINAL COMMAND FUNCTIONALITY
while cmdAvailable == True:
    cmdInput = input()                                                                                                                                                                  #Saves cmd input to read and detemine action

    if "sd." in cmdInput:
        if ".tablenum " in cmdInput:
            newTableNumPos = cmdInput.find("tablenum ")
            newTableNum = cmdInput[newTableNumPos + 9: newTableNumPos + 20]

            stockData.setTableNumber(newTableNum)
            print("Table number changed to " + tableNumber)
        if ".importstock" in cmdInput:
            stockData.updateInternalStock()
        if ".importoc" in cmdInput:
            stockData.updateInternalOrderCount()
        if ".updatemenu" in cmdInput:
            currentMenuItems = []
            currentMenuObjects = []
            currentMenuCategories = []
            stockData.importMenuItems()
        if ".updateordernum" in cmdInput:
            stockData.updateExternalOrderCount()
            fileSelfSync = False
            stockData.updateInternalOrderCount()
        if ".updatestock" in cmdInput:
            stockData.updateExternalStock()
    if "tst." in cmdInput:
        if ".fulltest" in cmdInput:
            runTest()
    if "oi." in cmdInput:
        if ".view" in cmdInput:
            if not userOrder == "":
                userOrder.identify()
            else:
                print("No order to display")
        if ".create" in cmdInput:
            createOrder()
        if ".add" in cmdInput:
            if cmdInput == "oi.add":
                print("Missing item to add")
            else:
                if not userOrder == "":
                    itemToAddPos = cmdInput.find(".add ")
                    itemToAdd = cmdInput[itemToAddPos + 5: itemToAddPos + 20]
                    print("Adding " + currentMenuItems[int(itemToAdd)] + " to order.")

                    userOrder.addItem(currentMenuObjects[int(itemToAdd)])
                else:
                    print("There is no order currently in use.")
        if ".remove" in cmdInput:
            userOrder.removeItem()
        if ".process" in cmdInput:
            if not userOrder == "":
                userOrder.processOrder()
            else:
                print("Nothing to print.")
    if "cmd." in cmdInput:
        if ".n" in cmdInput:
            print()
    if "app." in cmdInput:
        if ".end" in cmdInput:
            cmdAvailable = False
            break