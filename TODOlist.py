import PySimpleGUI as sg

#  __     __         _       _     _           
#  \ \   / /_ _ _ __(_) __ _| |__ | | ___  ___ 
#   \ \ / / _` | '__| |/ _` | '_ \| |/ _ \/ __|
#    \ V / (_| | |  | | (_| | |_) | |  __/\__ \
#     \_/ \__,_|_|  |_|\__,_|_.__/|_|\___||___/

SYMBOL_RIGHT ='►'
SYMBOL_DOWN =  '▼'

menus = {
        'Menu Bar': [['Edit', ['Add', ['Task::ADD', 'Section::ADD', 'List::ADD(MENU)'], ['Delete', ['List::DELETE'], 'Lists', 'Settings']]], ['Help', ['About', 'Wiki']]],
        'Task 0 & 1': ['Right', ['Insert', ['Task::INSERT', 'Section::INSERT'], 'Rename', 'Delete']],
        'Section 0 & 1': ['&Right', ['&Insert', ['Task::INSERT', 'Section::INSERT'], 'Add', ['Task::ADDTO', 'Section::ADDTO'], 'Rename', 'Delete']],
        'Task 2': ['Right', ['Insert', ['Task::INSERT'], 'Rename', 'Delete']],
        'Section 2': ['Right', ['&Insert', ['Task::INSERT', 'Section::INSERT'], 'Add', ['Task::ADDTO'], 'Rename', 'Delete']]
        }

programValues = {
                'List': '',
                'Colour': ''
                }

tempData = {
            'ListIndex': '',
            'elementKeys': [],
            'sectionsOpen': {},
            'combo': [],
            'latestElementRightClicked': '',
            'listSelectedToEdit': ''
            }

data = []



#   _____                 _   _                 
#  |  ___|   _ _ __   ___| |_(_) ___  _ __  ___ 
#  | |_ | | | | '_ \ / __| __| |/ _ \| '_ \/ __|
#  |  _|| |_| | | | | (__| |_| | (_) | | | \__ \
#  |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/

def readDataFile():
    tasks = ['(T)', '(F)']
    booleans = {
        '(T)': True,
        '(F)': False,
        '(O)': True,
        '(C)': False
    }

    with open('data.txt') as f:
        file = f.read().splitlines()

        settings = file[(file.index('Settings:') + 1):file.index('Data:')]
        taskData = file[(file.index('Data:') + 1):]

        previousLine = None

        todolistData = []
        listData = []
        section = []
        subsection = []

        for i in settings:
            i = i.split()

            global colour
            
            if i[0] == 'Colour1:':
                programValues['Colour'] = i[1]

        for i in taskData:
            i = i.split()

            if previousLine != None and previousLine[0] == '---' and i[0] != '---':
                if i[0] == '----':
                    subsection.append({' '.join(i[1:-1]): booleans[i[-1]]})
                elif len(section) != 0:
                    listData.append(section.copy())
                    section.clear() 

            if previousLine != None and previousLine[0] == '----' and i[0] != '----':
                if len(subsection) != 0:
                    section.append(subsection.copy())
                    subsection.clear() 

            if i[0] == '----' and previousLine[0] == '----':
                subsection.append({' '.join(i[1:-1]): booleans[i[-1]]})

            if i[0] == '---':
                if i[-1] in tasks:
                    section.append({' '.join(i[1:-1]): booleans[i[-1]]})
                else:
                    subsection.append({' '.join(i[1:-1]): booleans[i[-1]]})

            if i[0] == '--':
                if i[-1] in tasks:
                    listData.append({' '.join(i[1:-1]): booleans[i[-1]]})
                else:
                    section.append({' '.join(i[1:-1]): booleans[i[-1]]})

            if i[0] == '-':
                if len(listData) != 0:
                    todolistData.append(listData.copy())
                    listData.clear()

                if i[-1] == '!':
                    listData.append(' '.join(i[1:-1]))
                    programValues['List'] = ' '.join(i[1:-1])
                else:
                    listData.append(' '.join(i[1:]))

            previousLine = i


        if len(subsection) != 0:
            section.append(subsection.copy())
            subsection.clear()
        if len(section) != 0:
            listData.append(section.copy())
            section.clear()
        if len(listData) != 0:
            todolistData.append(listData.copy())
            listData.clear()

        global data
        data = todolistData

