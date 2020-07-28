import csv
import ipywidgets

class CinemaViewer():

    def __init__(self):
        self.imageWidgets = []
        # =====================================================================================
        # create display outputs for widgets
        self.parametersAndFilepathsSelectionOutput = ipywidgets.Output(layout={'border': '0px solid black', 'width':'98%'})
        self.parameterValuesOutput = ipywidgets.Output(layout={'border': '0px solid black', 'width':'40%', 'height':'512px'})
        self.imagesOutput = ipywidgets.Output(layout={'border': '0px solid black', 'width':'59%'})

        # =====================================================================================
        # global variables that control ...
        self.parameterWidgets = [] # the selected parameters
        self.filepathWidgets = [] # the selected file paths
        self.parameterValueWidgets = [] # the selected parameter values
        self.parameterKey2filepathMap = dict() # the key-value map that maps parameter combinations to filepaths

        # =====================================================================================
        # create database path widget 
        self.dbPathWidget = ipywidgets.Text(
            value='',
            placeholder='Absolute path to .cdb',
            description='CDB:',
            continuous_update=False,
            disabled=False,
            layout=ipywidgets.Layout(width='90%')
        )

    def readDataBaseHeader(self, path):
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
    def determineNumericColumns(self, path):
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
    def readParameterValues(self, path, selectedParameters):
        index2isNumeric = self.determineNumericColumns(path)
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
    def buildParameterKey2FilepathMap(self, path, selectedParameters, selectedFilepaths):
        self.parameterKey2filepathMap.clear()
        
        index2isNumeric = self.determineNumericColumns(path)
        
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
                
                if self.parameterKey2filepathMap.get(parameterKey)==None:
                    self.parameterKey2filepathMap[parameterKey] = []
                
                self.parameterKey2filepathMap[parameterKey] += filepaths
        
        return 

    # =====================================================================================
    # builds a parameter key based on widget values
    def buildParameterKey(self):
        key = ""
        for w in self.parameterValueWidgets:
            key += str(w.value)+"_"
        return key



    # =====================================================================================
    # update widgets to distinguish between parameters and filepaths of the selected database
    def updateParameterAndFilepathWidgets(self, ignore):
        cdatabases = self.dbPathWidget.value.split(' ')
        cdb = cdatabases[0] #all databases are assumed to have same parameter list
        dbHeader = self.readDataBaseHeader(cdb)
        self.parameterWidgets.clear()
        self.filepathWidgets.clear()

        for param in dbHeader:
            pW = ipywidgets.ToggleButton(
                value= param!="FILE",
                description=param,
                disabled=False
            )
            pW.observe(self.updateParameterValueWidgets, names='value')
            self.parameterWidgets.append(pW)

            fW = ipywidgets.ToggleButton(
                value= param=="FILE",
                description=param,
                disabled=False
            )
            fW.observe(self.updateParameterValueWidgets, names='value')
            self.filepathWidgets.append(fW)

        grid = ipywidgets.GridspecLayout(2, len(self.parameterWidgets)+1)
        grid[0,0] = ipywidgets.Label("Parameters")
        grid[1,0] = ipywidgets.Label("Paths")

        for j in range(0,len(self.parameterWidgets)):
            grid[0,j+1] = self.parameterWidgets[j]
        for j in range(0,len(self.filepathWidgets)):
            grid[1,j+1] = self.filepathWidgets[j]

        with self.parametersAndFilepathsSelectionOutput:
            self.parametersAndFilepathsSelectionOutput.clear_output()
            display(grid)

        self.updateParameterValueWidgets('')
        return

    # =====================================================================================
    # update widgets to select parameter values 
    def updateParameterValueWidgets(self, ignore):
        selectedParameters = dict()
        selectedFilepaths = dict()
        if True:
            i=0
            for w in self.parameterWidgets:
                if w.value==True:
#                 print(w.description)
                    selectedParameters[i] = w.description
                i+=1
            i=0
            for w in self.filepathWidgets:
                if w.value==True:
#                 print(w.description)
                    selectedFilepaths[i] = w.description
                i+=1
        
        cdatabases = self.dbPathWidget.value.split(' ')
        cdb = cdatabases[0]#all databases are assumed to have same parameter list
        selectedParameterValues = self.readParameterValues(cdb, selectedParameters)
        self.buildParameterKey2FilepathMap(cdb, selectedParameters, selectedFilepaths)

        self.parameterValueWidgets.clear()
        for i in selectedParameters:
            w = ipywidgets.SelectionSlider(
                options=sorted(selectedParameterValues[i]),
                description=selectedParameters[i],
                disabled=False,
                continuous_update=True,
                orientation='horizontal',
                readout=True
            )
            w.observe(self.updateImages, names='value')
            self.parameterValueWidgets.append(w)

        with self.parameterValuesOutput:
            self.parameterValuesOutput.clear_output()
            temp = ipywidgets.VBox(self.parameterValueWidgets)
            display( temp )

        self.updateImages('')
        return


    # =====================================================================================
    # fetch images that correspond to the currently selected parameter values 
    def updateImages(self, ignore):
        cdatabases = self.dbPathWidget.value.split(' ')
        cdatabases = list(filter(lambda a: a != '', cdatabases))
        
        key = self.buildParameterKey()
        
        files = []
        for cdb in cdatabases:
            for filepath in self.parameterKey2filepathMap[key]:
                file = open(cdb+'/'+filepath, "rb")
                files.append(file.read())

        if len(files)!=len(self.imageWidgets):
            self.imageWidgets.clear()
            self.imagesOutput.clear_output()
            for file in files:
                w = ipywidgets.Image(
                    format='png',
                    layout={'display':'block','max_width':'512px','max_height':'512px'}
                )
                self.imageWidgets.append(w)
                with self.imagesOutput:
                    display(w)

# to display horizontally, comment out previous 2 lines of code and uncomment below
                # TODO: implement as an option
#               with self.imagesOutput:
#                   self.imagesOutput.clear_output()
#                   temp = ipywidgets.HBox(self.imageWidgets)
#                   display(temp)                

        for i in range(0,len(files)):
            self.imageWidgets[i].value = files[i]
            
        return

    def load(self, paths):
        #set paths
        self.dbPathWidget.value = paths

        # start listening for new database path
        self.updateParameterAndFilepathWidgets('')
        
        # display UI
        frame = ipywidgets.VBox([
            self.parametersAndFilepathsSelectionOutput,
            ipywidgets.HBox([self.parameterValuesOutput, self.imagesOutput])
        ])
        display(frame)

