#!/usr/bin/env python
# coding: utf-8

# # Cinema Spec D Viewer (PNG data products only)

# In[211]:


# Author: Jonas Lukasczyk, Divya Banesh, David Rogers
# Date: 07/27/2020


# In[212]:


### This block imports dependencies

# csv reader dependencies
import csv

# ui dependencies
import ipywidgets


# In[213]:


# =====================================================================================
# This block contains generic database operations
# =====================================================================================


# =====================================================================================
# reads column names of a Cinema Spec D database
def readDataBaseHeader(path):
    index2ParameterNameMap = []
    with open(path+"/data.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        # parse header
        for row in csv_reader:
            i = 0
            index2ParameterNameMap = [j for j in range(len(row))]
            for value in row:
                if value=="FILE":
                    fileColumnIndex = i
                index2ParameterNameMap[i] = value
                i+=1
            break
            
    return index2ParameterNameMap

# =====================================================================================
# determines for each column if it contains numeric values
def determineNumericColumns(path):
    index2isNumeric = []
    with open(path+"/data.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        
        # skip header
        for row in csv_reader:
            break
            
        # determine type
        for row in csv_reader:
            for value in row:
                try:
                    valueAsNumber = float(value)
                    index2isNumeric.append(True)
                except ValueError:
                    index2isNumeric.append(False)
            break
            
    return index2isNumeric

# =====================================================================================
# determines the set of possible parameter values for each column
def readParameterValues(path, selectedParameters):
    index2isNumeric = determineNumericColumns(path)
    parameterValues = dict()
    
    for i in selectedParameters:
        parameterValues[i] = set()
    
    with open(path+"/data.csv") as csv_file:
        
        csv_reader = csv.reader(csv_file, delimiter=",")
        
        # skip header
        for row in csv_reader:
            break;
        
        # read content
        for row in csv_reader:
            for i in selectedParameters:
                value = row[i]
                if index2isNumeric[i]:
                    value = float(value)
                parameterValues[i].add(value)
            
    return parameterValues

# =====================================================================================
# builds the a map that maps a combination of parameter values to a set of filepaths
def buildParameterKey2filepathsMap(parameterKey2filepathsMap, path, selectedParameters, selectedFilepaths):
    parameterKey2filepathsMap.clear()
    
    index2isNumeric = determineNumericColumns(path)
    
    with open(path+"/data.csv") as csv_file:
        
        csv_reader = csv.reader(csv_file, delimiter=",")
        
        # skip header
        for row in csv_reader:
            break;
        
        # read content
        for row in csv_reader:
            filepaths = []
            parameterKey = ""
            for i in selectedParameters:
                value = row[i]
                if index2isNumeric[i]:
                    value = str(float(value))
                
                parameterKey += value+"_"
                
            for i in selectedFilepaths:
                filepaths.append(row[i])
            
            if parameterKey2filepathsMap.get(parameterKey)==None:
                parameterKey2filepathsMap[parameterKey] = []
            
            parameterKey2filepathsMap[parameterKey] += filepaths
    
    return parameterKey2filepathsMap

# =====================================================================================
# builds a parameter key based on widget values
def buildParameterKey(parameterWidgets):
    key = ""
    for w in parameterWidgets:
        key += str(w.value)+"_"
    return key


# In[214]:


# =====================================================================================
# create display outputs for widgets
parametersAndFilepathsSelectionOutput = ipywidgets.Output(layout={'border': '0px solid black', 'width':'98%'})
parameterValuesOutput = ipywidgets.Output(layout={'border': '0px solid black', 'width':'40%', 'height':'512px'})
imagesOutput = ipywidgets.Output(layout={'border': '0px solid black', 'width':'59%'})

# =====================================================================================
# global variables that control ...
parameterWidgets = [] # the selected parameters
filepathWidgets = [] # the selected file paths
parameterValueWidgets = [] # the selected parameter values
parameterKey2filepathMap = dict() # the key-value map that maps parameter combinations to filepaths

# =====================================================================================
# create database path widget 
dbPathWidget = ipywidgets.Text(
    value='',
    placeholder='Absolute path to .cdb',
    description='CDB:',
    continuous_update=False,
    disabled=False,
    layout=ipywidgets.Layout(width='90%')
)

# =====================================================================================
# update widgets to distinguish between parameters and filepaths of the selected database
def updateParameterAndFilepathWidgets(ignore):
    cdatabases = dbPathWidget.value.split(' ')
    cdb = cdatabases[0] #all databases are assumed to have same parameter list
    dbHeader = readDataBaseHeader(cdb)
    parameterWidgets.clear()
    filepathWidgets.clear()

    for param in dbHeader:
        pW = ipywidgets.ToggleButton(
            value= param!="FILE",
            description=param,
            disabled=False
        )
        pW.observe(updateParameterValueWidgets, names='value')
        parameterWidgets.append(pW)

        fW = ipywidgets.ToggleButton(
            value= param=="FILE",
            description=param,
            disabled=False
        )
        fW.observe(updateParameterValueWidgets, names='value')
        filepathWidgets.append(fW)

    grid = ipywidgets.GridspecLayout(2, len(parameterWidgets)+1)
    grid[0,0] = ipywidgets.Label("Parameters")
    grid[1,0] = ipywidgets.Label("Paths")

    for j in range(0,len(parameterWidgets)):
        grid[0,j+1] = parameterWidgets[j]
    for j in range(0,len(filepathWidgets)):
        grid[1,j+1] = filepathWidgets[j]

    with parametersAndFilepathsSelectionOutput:
        parametersAndFilepathsSelectionOutput.clear_output()
        display(grid)

    updateParameterValueWidgets('')
    return

# =====================================================================================
# update widgets to select parameter values 
def updateParameterValueWidgets(ignore):
    selectedParameters = dict()
    selectedFilepaths = dict()
    if True:
        i=0
        for w in parameterWidgets:
            if w.value==True:
#                 print(w.description)
                selectedParameters[i] = w.description
            i+=1
        i=0
        for w in filepathWidgets:
            if w.value==True:
#                 print(w.description)
                selectedFilepaths[i] = w.description
            i+=1
    
    cdatabases = dbPathWidget.value.split(' ')
    cdb = cdatabases[0]#all databases are assumed to have same parameter list
    selectedParameterValues = readParameterValues(cdb, selectedParameters)
    buildParameterKey2filepathsMap(parameterKey2filepathMap, cdb, 
                                   selectedParameters, selectedFilepaths)

    parameterValueWidgets.clear()
    for i in selectedParameters:
        w = ipywidgets.SelectionSlider(
            options=sorted(selectedParameterValues[i]),
            description=selectedParameters[i],
            disabled=False,
            continuous_update=True,
            orientation='horizontal',
            readout=True
        )
        w.observe(updateImages, names='value')
        parameterValueWidgets.append(w)

    with parameterValuesOutput:
        parameterValuesOutput.clear_output()
        temp = ipywidgets.VBox(parameterValueWidgets)
        display( temp )

    updateImages('')
    return

imageWidgets = []

# =====================================================================================
# fetch images that correspond to the currently selected parameter values 
def updateImages(ignore):
    cdatabases = dbPathWidget.value.split(' ')
    cdatabases = list(filter(lambda a: a != '', cdatabases))
    
    key = buildParameterKey( parameterValueWidgets )
    
    files = []
    for cdb in cdatabases:
        for filepath in parameterKey2filepathMap[key]:
            file = open(cdb+'/'+filepath, "rb")
            files.append(file.read())

    if len(files)!=len(imageWidgets):
        imageWidgets.clear()
        imagesOutput.clear_output()
        for file in files:
            w = ipywidgets.Image(
                format='png',
                layout={'display':'block','max_width':'512px','max_height':'512px'}
            )
            imageWidgets.append(w)
            with imagesOutput:
                display(w)

# to display horizontally, comment out previous 2 lines of code and uncomment below
#         with imagesOutput:
#             imagesOutput.clear_output()
#             temp = ipywidgets.HBox(imageWidgets)
#             display(temp)                

    for i in range(0,len(files)):
        imageWidgets[i].value = files[i]
        
    return

# =====================================================================================

def loadCinemaViewer(paths):
    #set paths
    dbPathWidget.value = paths

    # start listening for new database path
    updateParameterAndFilepathWidgets('')
    
    # display UI
    frame = ipywidgets.VBox([
        parametersAndFilepathsSelectionOutput,
        ipywidgets.HBox([parameterValuesOutput,imagesOutput])
    ])
    display(frame)