def writeDataFile():
    with open('data.txt', 'w') as f:

        lines = ['Settings:' ,'Data:']
        filesettings = [f"Colour1: {programValues['Colour']}"]
        filedata = []

        for i in data:
            todolist = i
            for content in todolist:
                if todolist.index(content) == 0:
                    filedata.append(f"- {content}{' !' if programValues['List'] == content else ''}")

                if type(content) is dict:
                    for key, value in content.items():
                        filedata.append(f"-- {key} {'(T)' if value == True else '(F)'}")

                if type(content) is list:

                    header = None
                    opened = None

                    for key, value in content[0].items():
                        header = key
                        opened = value

                    filedata.append(f"-- {header} {'(O)' if opened == True else '(C)'}")

                    for contentInSection in content:
                        if type(contentInSection) is dict and content.index(contentInSection) != 0:
                            for key, value in contentInSection.items():
                                filedata.append(f"--- {key} {'(T)' if value == True else '(F)'}")

                        if type(contentInSection) is list:

                            subheader = None
                            subopened = None

                            for key, value in contentInSection[0].items():
                                subheader = key
                                subopened = value

                            filedata.append(f"--- {subheader} {'(O)' if subopened == True else '(C)'}")

                            for contentInSubSection in contentInSection:
                                if type(contentInSubSection) is dict and contentInSection.index(contentInSubSection) != 0:
                                    for key, value in contentInSubSection.items():
                                        filedata.append(f"---- {key} {'(T)' if value == True else '(F)'}")

        lines[1:1] = filesettings
        lines.extend(filedata)

        f.write('\n'.join(lines))

def colours():
    colour = programValues['Colour']
    if colour != '':
        sg.theme_background_color(colour)
        sg.theme_element_background_color(colour)
        sg.theme_text_element_background_color(colour)
    sg.theme_button_color((None, '#ffffff'))

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
    tempData['combo'].clear()
    combo = tempData['combo']
    for i in data:
        combo.append(i[0])

def createTask(name, checked, listName, hierarchyIndex, sectionID):
    for i in data:
        if i[0] == listName:
            ListIndex = str(data.index(i)).zfill(2)
            hierarchyIndex = str(hierarchyIndex).zfill(2)
            sectionID = str(sectionID).zfill(2)
            elementIndexes = f"{ListIndex} {hierarchyIndex} {sectionID}"

            checkBoxKey = f"{elementIndexes} TASK CHECKBOX {name}"
            checkBoxTextKey = f"{elementIndexes} TASK TEXT {name}"

            rightClickMenu = menus['Task 0 & 1']
            if hierarchyIndex == '02':
                rightClickMenu = menus['Task 2']

            tempData['elementKeys'].append(f"{elementIndexes} TASK {name}")
            return [sg.Checkbox('', default=checked, enable_events=True, key=checkBoxKey, pad=((10, 0),(3,3))), sg.T(name, right_click_menu=rightClickMenu, pad=(0,0), key=checkBoxTextKey, enable_events=True)]

