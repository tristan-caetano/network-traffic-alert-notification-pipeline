#drop box
csvlist.append("No File")
variable = StringVar(win)
variable.set(csvlist[0]) # default value

dropdown = OptionMenu(win, variable, *csvlist)
dropdown.place(x=840, y=30)

#did not add to GUI.py cus tristan didnt push his new code to it and i didnt wanna ruin it
#this will go in GUI.py tho.. cant figure out how to update the list or add new items into it, got frustrated and gave up for now
