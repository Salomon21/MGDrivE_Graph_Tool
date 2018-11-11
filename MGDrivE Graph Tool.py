# -*- coding: utf-8 -*-
import plotly
import plotly.graph_objs as go
import pandas as pd
import plotly.io as pio
import os
import io
from PIL import Image
from os import listdir
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import threading
from threading import Thread

#Function that get positions of nodes from csv
def get_positions(file):
    pf = pd.read_csv(file,header=None)
    
    pieX = [0.125, 0.875]
    pieY = [0.125, 0.875]

    pf.columns = ['x','y']
    
    xValues = pf.x.tolist()
    yValues = pf.y.tolist()
    
    gCap = 0.040
    
    xMin = (pf.x.min()-10)
    xMax = (pf.x.max()+10)
    yMin = (pf.y.min()-10)
    yMax = (pf.y.max()+10)
    
    for yIndex, val in enumerate(xValues):
        #nX = ((val-(xMin)) / (xMax - (xMin)))
        marginR = 0.125
        marginL = 0.125
        marginsH = marginR + marginL
        
        marginT = 0.0
        marginB = 0.0
        marginsW = marginT + marginB
        
        #Normalize position in frame
        nX = ((val-(xMin)) / ((xMax - (xMin))+(xMax - (xMin))*marginsH))+marginL
        nY = ((yValues[yIndex] -(yMin)) / ((yMax - (yMin))+(yMax - (yMin))*marginsW))+marginB
        
        xPos0 = nX - gCap
        xPos1 = nX + gCap
        yPos0 = nY - gCap
        yPos1 = nY + gCap


        xPos0 = (xPos0 * pieX[1]) / 1
        xPos1 = (xPos1 * pieX[1]) / 1
        yPos0 = (yPos0 * pieY[1]) / 1
        yPos1 = (yPos1 * pieY[1]) / 1
        
        
        xPos = [xPos0,xPos1]
        yPos = [yPos0,yPos1]
        
        xPositions.append(xPos)
        yPositions.append(yPos)
        

#Function that iterates through all csv's to get the values in the table
def create_table(csvList):
    tableFrames = []
       
    for indexCsv, csv in enumerate(csvList):
        df = pd.read_csv(csv)
        df = df[df.columns[2:]]
        labelsList = list(df)
        columnIndex = 0
        for index, r in df.iterrows():
            if(len(tableFrames) < 100):
                elemNum = []
                tableFrames.append(elemNum)
            for columnIndex in range(len(labelsList)):
                if(indexCsv == 0):
                    tableFrames[index].append(r[columnIndex])
                else:
                    columnValue = round(tableFrames[index][columnIndex] + r[columnIndex],2)
                    tableFrames[index][columnIndex] = columnValue
    
    return tableFrames

def get_max(tableList):
    maxValue = 0
    for indT, i in enumerate(tableList):
        newVal = sum(tableList[indT])
        if(newVal > maxValue):
            maxValue = newVal
    
    return maxValue