def createSection(header, opened, content, listName, hierarchyIndex, sectionID):
    tempData['sectionsOpen'][f'{header}'] = opened
    for i in data:
        if i[0] == listName:
            ListIndex = str(data.index(i)).zfill(2)
            hierarchyIndex = str(hierarchyIndex).zfill(2)
            sectionID = str(sectionID).zfill(2)
            elementIndexes = f"{ListIndex} {hierarchyIndex} {sectionID}"

            sectionArrowKey = f'{elementIndexes} SECTION ARROW {header}'
            sectionTextKey = f'{elementIndexes} SECTION TEXT {header}'
            sectionContentKey = f'{elementIndexes} SECTION CONTENT {header}'

            rightClickMenu = menus['Section 0 & 1']
            if hierarchyIndex == '01':
                rightClickMenu = menus['Section 2']

            tempData['elementKeys'].append(f"{elementIndexes} SECTION {header}")
            return [[sg.T(symbol(opened), enable_events=True, k=sectionArrowKey, pad=((10, 0),(3,3))), sg.T(header, enable_events=True, k=sectionTextKey, right_click_menu=rightClickMenu)], [collapse(content, sectionContentKey, opened)]]

def createListLayout(theList):
    createdListLayout = []

    sectionID = 0

    for i in data:
        if i[0] is theList:
            contents = i
            for content in contents:
                if type(content) is dict:
                    for key, value in content.items():
                        createdListLayout.append(createTask(key, value, theList, 0, 0))

                if type(content) is list:
                    sectionID += 1

                    ID_of_section = sectionID

                    header = None
                    opened = None

                    for key, value in content[0].items():
                            header = key
                            opened = value

                    sectionContent = []

                    for contentInSection in content:
                        if type(contentInSection) is dict and content.index(contentInSection) != 0:
                            for key, value in contentInSection.items():
                                sectionContent.append(createTask(key, value, theList, 1, ID_of_section))

                        if type(contentInSection) is list:

                            sectionID += 1

                            subheader = None
                            subopened = None
                            
                            for key, value in contentInSection[0].items():
                                    subheader = key
                                    subopened = value

                            subsectionContent = []

                            for contentInSubSection in contentInSection:

                                if type(contentInSubSection) is dict and contentInSection.index(contentInSubSection) != 0:
                                    for key, value in contentInSubSection.items():
                                        subsectionContent.append(createTask(key, value, theList, 2, sectionID))

                            for i in createSection(subheader, subopened, subsectionContent, theList, 1, ID_of_section):
                                sectionContent.append(i)

                    for i in createSection(header, opened, sectionContent, theList, 0, 0):
                        createdListLayout.append(i)    
    return createdListLayout

def createRowOfColumns(listFocused):
    listsColumns = []
    for i in data:
        listLayout = createListLayout(i[0])
        listsColumns.append(sg.Column(layout=listLayout, visible=i[0] == listFocused, size=(300,390), key=f'COL{data.index(i)}', scrollable=True, vertical_scroll_only=True, pad=((0,5),(10,10))))
    
    editListsLayout = [
        [sg.Listbox(key='LISTS LISTBOX', values=tuple(tempData['combo']), size=(32,10), pad=(15,10), enable_events=True)],
        [sg.B('NONE', focus=True, visible=False)],
        [sg.B('Add', k='List::ADD(BUTTON)', image_filename='white.png', image_size=(240, 30), pad=(15, 8))],
        [sg.B('Rename', k='List::RENAME', image_filename='white.png', image_size=(110,30), pad=((15, 11), (0, 0))), sg.B('Delete', k='List::DELETE', image_filename='white.png', image_size=(110,30))],
        [sg.B('Move up', k='List::MOVEUP', image_filename='white.png', image_size=(110, 30), pad=((15, 11), (6, 0))), sg.B('Move down', k='List::MOVEDOWN', image_filename='white.png', image_size=(110, 30), pad=((5, 0), (6, 0)))]
    ]

    settingsLayout = [
        [sg.Text('Colour'), sg.Input(default_text=programValues['Colour'],key='Colour', size=(21,1)), sg.ColorChooserButton('Color...', target=(sg.ThisRow, -1))],
        [sg.B('Apply', pad=(10, 100))]
    ]

    if programValues['List'] == 'EDITING':
        editingListsVisible = True
    else:
        editingListsVisible = False

    if programValues['List'] == 'SETTINGS':
        inSettings = True
    else:
        inSettings = False
    
    listsColumns.append(sg.Column(layout=editListsLayout, visible=editingListsVisible, size=(300,400), key=f'COL EDIT LISTS', scrollable=False, pad=((0,5),(10,10)), metadata={'visible': editingListsVisible}))
    listsColumns.append(sg.Column(layout=settingsLayout, visible=inSettings, size=(300,400), key=f'COL SETTINGS', scrollable=False, pad=((0,5),(10,10)), metadata={'visible': inSettings}))
    return(listsColumns)

