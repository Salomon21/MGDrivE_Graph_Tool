# -*- coding: utf-8 -*-
import plotly
import plotly.graph_objs as go
import pandas as pd
from os import listdir

# =============================================================================
# def get_positions():
#     pf = pd.read_csv('NgTown_Coordinates.csv',header=None)
#     
#     pieX = [0.125, 0.875]
#     pieY = [0.125, 0.875]
# 
#     pf.columns = ['x','y']
#     
#     xPositions = []
#     yPositions = []
# # =============================================================================
# #     normalizedX = []
# #     normalizedY = []
# # =============================================================================
#     
#     xValues = pf.x.tolist()
#     yValues = pf.y.tolist()
#     
#     gCap = 0.035
#     
#     xMin = (pf.x.min()-10)
#     xMax = (pf.x.max()+10)
#     yMin = (pf.y.min()-10)
#     yMax = (pf.y.max()+10)
#     
#     for yIndex, val in enumerate(xValues):
#         #nX = ((val-(xMin)) / (xMax - (xMin)))
#         marginR = 0.125
#         marginL = 0.125
#         marginsH = marginR + marginL
#         
#         marginT = 0.0
#         marginB = 0.0
#         marginsW = marginT + marginB
#         
#         nX = ((val-(xMin)) / ((xMax - (xMin))+(xMax - (xMin))*marginsH))+marginL
#         nY = ((yValues[yIndex] -(yMin)) / ((yMax - (yMin))+(yMax - (yMin))*marginsW))+marginB
#         
#         xPos0 = nX - gCap
#         xPos1 = nX + gCap
#         yPos0 = nY - gCap
#         yPos1 = nY + gCap
# 
# 
#         xPos0 = (xPos0 * pieX[1]) / 1
#         xPos1 = (xPos1 * pieX[1]) / 1
#         yPos0 = (yPos0 * pieY[1]) / 1
#         yPos1 = (yPos1 * pieY[1]) / 1
#         
#         
#         xPos = [xPos0,xPos1]
#         yPos = [yPos0,yPos1]
#         
#         xPositions.append(xPos)
#         yPositions.append(yPos)
#         
# # =============================================================================
# #         normalizedX.append(nX)
# #         normalizedY.append(nY)
# # =============================================================================
# =============================================================================
    
def create_graph():
    
    csvList = []
    for csv in listdir('C:/Users/Salom/Desktop/TEC/asd'):
        if csv.endswith('.csv'):
            if(csv.startswith('ADM')):
                csvList.append(csv)
    
    csvList = csvList[:len(xPositions)]
    figure = {}
    figure['frames'] = [] 
    figureData = []
    framesData = []
    indexList = 0
    axis=dict(showline=True,zeroline=False,showgrid=True,mirror=True,ticklen=4, gridcolor='#ffffff',tickfont=dict(size=10))
    layout1 = dict(title='MGDrivE',margin = dict(t=100), 
                   xaxis2=dict(axis, **dict(domain=[0, 0.125], anchor='y2', showticklabels=False)), 
                   yaxis2=dict(axis, **dict(domain=[0.125, 0.875], anchor='x2', tickprefix='$', hoverformat='.2f')),
                   plot_bgcolor='rgba(228, 222, 249, 0.65)'
                   )
    figure['layout'] = layout1

    csvC = 0
    for indexCsv, csv in enumerate(csvList):
        df = pd.read_csv(csv)
        df = df[['WW','WH','WR','WB','HH','HR','HB','RR','RB','BB']]
        labelsList = list(df)
        # Takes the dataframe row out of the list and give it as one list:
        # Instead of [[x,x,x]] == [x,x,x]
        initialFigure = go.Pie(textposition="inside",labels=labelsList, values=sum(df.take([0]).values.tolist(),[]), domain = {'x': xPositions[indexCsv], 'y': yPositions[indexCsv]})
        scatter = go.Scatter(xaxis='x2', yaxis='y2', mode='lines', line=dict(width=2, color='#b04553'), name='mining revenue')
        table_trace1 = go.Table(domain=dict(x=[0.875,1],y=[0.25,0.75]),columnorder=[0, 1],
                                header = dict(height = 50,
                                              values = [['<b>HH</b>'],['<b>Number</b>']],
                                              line = dict(color='rgb(50, 50, 50)'),
                                              align = ['left'] * 5,
                                              font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                                              fill = dict(color='#d562be'))
                                )
        figureData.append(initialFigure)
        figureData.append(scatter)
        figureData.append(table_trace1)
        csvC += 1
        for index, r in df.iterrows():
            if(len(framesData) < 101):
                framesData.append([])
            rowFigure = go.Pie(textposition="inside",labels=labelsList, values=sum(df.take([index]).values.tolist(),[]), domain = {'x': xPositions[indexCsv], 'y': yPositions[indexCsv]})
            framesData[indexList].append(rowFigure)
            framesData[indexList].append(scatter)
            framesData[indexList].append(table_trace1)
            indexList = indexList+1
        indexList = 0
    
    figure['data'] = figureData
    
    for fi, x in enumerate(framesData):
        figure['frames'].append({'data': framesData[fi]})
    
    print(csvC)
    plotly.offline.plot(figure, auto_open=True)


    
if __name__ == "__main__":
    pf = pd.read_csv('NgTown_Coordinates.csv',header=None)
    
    pieX = [0.125, 0.875]
    pieY = [0.125, 0.875]

    pf.columns = ['x','y']
    
    xPositions = []
    yPositions = []
# =============================================================================
#     normalizedX = []
#     normalizedY = []
# =============================================================================
    
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
    
    create_graph()


