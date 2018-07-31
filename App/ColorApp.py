from tkinter import *
import re
import os
from tkcolorpicker import askcolor
import xml.etree.ElementTree as ET
from tkinter.filedialog import *

######   -> PalettePicker Version 1.0

#############################"TODO"###############
#
#   -> add tabs '(multiples charts)'
#   -> add shorcuts (ctrl z/n/o/y ...)
#   -> add Custom colorChooser
#	-> add export as svg/png
#
#
#################################################

###############################################
#Pipette icon made by : epiccoders
###############################################
ClipBoardColor = "#00000000"
BaseColors = ["#000000", "#111111","#222222", "#333333","#555555"]
GrayscaleColors = ["#000000", "#111111","#222222", "#333333","#444444","#555555", "#666666","#777777", "#888888", "#999999", "#AAAAAA", "#BBBBBB", "#CCCCCC", "#DDDDDD", "#EEEEEE", "#FFFFFF"]

IconList = ["tools","open","save","openrecent","export"]
IconListImage = ["","","","",""]
TempPic = ["","","","",""]
GuiColor = "#2b2f37"

FilePath = [""]
CurrentFileId = 0
FileContent = ["<issou></issou>","",""]
# set clipboard data
j=0

def getColor():
    color = askcolor()
    print (color)

# get clipboard data

########Init Vars

#master GUI
MG_width = 650
MG_height = 350
SidePannel_width = 35
ClipBoardRect_width = 25
IcButton_width = 32
padxIcButton = 2
SidePannel_width = IcButton_width - (padxIcButton*2)
CanvaDisplay_width = MG_width - SidePannel_width

nbGSColors = 5
nbBCColors = 7
def ButtonCommand(Command):
    print(Command)
    if (Command == "open"):
        name = askopenfilename(initialdir=os.path.expanduser("~/Desktop"),
                                   filetypes =(("Xml File", "*.xml"),("Klr File","*.klr")),
                                   title = "Choose the file to open."
                                   )
        FileOpen(name)
    elif (Command == "save"):
        if FilePath[CurrentFileId] == "":
            FilePath[CurrentFileId] = asksaveasfilename(initialdir=os.path.expanduser("~/Desktop"),
                                        defaultextension = ".xml",
                                        filetypes = (("Klr File","*.klr"),("All Files", "*.*")),
                                        title = "Chose the Emplacement and Name of your file."
                                        )
            FileSave(FilePath[CurrentFileId],'','')
    else:
        print("No function is connected to this Button")

def FileSave(FilePath,Colors,GScolors):

    Root = ET.Element("data")
    Klrs = ET.SubElement(Root, "Colors")
    GsKlrs = ET.SubElement(Root, "GSColors")

    for GetColor in BaseColors:
        ET.SubElement(Klrs,"color").text = GetColor

    for GetColor in GrayscaleColors:
        ET.SubElement(Klrs,"color").text = GetColor

    tree = ET.ElementTree(Root)
    tree.write(FilePath)
    print("FiLesave Working")



def FileOpen(Path):
    a = 0
    b = 0
    try:
        tree = ET.parse(Path)
        rootTree = tree.getroot()
        print("File is getting open")

        for child in rootTree:
            for color in child.iter('color'):
                if (child.tag == "Colors"):
                    print("color : " + color.text)
                    BaseColors[a] = color.text
                    a=a+1
                elif (child.tag == "GSColors"):
                    print("GSColor : " + color.text)
                    GrayscaleColors[b] = color.text
                    b=b+1
                else:
                    print("##### either this programm is badly written or the file is corrupted (that will be nice for me btw) #####")

    except:
        print("error reading file")


FileOpen('Struct.Klr')

class Gui:
    def __init__(self, master):