def createLayout(listFocused):
    if listFocused is None:
        listFocused = programValues['List']

    if listFocused == 'EDITING' or listFocused == 'SETTINGS':
        addButtonsVisible = False
        if listFocused == 'EDITING':
            comboDefaultValue = 'Editing Lists...'
        else:
            comboDefaultValue = 'Settings'
    else:
        addButtonsVisible = True
        comboDefaultValue = tempData['combo'][tempData['combo'].index(programValues['List'] if programValues['List'] != 'EDITING' else tempData['combo'][0])]

    return [
            [sg.Menu(menus['Menu Bar'])],
            [sg.Combo(tempData['combo'],default_value=comboDefaultValue , size=(100, 1), key='-COMBO-', readonly=True, enable_events=True)],
            createRowOfColumns(listFocused),
            [sg.Col(layout=[[sg.Button('Add Task', image_size=(125,35), key='Task::ADD(BUTTON)', pad=((0,0),(0,0)), image_filename='white.png', border_width=0, button_color=('black', 'black'), visible=addButtonsVisible)]], k='COL ADD BUTTON 1'), sg.Col([[sg.Button('Add Section', image_size=(125,35), key='Section::ADD(BUTTON)', pad=((10,0),(0,0)), image_filename='white.png', border_width=0, button_color=('black', 'black'), visible=addButtonsVisible)]], k='COL ADD BUTTON 2')]
        ]

def addElement(elementType, name, sectionNameToAddTo, hierarchyIndex):

    if name == '' or name is None:
        return 'Nevermind'

    elementToAdd = {name: False}
    if elementType == 'Section':
        elementToAdd = [{name: False}]

    for i in data:
        currentList = programValues['List']
        if i[0] == currentList:
            if hierarchyIndex == '00':
                i.append(elementToAdd)
                return createNewWindow()
            elif hierarchyIndex == '01':
                for content in i:
                    if type(content) is list and sectionNameToAddTo in content[0]:
                        content.append(elementToAdd)
                        return createNewWindow()
            elif hierarchyIndex == '02':
                for content in i:
                    if type(content) is list:
                        for contentInSection in content:
                            if type(contentInSection) is list and sectionNameToAddTo in contentInSection[0]:
                                contentInSection.append(elementToAdd)
                                return createNewWindow()

def insertElement(elementType, name, elementNameOfInsertPos, hierarchyIndex):

    if name == '' or name is None:
        return 'Nevermind'

    elementToInsert = {name: False}
    if elementType == 'Section':
        elementToInsert = [{name: False}]

    for i in data:
        if i[0] == programValues['List']:
            if hierarchyIndex == '00':
                for content in i:
                    if type(content) is dict and elementNameOfInsertPos in content:
                        i.insert(i.index(content), elementToInsert)
                        return createNewWindow()
                    elif type(content) is list and elementNameOfInsertPos in content[0]:
                        i.insert(i.index(content), elementToInsert)
                        return createNewWindow()
            elif hierarchyIndex == '01':
                for section in [content for content in i if type(content) is list]:
                    for contentInSection in section:
                        if type(contentInSection) is dict and elementNameOfInsertPos in contentInSection and section.index(contentInSection) != 0:
                            section.insert(section.index(contentInSection), elementToInsert)
                            return createNewWindow()
                        elif type(contentInSection) is list and elementNameOfInsertPos in contentInSection[0]:
                            section.insert(section.index(contentInSection), elementToInsert)
                            return createNewWindow()
            elif hierarchyIndex == '02':
                for section in [content for content in i if type(content) is list]:
                    for subSection in [contentInSection for contentInSection in section if type(contentInSection) is list]:
                        for contentInSubSection in subSection:
                            if type(contentInSubSection) is dict and elementNameOfInsertPos in contentInSubSection and subSection.index(contentInSubSection) != 0:
                                subSection.insert(subSection.index(contentInSubSection), elementToInsert)
                                return createNewWindow()

