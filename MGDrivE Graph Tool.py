# -*- coding: utf-8 -*-
import plotly
import plotly.graph_objs as go
import pandas as pd
import plotly.io as pio
import os
import io
from PIL import Image
from os import listdir

#Function that get positions of nodes from csv
def get_positions():
    pf = pd.read_csv('NgTown_Coordinates.csv',header=None)
    
    pieX = [0.125, 0.875]
    pieY = [0.125, 0.875]

    pf.columns = ['x','y']
    
    xValues = pf.x.tolist()
    yValues = pf.y.tolist()
    
    gCap = 0.035
    
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

#Function that creates all the jsons to make the graph
def create_graph():
    
    csvList = []
    #Get all the csv's in path
    for csv in listdir('C:/Users/Salom/Desktop/TEC/asd'):
        if csv.endswith('.csv'):
            csvList.append(csv)
    
    #Get the number of csv's depending on x's positions
    csvList = csvList[:len(xPositions)]
    figure = {}
    #figureToSave = {}
    figure['frames'] = [] 
    figureData = []
    framesData = []
    time = [str(x) for x in range(100)]
    
    axis=dict(showline=True,zeroline=False,showgrid=True,mirror=True,ticklen=4, gridcolor='#ffffff',tickfont=dict(size=10))

    #Create layout
    layout1 = dict(title='MGDrivE',margin = dict(t=100), 
                   xaxis2=dict(axis, **dict(domain=[0, 0.125], anchor='y2', showticklabels=False)), 
                   yaxis2=dict(axis, **dict(domain=[0.125, 0.875], anchor='x2', tickprefix='$', hoverformat='.2f')),
                   hovermode = 'closest',
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
    
    #Returns the values to fill the table
    frameTable = create_table(csvList)
    
    if not os.path.exists('images'):
        os.mkdir('images')
    
    #Iterate through all csvs
    for indexCsv, csv in enumerate(csvList):
        df = pd.read_csv(csv)
        df = df[df.columns[2:]]
        labelsList = list(df)
        # Takes the dataframe row out of the list and give it as one list:
        # Instead of [[x,x,x]] == [x,x,x]
        initialFigure = go.Pie(textposition="inside",labels=labelsList, values=[], domain = {'x': xPositions[indexCsv], 'y': yPositions[indexCsv]})
        scatter = go.Scatter(xaxis='x2', yaxis='y2', mode='lines', line=dict(width=2, color='#b04553'), name='mining revenue')
        table_trace1 = go.Table(domain=dict(x=[0.875,1],y=[0.25,0.75]),
                                header = dict(height = 20,
                                              values = ['<b>HH</b>','<b>Value</b>'],
                                              line = dict(color='rgb(50, 50, 50)'),
                                              font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                                              fill = dict(color='#d562be')),
                                cells = dict(height = 22,
                                             values = [labelsList,frameTable[0]],
                                             line = dict(color='rgb(50, 50, 50)'),
                                             font = dict(color=['rgb(45, 45, 45)'] * 5, size=12)
                                             )
                                )
        figureData.append(initialFigure)
        figureData.append(scatter)
        figureData.append(table_trace1)
        
        #Iterate through all rows per csv
        for index, r in df.iterrows():
            if(len(framesData) < 100):
                framesData.append([])
            
            namePie = "Patch " + str(indexCsv)
            rowFigure = go.Pie(hoverinfo="label+percent+name",name = namePie,textposition="inside",labels=labelsList, values=df.iloc[index,:].values.tolist(), domain = {'x': xPositions[indexCsv], 'y': yPositions[indexCsv]})
            rowTable = go.Table(domain=dict(x=[0.875,1],y=[0.25,0.75]),
                                header = dict(height = 20,
                                              values = ['<b>HH</b>','<b>Value</b>'],
                                              line = dict(color='rgb(50, 50, 50)'),
                                              font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                                              fill = dict(color='#d562be')),
                                cells = dict(height = 22,
                                             values = [labelsList,frameTable[index]],
                                             line = dict(color='rgb(50, 50, 50)'),
                                             font = dict(color=['rgb(45, 45, 45)'] * 5, size=12)
                                             )
                                )
            framesData[index].append(rowFigure)
            framesData[index].append(scatter)
            framesData[index].append(rowTable)
    
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
    
# =============================================================================
#         figureToSave['layout'] = dict(title='MGDrivE',margin = dict(t=100), 
#                    xaxis2=dict(axis, **dict(domain=[0, 0.125], anchor='y2', showticklabels=False)), 
#                    yaxis2=dict(axis, **dict(domain=[0.125, 0.875], anchor='x2', tickprefix='$', hoverformat='.2f')),
#                    plot_bgcolor='rgba(228, 222, 249, 0.65)'
#                    )
#         
#         figureToSave['data'] = framesData[fi]
#         #pio.write_image(figureToSave, 'images/'+str(fi)+'.png', width=1920, height=1080)
#         img_bytes = pio.to_image(figureToSave, format='png', width=1366, height=768)
#         image = Image.open(io.BytesIO(img_bytes))
#         image.save('images/'+str(fi)+'.png')
#         img_bytes = None
#         image = None
#             
#         print("{0} Vamos".format(fi))
#         print(img_bytes[:20])
# =============================================================================
        
        
        sliders_dict['steps'].append(slider_step)
    
    
    figure['layout']['sliders'] = [sliders_dict]
    
    #Plot the graph and auto open in explorer
    plotly.offline.plot(figure, auto_open=True)


#Main Function
if __name__ == "__main__":

    xPositions = []
    yPositions = []
    
    get_positions()
    create_graph()