######################
#       Set window parameters
######################
        self.master = master
        master.title("SuperMacro")
        master.resizable(False, False)
        master.configure(background=GuiColor)
        x = (master.winfo_screenwidth() // 2) - (MG_width // 2)
        y = (master.winfo_screenheight() // 2) - (MG_height // 2)
        master.geometry('{}x{}+{}+{}'.format(MG_width,MG_height,x,y))


        def DrawIcons():
            i=0
            for itemsIcons in IconList:
                TempPic[i] = PhotoImage(file='Icons/'+itemsIcons+'.png')
                print("ICons =" + itemsIcons)
                i=i+1

            self.t = Button (master,width=IcButton_width,height=IcButton_width,image=TempPic[0],borderwidth=0,bg=GuiColor,command= lambda: ButtonCommand(IconList[0])).grid(row=1, column=0,padx=padxIcButton)
            self.t = Button (master,width=IcButton_width,height=IcButton_width,image=TempPic[1],borderwidth=0,bg=GuiColor,command= lambda: ButtonCommand(IconList[1])).grid(row=2, column=0,padx=padxIcButton)
            self.t = Button (master,width=IcButton_width,height=IcButton_width,image=TempPic[2],borderwidth=0,bg=GuiColor,command= lambda: ButtonCommand(IconList[2])).grid(row=3, column=0,padx=padxIcButton)
            self.t = Button (master,width=IcButton_width,height=IcButton_width,image=TempPic[3],borderwidth=0,bg=GuiColor,command= lambda: ButtonCommand(IconList[3])).grid(row=4, column=0,padx=padxIcButton)
            self.t = Button (master,width=IcButton_width,height=IcButton_width,image=TempPic[4],borderwidth=0,bg=GuiColor,command= lambda: ButtonCommand(IconList[4])).grid(row=5, column=0,padx=padxIcButton)


        def IsClipboardReadable():
            try:
                result = master.clipboard_get()
                print("(yes) the clipbloard is readable")
                return True
            except:
                print("(no) the clipbloard is not readable")
                return False

        def GetClipBoardklr():
            if(IsClipboardReadable()):
                ClipBoardColor = re.match(r"#+((([A-F]|[a-f]|[0-9]){8})|(([A-F]|[a-f]|[0-9]){6})|(([A-F]|[a-f]|[0-9]){3}))", master.clipboard_get())
                if (ClipBoardColor):
                    print ("woohoo ClipBoard Contains a color : " + ClipBoardColor[0])
                    return(ClipBoardColor[0])
                else:
                    print ("ClipBoard Doesn't contain any color")
                    return(GuiColor)
        def SetClipBoardklr(Item):

    	    master.clipboard_clear()
    	    master.clipboard_append(Item)


######################
#       Side Pannel
######################


        DrawIcons()


        canvas = Canvas (master,width = CanvaDisplay_width,height = MG_height,bg = GuiColor, bd=0,highlightthickness=0,cursor="cross")
        ClipBoardRect = canvas.create_rectangle(CanvaDisplay_width-ClipBoardRect_width, 0, CanvaDisplay_width, MG_height,fill=GetClipBoardklr())#GetClipBoardklr()
        i=0

        for x in BaseColors:
            nbBCColors =len(BaseColors)
            sizeBC= (CanvaDisplay_width / nbBCColors)-(ClipBoardRect_width/nbBCColors)
            MarginBC = sizeBC*i

            canvas.create_rectangle(MarginBC, 0, MarginBC+sizeBC, sizeBC,fill=x,outline="",tags=(i,"Col"))
            i=i+1
        j=0
        for y in GrayscaleColors:
            MarginTop = 220
            Height = 150
            TextHeight = 30
            nbGSColors =len(GrayscaleColors)
            sizeGS= (CanvaDisplay_width / nbGSColors)-(ClipBoardRect_width/nbGSColors)
            MarginGS = sizeGS*j
            MAginTextpart2 = (CanvaDisplay_width/2)-ClipBoardRect_width/2

            canvas.create_rectangle(MarginGS, MarginTop, MarginGS+sizeGS, MarginTop + Height,fill=y,outline="",tags=(j,"GS"))
            canvas.create_rectangle(MAginTextpart2 + MarginGS/2, MarginTop-TextHeight, MAginTextpart2 + (MarginGS+sizeGS)/2 , MarginTop,fill=y,outline="",tags=(j,"GS"))
            canvas.create_rectangle(MarginGS/2, MarginTop-TextHeight, (MarginGS+sizeGS)/2, MarginTop,fill=y,outline="",tags=(j,"GS"))
            j=j+1

        canvas.grid(row=0,column=1,rowspan=24)



        def Leftclick(event):
            if canvas.find_withtag(CURRENT):
                colorClickGet = canvas.itemcget(CURRENT, "fill")
                print(colorClickGet)
                SetClipBoardklr(colorClickGet)
                SetClipBoardViewerklr(colorClickGet)
    # this item does NOT have the "clickable" tag
                #canvas.update_idletasks()
                #canvas.after(200)
                #canvas.itemconfig(CURRENT, fill="red")
        def Rightclick(event):
            if canvas.find_withtag(CURRENT):
                tags = canvas.itemcget(CURRENT, "tags")
                if ("Col" in tags) or ("GS" in tags):

                    TempKlr = canvas.itemcget(CURRENT, "fill")
                    NwKlr = askcolor(canvas.itemcget(CURRENT, "fill"), master)[1]

                    if TempKlr != NwKlr :
                        if "Col" in tags:
                            print("colorClicked")
                            BaseColors[int(tags[0])] = NwKlr
                        elif "GS" in tags:
                            print("GrayClicked")
                            GrayscaleColors[int(tags[0])] = NwKlr
                        else:
                            print("Wut?")
                        canvas.itemconfig(CURRENT,fill=NwKlr)


        def SetClipBoardViewerklr(color):
            canvas.itemconfig(ClipBoardRect, fill=color)

        canvas.bind("<Button-1>", Leftclick)
        canvas.bind("<Button-3>", Rightclick)

root = Tk()
Gui(root)

root.mainloop()