def updateData(elementType, name):
    for todoList in data:
            if todoList[0] == programValues['List']:
                for content in todoList:
                    if elementType == 'Section':
                        if type(content) is list:
                            if name in content[0]:
                                content[0][name] = tempData['sectionsOpen'][name]
                                return

                            for contentInSection in content:
                                if type(contentInSection) is list:
                                    if name in contentInSection[0]:
                                        contentInSection[0][name] = tempData['sectionsOpen'][name]
                                        return

                    if elementType == 'Task':
                        if type(content) is dict:
                            if name in content:
                                content[name] = not content[name]
                                return
                            
                        if type(content) is list:
                            for contentInSection in content:
                                if type(contentInSection) is dict:
                                    if name in contentInSection:
                                        contentInSection[name] = not contentInSection[name]
                                        return
                                if type(contentInSection) is list:
                                    for contentInSubSection in contentInSection:
                                        if name in contentInSubSection:
                                            contentInSubSection[name] = not contentInSubSection[name]
                                            return

def bindRightClick():
    for i in tempData['elementKeys']:
        elementKey = i.split(' ')
        elementKey.insert(4, 'TEXT')
        window[' '.join(elementKey)].bind('<Button-3>', ' +RIGHT CLICK+')

def renameElement(oldKey, newName):
    if 'TASK' in oldKey:
        oldName = oldKey[19:]
    else:
        oldName = oldKey[22:]

    for i in data:
        if i[0] == programValues['List']:
            for content in i:
                if type(content) is dict and oldName in content:
                    content[newName] = content.pop(oldName)
                    break
                elif type(content) is list:
                    for contentInSection in content:
                        if type(contentInSection) is dict and oldName in contentInSection:
                            contentInSection[newName] = contentInSection.pop(oldName)
                            break
                        elif type(contentInSection) is list:
                            for contentInSubSection in contentInSection:
                                if type(contentInSubSection) is dict and oldName in contentInSubSection:
                                    contentInSubSection[newName] = contentInSubSection.pop(oldName)
                                    break
                            else:
                                continue
                            break
                    else:
                        continue
                    break
            else:
                continue
            break

    elementKeys = tempData['elementKeys']
    createNewWindow()
    for i in elementKeys:
        if oldKey in i:
            elementKeys.remove(i)
            return

def delElement(elementKey):
    if 'TASK' in elementKey:
        elementName = elementKey[19:]
    else:
        elementName = elementKey[22:]

    for i in data:
        if i[0] == programValues['List']:
            for content in i:
                if type(content) is dict and elementName in content:
                    i.remove(content)
                    break
                elif type(content) is list:
                    for contentInSection in content:
                        if type(contentInSection) is dict and content.index(contentInSection) == 0 and elementName in contentInSection:
                            i.remove(content)
                            break
                        elif type(contentInSection) is list:
                            for contentInSubSection in contentInSection:
                                if contentInSection.index(contentInSubSection) == 0 and elementName in contentInSubSection:
                                    content.remove(contentInSection)
                                    break
                                elif elementName in contentInSubSection:
                                    contentInSection.remove(contentInSubSection)
                                    break
                            else:
                                continue
                            break
                        elif type(contentInSection) is dict and elementName in contentInSection:
                            content.remove(contentInSection)
                            break
                    else:
                        continue
                    break
            else:
                continue
            break

    elementKeys = tempData['elementKeys']
    createNewWindow()
    for i in elementKeys:
        if elementKey is i:
            elementKeys.remove(i)
            return

