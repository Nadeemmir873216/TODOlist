import PySimpleGUI as sg

# test thing yknow

SYMBOL_RIGHT ='►'
SYMBOL_DOWN =  '▼'


opened1, opened2 = True, False

menu = [['Add', ['Task', 'Section']],      
        ['Lists', ['View', 'Add']
     ]]

section_right_click = ['&Right', [['&Add', ['Task', 'Section', ]], 'Rename', 'Delete']]
task_right_click = ['&Right', [['&Rename', 'Delete']]]

programValues = {'List': 'Today'}

elementKeys = []

SectionsOpen = {}

combo = []

# data is pretty much everything from the to do lists, sections and tasks
# it is a list of lists that shows each To do list
# The first element of the to do lists is the name of the to do list
# Dictionaries are checkboxes that say whether they are ticked or not.
# lists are sections that contain dicitonaries
# The first dictionary under in a list is the name of the section and whether it is closed or not

data = [
    ['Today', [{'Daily': True}, {'Cry': False, 'Protein shake': True}], {'Methods homework': False, 'Physics': True}, [{'Section 1': True}, {'Learn python': False, 'Buy Furniture': True}], [{'Section 2': False}, {'Workout': False}]],
    ['Project 1', {'Sell stocks': False}, [{'Section 3': False}, {'Lift weights': False}], [{'Tessubcontent': True}, {'Cook': False}, [{'Work': False}, {'Fix bug': False}]]]
]

layoutForEachToDoList = {}

def collapse(layout, key, isVisible):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key, visible=isVisible, pad=(15,0)))

def symbol(opened):
    if opened is True:
        return SYMBOL_DOWN
    else:
        return SYMBOL_RIGHT

def createCombo():
    for i in data:
        combo.append(i[0])
    combo.append('                         Add List')
    #print(combo)

def createCheckBox(name, checked, listName):
    for i in data:
        if i[0] == listName:
            return [sg.Checkbox(name, default=checked, enable_events=True, key=f'{data.index(i)} CHECKBOX {name}')]

def createSection(header, opened, content):
    elementKeys.append(f'{header}')
    SectionsOpen[f'{header}'] = opened
    return [[sg.T(symbol(opened), enable_events=True, k=f'{header} ARROW'), sg.T(header, enable_events=True, k=f'{header}', right_click_menu=section_right_click)], [collapse(content, f'{header} CONTENT', opened)]]

def createListLayout(theList):
    createdListLayout = []
    for i in data:
        if i[0] is theList:
            contents = i
            for content in contents:
                if type(content) is dict:
                    for key, value in content.items():
                        createdListLayout.append(createCheckBox(key, value, theList))

                if type(content) is list:
                    for key, value in content[0].items():
                            header = key
                            opened = value

                    for contentInSection in content:
                        sectionContent = []

                        if type(contentInSection) is dict and content.index(contentInSection) != 0:
                            for key, value in contentInSection.items():
                                sectionContent.append(createCheckBox(key, value, theList))

                        if type(contentInSection) is list:
                            for key, value in contentInSection[0].items():
                                    subheader = key
                                    subopened = value

                            for contentInSubSection in contentInSection:
                                subsectionContent = []

                                if type(contentInSubSection) is dict and content.index(contentInSection) != 0:
                                    for key, value in contentInSubSection.items():
                                        subsectionContent.append(createCheckBox(key, value, theList))

                            for i in createSection(subheader, subopened, subsectionContent):
                                sectionContent.append(i)

                    #print(sectionContent)
                    for i in createSection(header, opened, sectionContent):
                        createdListLayout.append(i)
                    
    return createdListLayout

def createRowOfColumns(listFocused):
    listsColumns = []
    for i in data:
        listLayout = createListLayout(i[0])
        listsColumns.append(sg.Column(layout=listLayout, visible=i[0] == listFocused, size=(300,400), key=f'COL{data.index(i)}', scrollable=True, vertical_scroll_only=True, pad=((0,5),(10,10))))
    return(listsColumns)

