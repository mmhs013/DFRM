"""
Dynamic Flood Risk Model (DFRM)

Author: Md. Manjurul Husain Shourov
last edited: 17/10/2020
"""

import sys
import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from pandas import read_csv
from shutil import copyfile
from PyQt5 import uic, QtWidgets, QtGui
from pyproj import _datadir, datadir
# import mapclassify


class Ui(QtWidgets.QDialog):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('DFRM_GUI.ui', self)
        
        self.setWindowTitle('Dynamic Flood Risk Model')
        self.show()

        self.RootDir = os.getcwd()

        self.ImView.setScaledContents(True)
        self.ImView.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)

        self.rbGroup = QtWidgets.QButtonGroup()
        self.rbGroup.addButton(self.InundatatiinRB)
        self.rbGroup.addButton(self.HazardRB)
        self.rbGroup.addButton(self.RiskRB)
        self.rbGroup.addButton(self.VulnerabilityRB)
        self.rbGroup.addButton(self.CapitalRB)

        self.radioBtn = 'Inundation'
        self.InundatatiinRB.toggled.connect((self.RBAction))
        self.HazardRB.toggled.connect((self.RBAction))
        self.RiskRB.toggled.connect((self.RBAction))
        self.VulnerabilityRB.toggled.connect((self.RBAction))
        self.CapitalRB.toggled.connect((self.RBAction))
        self.VulCombo.hide()
        self.CapCombo.hide()

        self.comb = 'full'
        self.comBtn = ''
        self.UnionCombo.hide()
        self.MapExtendCombo.activated.connect(self.ExtendComAction)

        
        self.SubmitPButton.clicked.connect(lambda: self.Action(self.radioBtn, self.comb, self.comBtn))
        self.ClearPButton.clicked.connect(lambda: self.Action(self.radioBtn, self.comb, self.comBtn))
        print(self.comBtn)
        self.savePB.hide()
        self.savePB.clicked.connect(lambda: self.save())

    def RBAction(self):
        self.radioBtn = self.sender().text()[:-4]
        self.VulCombo.hide()
        self.CapCombo.hide()

        if self.radioBtn == 'Vulnerability':
            self.VulCombo.show()
            self.comBtn = 'Human Vulnerability'
            self.VulCombo.activated.connect(self.ComText)
            
        elif self.radioBtn == 'Capital':
            self.CapCombo.show()
            self.comBtn = 'Human Capital'
            self.CapCombo.activated.connect(self.ComText)


    def ComText(self):
        self.comBtn = self.sender().currentText()
        


    def ExtendComAction(self):
        if self.sender().currentText() == 'District Level':
            self.comb = 'full'
            self.UnionCombo.hide()
        else:
            self.comb = 'Ashtamir Char'
            self.UnionCombo.show()
            self.UnionCombo.activated.connect(self.UnionComAction)


    def UnionComAction(self):
        self.comb = self.sender().currentText()
        
    # save method 
    def save(self):
        # selecting file path 
        newfilePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "", 
                         "JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        
        # if file path is blank return back 
        if newfilePath == "": 
            return
          
        # saving canvas at desired path 
        copyfile(self.FilePath, newfilePath) # + '.jpg')

        
    def MapPath(self, WL, RButton, CombButton, VulCapComBtn):
        hydroData = read_csv(self.RootDir + '/DFRM_Database/WL_Hydrograph.csv')
        FName = hydroData.Day.iloc[(hydroData.WL - WL).abs().idxmin()]

        self.River_active = gpd.read_file(self.RootDir + '/DFRM_Database/' + 'NRP_River_Active_2020.shp')
        self.River_corridor = gpd.read_file(self.RootDir + '/DFRM_Database/' + 'NRP_River_Corridor_2020.shp')

        if CombButton == 'full':
            self.data = gpd.read_file(self.RootDir + '/DFRM_Database/Union_' + RButton + '.shp')
            margin_x = 0.15
            margin_y = 0.005
            ColN = 'UNIONNAME'

            arrow_loc = [89.95, 25.6, 0, 0.03, 0.01, 0.02, 1.2] 

        else:
            self.data = gpd.read_file(self.RootDir + '/DFRM_Database/Village_' + RButton + '.shp')
            self.data = self.data[self.data.UNION_NAME == CombButton]
            margin_x = 0.005
            margin_y = 0.005
            ColN = 'Village'

            if CombButton == 'Ashtamir Char':
                arrow_loc = [89.78, 25.46, 0, 0.01, 0.003, 0.005, 0.5]
            elif CombButton == 'Patharsi':
                arrow_loc = [89.77, 25.12, 0,  0.005, 0.002, 0.0025, 0.001]


        ax= self.River_corridor.plot(alpha=0.1, edgecolor='black', figsize=(12,12))
        self.River_active.plot(alpha=0.3, edgecolor='black', ax=ax)

        if RButton == 'Inundation':
            self.data.plot(alpha=0.8,column=FName, cmap='RdYlGn_r', vmin=0,vmax=4, legend=True, legend_kwds = {'label': "Water Depth"}, figsize=(7,10), ax=ax)
            tempData = gpd.read_file(self.RootDir + '/DFRM_Database/Union_Hazard.shp')
            tempData.plot(alpha=0.1,edgecolor='black',ax=ax)

        elif RButton == 'Hazard':
            self.data.plot(alpha=0.8,column=FName, edgecolor='black', cmap='RdYlGn_r', figsize=(7,10), ax=ax, legend=True, legend_kwds = {'label': "Hazard"}, vmin=0, vmax=100) #, legend_kwds={'loc': 'lower right'}, scheme='user_defined', classification_kwds={'bins':[15,30,45,60,100]})

            for x, y, label in zip(self.data.centroid.x, self.data.centroid.y, self.data[ColN]):
                ax.annotate(label, xy=(x, y),horizontalalignment='center',fontsize=9) # xytext=(3, 3), textcoords="offset points", color="red")

        elif RButton == 'Risk':
            self.data.plot(alpha=0.8,column=FName, edgecolor='black', cmap='RdYlGn_r', figsize=(7,10), ax=ax, legend=True, legend_kwds = {'label': "Risk"}, vmin=0,vmax=100) #legend_kwds={'loc': 'lower right'},  scheme='user_defined', classification_kwds={'bins':[15,30,45,60,100]})

            for x, y, label in zip(self.data.centroid.x, self.data.centroid.y, self.data[ColN]):
                ax.annotate(label, xy=(x, y),horizontalalignment='center',fontsize=9) # xytext=(3, 3), textcoords="offset points", color="red")

        elif RButton == 'Vulnerability':

            if VulCapComBtn == 'Human Vulnerability':
                FName = 'Hum_vul'
            elif VulCapComBtn == 'Social Vulnerability':
                FName = 'Soc_vul'
            elif VulCapComBtn == 'Physical Vulnerability':
                FName = 'Phy_vul'
            elif VulCapComBtn == 'Natural Vulnerability':
                FName = 'Nat_vul'
            elif VulCapComBtn == 'Financial Vulnerability':
                FName = 'Fin_vul'
            elif VulCapComBtn == 'Combine Vulnerability':
                FName = 'Com_vul'

            self.data.plot(alpha=0.8,column=FName, edgecolor='black', cmap='RdYlGn_r', figsize=(7,10), ax=ax, legend=True, legend_kwds = {'label': "Vulnerability"}, vmin=0, vmax=100) #, legend_kwds={'loc': 'lower right'}, scheme='user_defined', classification_kwds={'bins':[15,30,45,60,100]})

            for x, y, label in zip(self.data.centroid.x, self.data.centroid.y, self.data[ColN]):
                ax.annotate(label, xy=(x, y),horizontalalignment='center',fontsize=9) # xytext=(3, 3), textcoords="offset points", color="red")

        elif RButton == 'Capital':

            if VulCapComBtn == 'Human Capital':
                FName = 'Hum_cap'
            elif VulCapComBtn == 'Social Capital':
                FName = 'Soc_cap'
            elif VulCapComBtn == 'Physical Capital':
                FName = 'Phy_cap'
            elif VulCapComBtn == 'Natural Capital':
                FName = 'Nat_cap'
            elif VulCapComBtn == 'Financial Capital':
                FName = 'Fin_cap'
            elif VulCapComBtn == 'Combine Capital':
                FName = 'Com_cap'

            self.data.plot(alpha=0.8,column=FName, edgecolor='black', cmap='RdYlGn', figsize=(7,10), ax=ax, legend=True, legend_kwds = {'label': "Capital"}, vmin=0, vmax=100) # legend_kwds={'loc': 'lower right'}, scheme='user_defined', classification_kwds={'bins':[15,30,45,60,100]})

            for x, y, label in zip(self.data.centroid.x, self.data.centroid.y, self.data[ColN]):
                ax.annotate(label, xy=(x, y),horizontalalignment='center',fontsize=9) # xytext=(3, 3), textcoords="offset points", color="red")

   
        xlim = ([self.data.total_bounds[0] - margin_x,  self.data.total_bounds[2]+ margin_x])
        ylim = ([self.data.total_bounds[1] - margin_y,  self.data.total_bounds[3]+ margin_y])
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        plt.xlabel('Longitude',fontsize=10)
        plt.ylabel('Latitude',fontsize=10)
        plt.yticks(rotation=90)
        plt.arrow(x= arrow_loc[0], y=arrow_loc[1], dx=arrow_loc[2], dy=arrow_loc[3], fc="k", ec="k", head_width=arrow_loc[4], head_length=arrow_loc[5], linewidth=arrow_loc[6])
        ax.annotate('N', xy=(arrow_loc[0] + arrow_loc[4], arrow_loc[1]),horizontalalignment='center',fontsize=16)
        
        plt.savefig(self.RootDir + '/DFRM_Database/Temp/im.jpg',bbox_inches='tight',dpi=300)

        self.FilePath = self.RootDir + '/DFRM_Database/Temp/im.jpg'

    def Action(self, RButton, CombButton, VulCapComBtn):
        sender = self.sender()

        if sender.text() == 'Submit':
            
            if ((self.JamunaLineEdit.text() != '') or (self.TeestaLineEdit.text() != '') or (self.DharlaLineEdit.text() != '')):
                JamunaWL = float(self.JamunaLineEdit.text())
##                JamunaWL = float(self.TeestaLineEdit.text())
##                JamunaWL = float(self.DharlaLineEdit.text())
##                TeestaWL = float(self.TeestaLineEdit.text())
##                DharlaWL = float(self.DharlaLineEdit.text())
##                print(JamunaWL)
                self.MapPath(JamunaWL, RButton, CombButton, VulCapComBtn)

                # Map Preparation
                self.PixMap = QtGui.QPixmap(self.FilePath)
                self.ImView.setPixmap(self.PixMap)
                self.ImView.adjustSize()
                self.savePB.show()


        else:
            self.JamunaLineEdit.clear()
            self.TeestaLineEdit.clear()
            self.DharlaLineEdit.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