def renameList(listName, newListName):
    for i in data:
        if i[0] == listName:
            i[0] = newListName
            break
         
    for listNameInCombo in tempData['combo']:
        if listNameInCombo is listName:
            listNameInCombo = newListName
            break

    createCombo()

    window['-COMBO-'].update(values=tempData['combo'])
    window['LISTS LISTBOX'].update(values=tuple(tempData['combo']))

    print('donee')


def delList():
    if window[f'COL EDIT LISTS'].metadata['visible'] == True:
        theList = values['LISTS LISTBOX'][0]
    else:
        theList = programValues['List']
        
    for i in data:
        if i[0] == theList:
            data.remove(i)
            tempData['combo'].remove(theList)
            for listName in tempData['combo']:
                if listName is not theList:
                    if window[f'COL EDIT LISTS'].metadata['visible'] == True:
                        programValues['List'] = 'EDITING'
                    else:
                        programValues['List'] = listName
                    break
            return createNewWindow()

def getTxt(msg):
    currentLoc = window.CurrentLocation()
    loc = (currentLoc[0] - 25, currentLoc[1] + 100)
    return sg.popup_get_text(msg, location=loc)

def applySettings():
    programValues['Colour'] = values['Colour']
    colours()
    createNewWindow()

def startup():
    readDataFile()

    for i in data:
        if i[0] == programValues['List']:
            tempData['ListIndex'] = str(data.index(i)).zfill(2)
            break

    colours()
    createCombo()
    
startup()

window = sg.Window('TODOlist', layout=createLayout(None), size=(300,500), finalize=True)
bindRightClick()


def createNewWindow():
    tempData['elementKeys'].clear()
    global window
    window1 = sg.Window('TODOlist', layout=createLayout(None), location=window.CurrentLocation(), size=(300,500), finalize=True)
    # if programValues['List'] == 'EDITING':
    #     window1['Task::ADD(BUTTON)'].hide_row()
    window.Close()
    window = window1
    bindRightClick()


#   _____                 _     _                   
#  | ____|_   _____ _ __ | |_  | | ___   ___  _ __  
#  |  _| \ \ / / _ \ '_ \| __| | |/ _ \ / _ \| '_ \ 
#  | |___ \ V /  __/ | | | |_  | | (_) | (_) | |_) |
#  |_____| \_/ \___|_| |_|\__| |_|\___/ \___/| .__/ 
#                                            |_|     
  