#Function that creates all the jsons to make the graph
def create_graph(csvList):
    
    #Get the number of csv's depending on x's positions
    csvList = csvList[:len(xPositions)]
    figure = {}
    #figureToSave = {}
    figure['frames'] = [] 
    figureData = []
    framesData = []
    time = [str(x) for x in range(100)]
    
    axis=dict(showline=True,zeroline=False,showgrid=True,mirror=True,ticklen=4, gridcolor='#ffffff',tickfont=dict(size=10))
              
    #Returns the values to fill the table
    frameTable = create_table(csvList)              
    maxScatter = get_max(frameTable)
    
    #Create layout
    layout1 = dict(dragmode = "zoom", clickmode = "none", title='MGDrivE', titlefont = dict(size = 40), hidesources = True, margin = dict(t=100), 
                   xaxis2=dict(axis, **dict(domain=[0, 0.125], range = [0, 100], autorange = False, anchor='y2', title='Time')), 
                   yaxis2=dict(axis, **dict(domain=[0.125, 0.875], range = [0, maxScatter], autorange = False, anchor='x2', title='Population', hoverformat='.2f')),
                   sliders = dict(args=['transition', dict(duration = 400,easing = 'cubic-in-out')],
                                        initialValue = '0',plotlycommand = 'animate',values = time,
                                        visible = True),
                   plot_bgcolor='rgba(228, 222, 249, 0.65)'
                   )
    figure['layout'] = layout1
    
    #Sliders dict to control de animation
    sliders_dict = {
            'active': 0,
            'yanchor': 'top',
            'xanchor': 'left',
            'currentvalue': {
                    'font': {'size': 20},
                    'prefix': 'Time:',
                    'visible': True,
                    'xanchor': 'right'
                    },
                    'transition': {'duration': 300, 'easing': 'cubic-in-out'},
                    'pad': {'b': 10, 't': 50},
                    'len': 0.9,
                    'x': 0.1,
                    'y': 0,
                    'steps': []
                    }
    
    #Put the buttons to control the animation
    figure['layout']['updatemenus'] = [
            {'buttons': [
                    {'args': [None,
                              {'frame': {'duration': 500, 'redraw': False},
                               'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
                     'label': 'Play',
                     'method': 'animate'
                     },
                    {'args': [[None],
                              {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                               'transition': {'duration': 0}}],
                    'label': 'Pause',
                    'method': 'animate'
                    }],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
            }
    ]

    
    #Iterate through all csvs
    for indexCsv, csv in enumerate(csvList):
        df = pd.read_csv(csv)
        df = df[df.columns[2:]]
        labelsList = list(df)
        
        initialFigure = go.Pie(showlegend = False,textposition="inside",labels=labelsList, values=df.iloc[2,:].values.tolist(), domain = {'x': xPositions[indexCsv], 'y': yPositions[indexCsv]})
        figureData.append(initialFigure)
        
        #Iterate through all rows per csv
        for index, r in df.iterrows():
            if(len(framesData) < 100):
                framesData.append([])
            
            namePie = "Patch " + str(indexCsv)
            rowFigure = go.Pie(showlegend = False, hoverinfo="label+percent+name",name = namePie,textposition="inside",labels=labelsList, values=df.iloc[index,:].values.tolist(), domain = {'x': xPositions[indexCsv], 'y': yPositions[indexCsv]})
            
            
            framesData[index].append(rowFigure)
        
        if(indexCsv == 0):
            
            framesScatter = []
            framesScatter.append(sum(frameTable[0]))
            scatter = go.Scatter(showlegend = False, xaxis='x2', yaxis='y2', mode='lines', name = "Población Total", line=dict(width=2), x = time, y = framesScatter)
            
            table_trace1 = go.Table(domain=dict(x=[0.875,1],y=[0.25,0.75]),
                                    header = dict(height = 20,
                                                  values = ['<b>Genotype</b>','<b>Population</b>'],
                                                  line = dict(color='rgb(50, 50, 50)'),
                                                  font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                                                  fill = dict(color='#d562be')),
                                    cells = dict(height = 22,
                                                 values = [labelsList,frameTable[0]],
                                                 line = dict(color='rgb(50, 50, 50)'),
                                                 font = dict(color=['rgb(45, 45, 45)'] * 5, size=12)
                                                 )
                                    )
            figureData.append(scatter)
            figureData.append(table_trace1)
            framesScatter = []
            for indexT in range(100):
                framesScatter.append(sum(frameTable[indexT]))
                rowTable = go.Table(domain=dict(x=[0.875,1],y=[0.125, 0.875]),
                                header = dict(height = 20,
                                              values = ['<b>Genotype</b>','<b>Population</b>'],
                                              line = dict(color='rgb(50, 50, 50)'),
                                              font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                                              fill = dict(color='#d562be')),
                                cells = dict(height = 22,
                                             values = [labelsList,frameTable[indexT]],
                                             line = dict(color='rgb(50, 50, 50)'),
                                             font = dict(color=['rgb(45, 45, 45)'] * 5, size=12)
                                             )
                                )
                rowscatter = go.Scatter(showlegend = False,xaxis='x2', yaxis='y2', mode='lines', name = "Población Total", line=dict(width=2), x = time, y = framesScatter)
                framesData[indexT].append(rowTable)
                framesData[indexT].append(rowscatter)
    
    figure['data'] = figureData
    
    
    #Iterate through frames to create json and manage the sliders
    for fi, x in enumerate(framesData):
        figure['frames'].append({'data': framesData[fi], 'name': str(fi)})
        slider_step = {'args': [
                [fi],
                {'frame': {'duration': 300, 'redraw': True},
                 'mode': 'immediate',
                 'transition': {'duration': 300}}
                ],
                'label': time[fi],
                'method': 'animate'}
        
        
        sliders_dict['steps'].append(slider_step)
    
    
    figure['layout']['sliders'] = [sliders_dict]
    
    #Plot the graph and auto open in explorer
    plotly.offline.plot(figure, auto_open=True)
    
def ask_quit():
    if messagebox.askokcancel("Salir", "¿Seguro que desea salir de la aplicación?"):
        root.destroy()

def browse_button(x):
    # Allow user to select a directory and store it in global var
    # called folder_path
    if(x == 1):
        filenames = filedialog.askopenfilenames(filetypes = (("CSV files","*.csv"),("all files","*.*")))
        folder_path.set(filenames)
    else:
        filename = filedialog.askopenfilename(filetypes = (("CSV files","*.csv"),("all files","*.*")))
        node_path.set(filename)
        continue_button_frame = Frame(root)
        Button(continue_button_frame,text="Continuar",width=12,cursor="hand2",state=NORMAL,command=second_window).pack()
        continue_button_frame.place(x=370,y=250)

def execute_code():
    nodes = node_path.get()
    csvLists = folder_path.get()
    
    cList = csvLists.split(',')
    regexCsv = []
    goodCsvs = []
    
    for c in cList:
        if c.startswith("("):
            c = c[1:]
            regexCsv.append(c)
        elif c.endswith(")"):
            c = c[1:-1]
            regexCsv.append(c)
        else:
            c = c[1:]
            regexCsv.append(c)
    
    for gc in regexCsv:
        goodCsvs.append(gc[1:-1])
    
    get_positions(nodes)
    create_graph(goodCsvs)
        
def second_window():
    def start():
        progress["value"] = 0
        maxbytes = 50000
        progress["maximum"] = 50000
        read_bytes()
        
    root.destroy()
    window2 = Tk()
    window2.title("MGDrivE Graph Tool")
    window2.geometry("600x300")
    window2.resizable(False,False)
    bytes = 0
    maxbytes = 0
    
    if(show_page.get() == 1):
        print("Si")
    else:
        print("No")
    
    label = Label(window2, text="Generando gráficas...")
    label.pack(padx=10, pady=40)
    progress = ttk.Progressbar(window2, orient="horizontal",length=500, mode="determinate", takefocus=True)
    progress.pack()
    progress.start()
    
    #Thread(target = execute_code).start()
    #progress.stop()
    
if __name__ == "__main__":
    root = Tk()
    root.title("MGDrivE Graph Tool")
    root.geometry("600x300")
    root.resizable(False,False)
    
    progress = None
    folder_path = StringVar()
    node_path = StringVar()
    show_page = IntVar()
    show_page.set(1)
    xPositions = []
    yPositions = []
    
    directory_frame = Frame(root,width=500,height=40)
    directory_frame.pack_propagate(0) # Stops child widgets of label_frame from resizing it
    Label(directory_frame,fg="black",text="Seleccione los CSV con la información de los nodos:").pack()
    directory_frame.place(x=10,y=10)
    
    folder_frame = Frame(root,width=400,height=40,bg="white")
    folder_frame.pack_propagate(0) # Stops child widgets of label_frame from resizing it
    Label(folder_frame,bg="white",fg="black",textvariable=folder_path).pack()
    folder_frame.place(x=80,y=40)
    
    browse_button1 = Frame(root, width=100,height=20)
    Button(browse_button1,text="Buscar",cursor="hand2", command=lambda:browse_button(1)).pack()
    browse_button1.place(x=500,y=45)
    
    #Second Parameter
    file_frame = Frame(root,width=500,height=40)
    file_frame.pack_propagate(0) # Stops child widgets of label_frame from resizing it
    Label(file_frame,fg="black",text="Seleccione el CSV donde se encuentran la posición de los nodos:").pack()
    file_frame.place(x=10,y=100)
    
    file_path_frame = Frame(root,width=400,height=40,bg="white")
    file_path_frame.pack_propagate(0) # Stops child widgets of label_frame from resizing it
    Label(file_path_frame,bg="white",fg="black",textvariable=node_path).pack()
    file_path_frame.place(x=80,y=130)
    
    browse_button2 = Frame(root, width=100,height=20)
    Button(browse_button2,text="Buscar",cursor="hand2", command=lambda:browse_button(2)).pack()
    browse_button2.place(x=500,y=135)
    
    checkButton = Frame(root)
    Checkbutton(checkButton, text="¿Desea ver la página informativa?", variable=show_page).pack()
    checkButton.place(x=80, y=200)
    
    
    cancel_button = Frame(root)
    Button(cancel_button,text="Cancelar",width=12,cursor="hand2",command=ask_quit).pack()
    cancel_button.place(x=260,y=250)
    
    continue_button_frame = Frame(root)
    Button(continue_button_frame,text="Continuar",width=12,cursor="hand2",state=DISABLED).pack()
    continue_button_frame.place(x=370,y=250)
    
    root.mainloop()