def createLayout(listFocused):
    if listFocused is None:
        listFocused = programValues['List']
    return [
            [sg.Menu(menu)],
            [sg.Combo(combo,default_value=combo[combo.index(programValues['List'])] , size=(100, 1), key='-COMBO-', readonly=True, enable_events=True)],
            createRowOfColumns(listFocused),
            [sg.Button('Add Task', image_size=(130,40), key='ADDTASK', pad=((5,0),(0,10)), image_filename='white.png', border_width=0, button_color=('black', 'black')), sg.Button('Add Section', image_size=(130,40), pad=((5,0),(0,10)), image_filename='white.png', border_width=0, button_color=('black', 'black'))]
            ]

def addTask(task):
    if task == '':
        print('bruh')
        return 'Nevermind'
        
    for i in data:
        currentList = programValues['List']
        if i[0] == currentList:
            if type(i[-1]) is dict:
                checklistdict = i[-1]
                checklistdict[task] = False
                #i.append(checklistdict)
                #print('to do')
            else:
                #print('theres a section')
                checklistdict = {}
                checklistdict[task] = False
                i.append(checklistdict)

def updateData(dataType, name):
    for todoList in data:
            if todoList[0] == programValues['List']:
                for content in todoList:
                    if dataType == 'section':
                        if type(content) is list:
                            if name in content[0]:
                                content[0][name] = SectionsOpen[name]

                            for subcontent in content:
                                if type(subcontent) is list:
                                    if name in subcontent[0]:
                                        subcontent[0][name] = SectionsOpen[name]

                    if dataType == 'checkbox':
                        if type(content) is dict:
                            if name in content:
                                content[name] = not content[name]
                            
                        if type(content) is list:
                            for subcontent in content:
                                if type(subcontent) is dict:
                                    if name in subcontent:
                                        subcontent[name] = not subcontent[name]



#createListLayout(programValues['List'])
createCombo()

window = sg.Window('TODOlist', layout=createLayout(None), size=(300,500))
print(elementKeys)

bruh = 0

while True:             # Event Loop
    event, values = window.read()
    print(event, values)

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if values['-COMBO-'] == '                         Add List':  # Add a to do list
        currentLoc = window.CurrentLocation()
        loc = (currentLoc[0] - 25, currentLoc[1] + 100)
        text = sg.popup_get_text('List Name', location=loc)

    if event == '-COMBO-':  # Change which list your on
        programValues['List'] = values['-COMBO-']
        for i in data:
            if i[0] == programValues['List']:
                #print('i is the current list')
                window[f'COL{data.index(i)}'].update(visible=True)
            else:
                #print('i is not the current list')
                window[f'COL{data.index(i)}'].update(visible=False)

    if event == 'ADDTASK' or event == 'Task':       # Add A Task

        currentLoc = window.CurrentLocation()
        loc = (currentLoc[0] - 25, currentLoc[1] + 100)
        taskToAdd = sg.popup_get_text('Task Name', location=loc)

        newListLayout = createListLayout(programValues['List'])

        if f"{combo.index(programValues['List'])} CHECKBOX {taskToAdd}" in values:
            sg.popup('Task already exists', location=(currentLoc[0] + 70, currentLoc[1] + 100))
        else:
            if addTask(taskToAdd) != 'Nevermind':

                #print(data)

                newListLayout.append(createCheckBox(taskToAdd, False, programValues['List']))

                #print(newListLayout)
                window1 = sg.Window('TODOlist', layout=createLayout(None), location=window.CurrentLocation(), size=(300,500))
                window.Close()
                window = window1
        



    # Closing and opening sections
    if 'ARROW' in event:
        eventName = event.replace(' ARROW', '')
        SectionsOpen[eventName] = not SectionsOpen[eventName]
        window[f'{event}'].update(SYMBOL_DOWN if SectionsOpen[eventName] else SYMBOL_RIGHT)
        window[f'{eventName} CONTENT'].update(visible=SectionsOpen[eventName])
        #print(SectionsOpen)
        updateData('section', eventName)
        #print(data)


    if event in elementKeys:
        SectionsOpen[event] = not SectionsOpen[event]
        window[f'{event} ARROW'].update(SYMBOL_DOWN if SectionsOpen[event] else SYMBOL_RIGHT)
        window[f'{event} CONTENT'].update(visible=SectionsOpen[event])
        updateData('section', event)

    if 'CHECKBOX' in event:
        listIndex = combo.index(values['-COMBO-'])
        eventName = event.replace(f'{listIndex} CHECKBOX ', '')
        updateData('checkbox', eventName)
    

window.close()