while True:             
    event, values = window.read()
    print(event, values)

    if event == sg.WIN_CLOSED or event == 'Exit':
        #writeDataFile()
        break

    # Add a to do list
    if 'List::ADD' in event:
        listName = getTxt('List Name:')

        if listName is not None and listName not in tempData['combo']:
            data.append([listName])

            if 'BUTTON' in event:
                programValues['List'] = 'EDITING'
            else:
                programValues['List'] = listName

            createCombo()
            tempData['ListIndex'] = str(tempData['combo'].index(listName)).zfill(2)

            createNewWindow()
            
        elif listName in tempData['combo']:
            currentLoc = window.CurrentLocation()
            loc = (currentLoc[0] + 80, currentLoc[1] + 100)
            sg.popup('List already exists!', location=loc)

        

    # Change which list your on
    if event == '-COMBO-':  
        programValues['List'] = values['-COMBO-']
        tempData['ListIndex'] = str(tempData['combo'].index(values['-COMBO-'])).zfill(2)
        for i in data:
            if i[0] == programValues['List']:
                window[f'COL{data.index(i)}'].update(visible=True)
            else:
                window[f'COL{data.index(i)}'].update(visible=False)

        otherPages = ['EDIT LISTS', 'SETTINGS']
        for i in otherPages:
            if window[f'COL {i}'].metadata['visible'] == True:
                window[f'COL {i}'].update(visible=False)
                window[f'COL {i}'].metadata = {'visible': False}

        window['Task::ADD(BUTTON)'].update(visible=True)
        window['Section::ADD(BUTTON)'].update(visible=True)
        window['COL ADD BUTTON 1'].unhide_row()


    # Adding an element to the end of the list or section
    if '::ADD' in event and 'List' not in event:

        sectionNameToAddTo = None
        hierarchyIndex = '00'
        sectionID = '00'

        if 'BUTTON' in event:
            elementType = event[:-13]
        else:
            elementType = event[:-5]

        if 'ADDTO' in event:
            sectionNameToAddTo = tempData['latestElementRightClicked'][22:]
            hierarchyIndex = tempData['latestElementRightClicked'][3:5]
            hierarchyIndex = str((int(hierarchyIndex) + 1)).zfill(2)
            sectionID = str((int(tempData['latestElementRightClicked'][6:8]) + 1)).zfill(2)
            elementType = event[:-7]

        elementName = getTxt(f'{elementType} Name:')

        if f"{tempData['ListIndex']} {hierarchyIndex} {sectionID} {elementType.upper()} {elementName}" in tempData['elementKeys']:
            currentLoc = window.CurrentLocation()
            sg.popup(f'{elementType} already exists', location=(currentLoc[0] + 70, currentLoc[1] + 100))
        else:
            addElement(elementType, elementName, sectionNameToAddTo, hierarchyIndex)

    # Inserting elements before the element you right clicked
    if '::INSERT' in event:

        hierarchyIndex = tempData['latestElementRightClicked'][3:5]
        elementType = event[:-8]
        elementName = getTxt(f'{elementType} Name:')

        if tempData['latestElementRightClicked'][6:7] == 'T':
            elementNameOfInsertPos = tempData['latestElementRightClicked'][16:]
        else:
            elementNameOfInsertPos = tempData['latestElementRightClicked'][19:]

        if f"{tempData['ListIndex']} {hierarchyIndex} {elementType.upper()} {elementName}" in tempData['elementKeys']:
            currentLoc = window.CurrentLocation()
            sg.popup(f'{elementType} already exists', location=(currentLoc[0] + 70, currentLoc[1] + 100))
        else:
            insertElement(elementType, elementName, elementNameOfInsertPos, hierarchyIndex)

    # Opening and closing sections
    if 'SECTION' in event and 'RIGHT CLICK' not in event:
        elementIndexes = event[:8]

        if 'ARROW' in event:
            eventName = event[23:]
        else:
            eventName = event[22:]

        tempData['sectionsOpen'][eventName] = not tempData['sectionsOpen'][eventName]
        window[f"{elementIndexes} SECTION ARROW {eventName}"].update(SYMBOL_DOWN if tempData['sectionsOpen'][eventName] else SYMBOL_RIGHT)
        window[f"{elementIndexes} SECTION CONTENT {eventName}"].update(visible=tempData['sectionsOpen'][eventName]) 
        updateData('Section', eventName)


    # Updating the checkbox
    if 'TASK' in event and 'RIGHT CLICK' not in event:

        if 'TEXT' in event:
            eventName = event[19:]
            elementKey = event.split(' ')
            elementKey.remove('TEXT')
            elementKey.insert(4, 'CHECKBOX')
            elementKey = ' '.join(elementKey)
            checked =  window[elementKey].Get()
            window[elementKey].Update(value=not checked)
        else:
            eventName = event[23:]

        #print(eventName)

        updateData('Task', eventName)
    
    # Checking what element the user right clicked
    if '+RIGHT CLICK+' in event:
        elementKey = event[:-14]

        if elementKey is not tempData['latestElementRightClicked']:
            tempData['latestElementRightClicked'] = elementKey
            #print(f"Element right clicked was: {elementKey}")

        event = window[elementKey].user_bind_event
        window[elementKey]._RightClickMenuCallback(event)
        event = elementKey

    # Rename
    if event == 'Rename':
        elementKey = tempData['latestElementRightClicked']
        newName = getTxt('Rename to:')
        if newName is not None:
            renameElement(elementKey, newName)

    # Delete Element
    if event == 'Delete':
        delElement(tempData['latestElementRightClicked'])

    
    # Rename List
    if event == 'List::RENAME' and len(values['LISTS LISTBOX']) != 0:
        listNameToRename = values['LISTS LISTBOX'][0]
        newListName = getTxt('Rename to:')
        renameList(listNameToRename, newListName)
    elif event == 'List:RENAME' and len(values['LISTS LISTBOX']) == 0:
        currentLoc = window.CurrentLocation()
        loc = (currentLoc[0] + 80, currentLoc[1] + 100)
        sg.popup('Please select a list first', location=loc)

    # Delete List
    if event == 'List::DELETE':
        currentLoc = window.CurrentLocation()
        loc = (currentLoc[0] + 4, currentLoc[1] + 100)
        if sg.popup_ok_cancel("This will delete the list and all of it's contents", title='Delete?', location=loc) == 'OK':
            delList()

    # Show Edit Lists Page
    if event == 'Lists':
        for i in tempData['combo']:
            if i == programValues['List']:
                window[f"COL{tempData['combo'].index(i)}"].update(visible=False)
                break
        
        if window['COL SETTINGS'].metadata == {'visible': True}:
            window['COL SETTINGS'].update(visible=False)
            window['COL SETTINGS'].metadata = {'visible': False}

        window['COL EDIT LISTS'].update(visible=True)
        isVisible = window[f'COL EDIT LISTS'].metadata['visible']
        window['COL EDIT LISTS'].metadata = {'visible': not isVisible}
        window['COL ADD BUTTON 1'].hide_row()
        window['-COMBO-'].update(value='Editing Lists...')

    if 'List::MOVE' in event:
        combo = tempData['combo']
        listName = ''

        if values['LISTS LISTBOX'] != []:
            listName = values['LISTS LISTBOX'][0]
        elif values['LISTS LISTBOX'] == [] and tempData['listSelectedToEdit'] != '':
            listName = tempData['listSelectedToEdit']
        else:
            currentLoc = window.CurrentLocation()
            loc = (currentLoc[0] + 80, currentLoc[1] + 100)
            sg.popup('Please select a list first', location=loc)

        for i in data:
            if i[0] is listName:
                theList = i

                index = data.index(theList)
                data.remove(theList)

                if 'UP' in event:
                    data.insert(index - 1, theList)
                elif 'DOWN' in event:
                    data.insert(index + 1, theList)
                createCombo()
                break

        tempData['listSelectedToEdit'] = listName

        window['-COMBO-'].update(values=tempData['combo'])
        window['LISTS LISTBOX'].update(values=tuple(tempData['combo']))

    
    if event == 'Settings':
        for i in tempData['combo']:
            if i == programValues['List']:
                window[f"COL{tempData['combo'].index(i)}"].update(visible=False)
                break

        if window['COL EDIT LISTS'].metadata == {'visible': True}:
            window['COL EDIT LISTS'].update(visible=False)
            window['COL EDIT LISTS'].metadata = {'visible': False}

        programValues['List'] = 'SETTINGS'
        window['COL SETTINGS'].update(visible=True)
        window['COL SETTINGS'].metadata = {'visible': True}
        window['COL ADD BUTTON 1'].hide_row()
        window['-COMBO-'].update(value='Settings')
    
    if event == 'Apply':
        applySettings()
    

window.close()
