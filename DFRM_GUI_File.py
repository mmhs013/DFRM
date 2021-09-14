"""
Dynamic Flood Risk Model (DFRM)

Author: Md. Manjurul Husain Shourov
last edited: 27/06/2021
version : 5.0
"""

import sys
import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from pandas import DataFrame, read_csv, read_excel
from shutil import copyfile
from PyQt5 import uic, QtWidgets, QtGui
from pyproj import _datadir, datadir



class Ui(QtWidgets.QDialog):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('DFRM_GUI.ui', self)
        
        self.setWindowTitle('Dynamic Flood Risk Model')
        self.show()

        self.RootDir = os.getcwd()
        self.db = read_excel(self.RootDir + "/DFRM_Database/NRP_Study_area.xls", "Village")
        # self.hydroData = read_excel(self.RootDir + '/DFRM_Database/WL_Hydrograph.xls',self.river)

        self.River_active = gpd.read_file(self.RootDir + '/DFRM_Database/' + 'NRP_River_Active_2020.shp')
        self.River_corridor = gpd.read_file(self.RootDir + '/DFRM_Database/' + 'NRP_River_Corridor_2020.shp')
        self.river = 'Jamuna'
        self.WL_label.setText('Bahadurabad (Jamuna)')
        self.JamunaLineEdit.setPlaceholderText('Danger Level: 19.5m')

        # self.wrn_vill = read_excel(self.RootDir + "/DFRM_Database/Waring.xlsx",'Village',index_col='Vill_ID', engine='openpyxl')
        # self.wrn_uni = read_excel(self.RootDir + "/DFRM_Database/Waring.xlsx",'Union',index_col='Uni_ID', engine='openpyxl')
        # self.wrn_th = read_excel(self.RootDir + "/DFRM_Database/Waring.xlsx",'Upazilla',index_col='Thana_ID', engine='openpyxl')
        # self.wrn_dist = read_excel(self.RootDir + "/DFRM_Database/Waring.xlsx",'District',index_col='Dist_ID', engine='openpyxl')
                    

        self.ImView.setScaledContents(True)
        self.ImView.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)

        self.rbGroup = QtWidgets.QButtonGroup()
        self.rbGroup.addButton(self.InundatatiinRB)
        self.rbGroup.addButton(self.HazardRB)
        self.rbGroup.addButton(self.RiskRB)
        self.rbGroup.addButton(self.VulnerabilityRB)
        self.rbGroup.addButton(self.WarningRB)
        self.InundatatiinRB.setChecked(True)

        self.rbGroup2 = QtWidgets.QButtonGroup()
        self.rbGroup2.addButton(self.WLRB)
        self.rbGroup2.addButton(self.DLRB)
        self.WLRB.setChecked(True)

        self.WLtype = 'WL'
        self.WLRB.toggled.connect((self.WLAction))
        self.DLRB.toggled.connect((self.WLAction))

        self.radioBtn = 'Inundation'
        self.InundatatiinRB.toggled.connect((self.RBAction))
        self.HazardRB.toggled.connect((self.RBAction))
        self.RiskRB.toggled.connect((self.RBAction))
        self.VulnerabilityRB.toggled.connect((self.RBAction))
        self.WarningRB.toggled.connect((self.RBAction))
        self.TextBox.hide()

        self.LimbText = 'Flood Increasing'
        self.LimbCombo.activated.connect(self.ComText)

        self.Dist_id = 'Dist_01'
        self.Thana_id = 'Th_01'
        self.Union_id = 'Un_001'
        self.Village_id = 'V_0001'
        self.MapLavel = 'District'

        self.DistCombo.show()
        self.UpazillaCombo.hide()
        self.UnionCombo.hide()
        self.VillCombo.hide()
        self.Up_label.hide()
        self.Uni_label.hide()
        self.Vill_label.hide()

        self.DistCombo.addItems(self.db.DISTNAME.unique())
        self.UpazillaCombo.addItems(self.db[self.db.Dist_ID == self.Dist_id].THANAME.unique())
        self.UnionCombo.addItems(self.db[self.db.Thana_ID == self.Thana_id].UNINAME.unique())
        self.VillCombo.addItems(self.db[self.db.Uni_ID == self.Union_id].Village.unique())
        self.MapExtendCombo.addItems(['District', 'Upazilla', 'Union'])
        self.MapExtendCombo.activated.connect(self.ExtendComAction)

        self.DistCombo.activated.connect(self.DistComAction)
        self.UpazillaCombo.activated.connect(self.UpazillaComAction)
        self.UnionCombo.activated.connect(self.UnionComAction)
        self.VillCombo.activated.connect(self.VillComAction)

        self.SubmitPButton.clicked.connect(lambda: self.Action(self.radioBtn))
        self.ClearPButton.clicked.connect(lambda: self.Action(self.radioBtn))

        self.savePB.hide()
        self.savePB.clicked.connect(lambda: self.save())

    def RBAction(self):
        self.radioBtn = self.sender().text()[:-4]
        self.VillCombo.hide()

        self.MapExtendCombo.clear()
        self.MapExtendCombo.addItems(['District', 'Upazilla', 'Union'])

        self.MapExtendCombo.setCurrentText(self.MapLavel)

        if self.radioBtn == 'Warning':
            self.MapExtendCombo.addItems(['Village'])

            if self.MapLavel == 'Village':
                self.VillCombo.show()

    
    def WLAction(self):
        self.radioBtn2 = self.sender().text()

        if self.radioBtn2 == 'Water Level':
            self.WLtype = 'WL'
            self.JamunaLineEdit.clear()
        else:
            self.WLtype = 'DL'
            self.JamunaLineEdit.clear()        

    def ComText(self):
        self.LimbText = self.sender().currentText()


    def ExtendComAction(self):
        self.MapLavel = self.sender().currentText()
        if self.MapLavel == 'District':
            self.UpazillaCombo.hide()
            self.UnionCombo.hide()
            self.VillCombo.hide()
            self.Up_label.hide()
            self.Uni_label.hide()
            self.Vill_label.hide()

            self.DistCombo.activated.connect(self.DistComAction)
            self.UpazillaCombo.activated.connect(self.UpazillaComAction)
            self.UnionCombo.activated.connect(self.UnionComAction)
            self.VillCombo.activated.connect(self.VillComAction)

        elif self.MapLavel == 'Upazilla':            
            self.DistCombo.show()
            self.UpazillaCombo.show()
            self.UnionCombo.hide()
            self.VillCombo.hide()
            self.Up_label.show()
            self.Uni_label.hide()
            self.Vill_label.hide()

            self.DistCombo.activated.connect(self.DistComAction)
            self.UpazillaCombo.activated.connect(self.UpazillaComAction)
            self.UnionCombo.activated.connect(self.UnionComAction)
            self.VillCombo.activated.connect(self.VillComAction)

        elif self.MapLavel == 'Union':
            self.UpazillaCombo.show()
            self.UnionCombo.show()
            self.VillCombo.hide()
            self.Up_label.show()
            self.Uni_label.show()
            self.Vill_label.hide()

            self.DistCombo.activated.connect(self.DistComAction)
            self.UpazillaCombo.activated.connect(self.UpazillaComAction)
            self.UnionCombo.activated.connect(self.UnionComAction)
            self.VillCombo.activated.connect(self.VillComAction)
        
        elif self.MapLavel == 'Village':
            if self.radioBtn == 'Warning':
                self.VillCombo.show()
                self.Vill_label.show()

            self.UnionCombo.show()
            self.UpazillaCombo.show()
            self.Up_label.show()
            self.Uni_label.show()
            
            self.DistCombo.activated.connect(self.DistComAction)
            self.UpazillaCombo.activated.connect(self.UpazillaComAction)
            self.UnionCombo.activated.connect(self.UnionComAction)
            self.VillCombo.activated.connect(self.VillComAction)


    def DistComAction(self):
        comboText = self.sender().currentText()
        self.Dist_id = self.db[self.db.DISTNAME == comboText].Dist_ID.unique()[0]
        self.Thana_id = self.db[self.db.Dist_ID == self.Dist_id].Thana_ID.unique()[0]
        self.Union_id = self.db[self.db.Thana_ID == self.Thana_id].Uni_ID.unique()[0]
        self.Village_id = self.db[self.db.Uni_ID == self.Union_id].Vill_ID.unique()[0]

        self.UpazillaCombo.clear()
        self.UpazillaCombo.addItems(self.db[self.db.Dist_ID == self.Dist_id].THANAME.unique())

        self.UnionCombo.clear()
        self.UnionCombo.addItems(self.db[self.db.Thana_ID == self.Thana_id].UNINAME.unique())

        self.VillCombo.clear()
        self.VillCombo.addItems(self.db[self.db.Uni_ID == self.Union_id].Village.unique())

        self.river = 'Jamuna'
        self.WL_label.setText('Bahadurabad (Jamuna)')
        self.JamunaLineEdit.setPlaceholderText('Danger Level: 19.5m')

    def UpazillaComAction(self):
        comboText = self.sender().currentText()
        self.Thana_id = self.db[self.db.THANAME == comboText].Thana_ID.unique()[0]
        self.Union_id = self.db[self.db.Thana_ID == self.Thana_id].Uni_ID.unique()[0]
        self.Village_id = self.db[self.db.Uni_ID == self.Union_id].Vill_ID.unique()[0]

        self.UnionCombo.clear()
        self.UnionCombo.addItems(self.db[self.db.Thana_ID == self.Thana_id].UNINAME.unique())

        self.VillCombo.clear()
        self.VillCombo.addItems(self.db[self.db.Uni_ID == self.Union_id].Village.unique())

        self.river = 'Jamuna'
        self.WL_label.setText('Bahadurabad (Jamuna)')
        self.JamunaLineEdit.setPlaceholderText('Danger Level: 19.5m')


    def UnionComAction(self):
        comboText = self.sender().currentText()
        self.Union_id = self.db[self.db.UNINAME == comboText].Uni_ID.unique()[0]
        self.Village_id = self.db[self.db.Uni_ID == self.Union_id].Vill_ID.unique()[0]

        self.VillCombo.clear()
        self.VillCombo.addItems(self.db[self.db.Uni_ID == self.Union_id].Village.unique())

        if self.Union_id in ['Un_091','Un_094','Un_095','Un_110']:
            self.river = 'Dharla'
            self.WL_label.setText('Kurigram (Dharla)')
            self.JamunaLineEdit.setPlaceholderText('Danger Level: 26.5m')
        else:
            self.river = 'Jamuna'
            self.WL_label.setText('Bahadurabad (Jamuna)')
            self.JamunaLineEdit.setPlaceholderText('Danger Level: 19.5m')

    def VillComAction(self):
        comboText = self.sender().currentText()
        self.Village_id = self.db[self.db.Village == comboText].Vill_ID.unique()[0]

        self.river = self.db[self.db.Vill_ID == self.Village_id].River.unique()[0]
        if self.river == 'Dharla':
            self.WL_label.setText('Kurigram (Dharla)')
            self.JamunaLineEdit.setPlaceholderText('Danger Level: 26.5m')
        else:
            self.WL_label.setText('Bahadurabad (Jamuna)')
            self.JamunaLineEdit.setPlaceholderText('Danger Level: 19.5m')
    
    # def warn_replace(self, wn, cs, MapLavel, i):
    #     if wn == 0:
    #         return cs[MapLavel][0]
    #     elif wn == 1:
    #         return cs[MapLavel][0 + i]
    #     elif wn == 2:
    #         return cs[MapLavel][1 + i]
    #     elif wn == 3:
    #         return cs[MapLavel][2 + i]
    #     elif wn == 4:
    #         return cs[MapLavel][3 + i]
    #     elif wn == 5:
    #         return cs[MapLavel][4 + i]
        

    # save method 
    def save(self):
        if self.save_opt == 'Warning':
            newfilePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Warning", "", 
                         "CSV(*.csv);;All Files(*.*) ")
            
            if newfilePath != "": 
                self.wrRes.to_csv(newfilePath)

        else:
            # selecting file path 
            newfilePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "", 
                            "JPEG(*.jpg *.jpeg);;All Files(*.*) ")
            
            # if file path is blank return back 
            if newfilePath == "": 
                return
            
            # saving canvas at desired path 
            copyfile(self.FilePath, newfilePath)

        
    def MapPath(self, WL, RButton):
        self.hydroData = read_excel(self.RootDir + '/DFRM_Database/WL_Hydrograph.xls',self.river)
        hydro = self.hydroData[self.hydroData.Limb == self.LimbText]
        FName = hydro.loc[(hydro.WL - WL).abs().idxmin()].Day
        print(self.river)     

        if RButton != 'Warning':
            self.data = gpd.read_file(self.RootDir + '/DFRM_Database/Union_' + self.radioBtn + '.shp')

            if RButton != 'Inundation':
                temp_df = DataFrame(self.data.iloc[:,8:-1])
                self.data.iloc[:,8:-1] = (temp_df - temp_df.min().min()) / (temp_df.max().max() - temp_df.min().min()) * 100
                
            if self.MapLavel == 'District':
                self.bound = self.data[self.data.Dist_ID == self.Dist_id]
            elif self.MapLavel == 'Upazilla':
                self.bound = self.data[self.data.Thana_ID == self.Thana_id]
            elif self.MapLavel == 'Union':
                self.bound = self.data[self.data.Uni_ID == self.Union_id]
            elif self.MapLavel == 'Village':
                self.bound = self.data[self.data.Uni_ID == self.Union_id]

            ax= self.River_corridor.plot(alpha=0.1, edgecolor='black', figsize=(12,12))
            self.River_active.plot(alpha=0.3, edgecolor='black', ax=ax)
            self.bound.plot(alpha=0.8,column=FName, edgecolor='black', cmap='RdYlGn_r', figsize=(7,10), ax=ax, legend=True, legend_kwds = {'label': RButton} , vmin=self.data.iloc[:,8:-1].min().min(),vmax=self.data.iloc[:,8:-1].max().max()) #legend_kwds={'loc': 'lower right'},  scheme='user_defined', classification_kwds={'bins':[15,30,45,60,100]})
            
            margin_x = 0.005
            margin_y = 0.005
            xlim = ([self.bound.total_bounds[0] - margin_x,  self.bound.total_bounds[2]+ margin_x])
            ylim = ([self.bound.total_bounds[1] - margin_y,  self.bound.total_bounds[3]+ margin_y])
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)

            plt.xlabel('Longitude',fontsize=10)
            plt.ylabel('Latitude',fontsize=10)
            plt.yticks(rotation=90)

            plt.savefig(self.RootDir + '/DFRM_Database/Temp/im.jpg',bbox_inches='tight',dpi=300)
            self.FilePath = self.RootDir + '/DFRM_Database/Temp/im.jpg'
            # print(self.Dist_id, self.Thana_id, self.Union_id, self.Village_id)

       
    def Action(self, RButton):
        sender = self.sender()

        if sender.text() == 'Submit':
            if (self.JamunaLineEdit.text() != ''):
                JamunaWL = float(self.JamunaLineEdit.text())

                if self.WLtype == 'DL':
                    JamunaWL = JamunaWL + 19.5

                if RButton == 'Warning':
                    self.hydroData = read_excel(self.RootDir + '/DFRM_Database/WL_Hydrograph.xls',self.river)
                    hydro = self.hydroData[self.hydroData.Limb == self.LimbText]
                    day_no = hydro.Day.loc[(hydro.WL - JamunaWL).abs().idxmin()]
                    print(self.river) 

                    if self.MapLavel == 'District':
                        area_id = self.Dist_id
                        col_id = "Dist_ID"
                        lavel_name = self.db[self.db.loc[:,col_id] == area_id].DISTNAME.iloc[0]
                        # wrn = self.wrn_dist
                    elif self.MapLavel == 'Upazilla':
                        area_id = self.Thana_id
                        col_id = "Thana_ID"
                        lavel_name = self.db[self.db.loc[:,col_id] == area_id].THANAME.iloc[0]
                        # wrn = self.wrn_th
                    elif self.MapLavel == 'Union':
                        area_id = self.Union_id
                        col_id = "Uni_ID"
                        lavel_name = self.db[self.db.loc[:,col_id] == area_id].UNINAME.iloc[0]
                        # wrn = self.wrn_uni
                    elif self.MapLavel == 'Village':
                        area_id = self.Village_id
                        col_id = "Vill_ID"
                        lavel_name = self.db[self.db.loc[:,col_id] == area_id].Village.iloc[0]
                        # wrn = self.wrn_vill

                    vl_cs = {
                            1 : 'Very Low',
                            2 : 'Low',
                            3 : 'Medium',
                            4 : 'High',
                            5 : 'Very High'
                        }

                    dmg_cs = {
                            1 : 'Very Small',
                            2 : 'Small',
                            3 : 'Medium',
                            4 : 'Big',
                            5 : 'Very Big'
                        }

                    print(day_no)
                    wrn = read_excel(self.RootDir + "/DFRM_Database/Warning.xlsx",self.MapLavel,index_col=col_id, engine='openpyxl')
                    wd_cls1 = read_excel(self.RootDir + "/DFRM_Database/WD_1_cls.xlsx",self.MapLavel,index_col=col_id, engine='openpyxl')
                    wd_cls2 = read_excel(self.RootDir + "/DFRM_Database/WD_2_cls.xlsx",self.MapLavel,index_col=col_id, engine='openpyxl')
                    du_cls1 = read_excel(self.RootDir + "/DFRM_Database/Du_1_cls.xlsx",self.MapLavel,index_col=col_id, engine='openpyxl')
                    du_cls2 = read_excel(self.RootDir + "/DFRM_Database/Du_2_cls.xlsx",self.MapLavel,index_col=col_id, engine='openpyxl')
                    
                    # wd_cs = read_csv(self.RootDir + "/DFRM_Database/WD_all_new_warning_ft.csv")
                    # du_cs = read_csv(self.RootDir + "/DFRM_Database/Du_all_new_warning.csv")

                    # wd_cls1 = wrn.applymap(lambda x : self.warn_replace(x, wd_cs, self.MapLavel, 0))
                    # wd_cls2 = wrn.applymap(lambda x : self.warn_replace(x, wd_cs, self.MapLavel, 1))
                    # du_cls1 = wrn.applymap(lambda x : self.warn_replace(x, du_cs, self.MapLavel, 0))
                    # du_cls2 = wrn.applymap(lambda x : self.warn_replace(x, du_cs, self.MapLavel, 1))
                    vl_cls = wrn.replace(vl_cs)
                    dmg_cls = wrn.replace(dmg_cs)
                    std = read_excel(self.RootDir + "/DFRM_Database/NRP_Study_area.xls", self.MapLavel, index_col = col_id)

                    com_Res = DataFrame([wrn.loc[:,day_no],
                                        wd_cls1.loc[:,day_no],
                                        wd_cls2.loc[:,day_no],
                                        du_cls1.loc[:,day_no],
                                        du_cls2.loc[:,day_no],
                                        vl_cls.loc[:,day_no],
                                        dmg_cls.loc[:,day_no]]).T
                    com_Res.columns = ['Warning','WD1','WD2','Du1','Du2','VL','Damage']
                    self.wrRes = std.join(com_Res)
                    tbl = self.wrRes[self.wrRes.index == area_id]

                    if tbl.Warning[0] == 0:
                        text = '''
                        <body style=" font-family:'Times New Roman', Times, serif;">
                        <p  align="center" style=color:#ff0000><h1>No Warning</h1> </p>
                        '''
                    elif tbl.WD2[0] == 20:
                            text = '''
                        <body style=" font-family:'Times New Roman', Times, serif; line-height: 1; font-size:11pt;">
                        <p><b> Warning For : </b> {date} <br>
                        <b> {lavel} : </b> {name} <br>
                        <span style=color:#ff0000><b>Flood Danger Signal : {Warn} </b></span> <br>
                        <b>Water Depth : </b> above {WD_1} ft <br>
                        <b>Flood Duration : </b> {Du_1} days to {Du_2} days<br>
                        <b>Water Speed : </b> {VL} <br>
                        <b>Damage : </b> {Dg}</p>
                        </body>
                        '''.format(
                            date = self.dateEdit.text(),
                            lavel = self.MapLavel,
                            name = lavel_name,
                            Warn = str(int(tbl.Warning[0])),
                            WD_1 = str(tbl.WD1[0]),
                            WD_2 = str(tbl.WD2[0]),
                            Du_1 = str(int(tbl.Du1[0])),
                            Du_2 = str(int(tbl.Du2[0])),
                            VL = tbl.VL[0],
                            Dg = tbl.Damage[0]
                        )
                    else:
                        text = '''
                        <body style=" font-family:'Times New Roman', Times, serif; line-height: 1; font-size:11pt;">
                        <p><b> Warning For : </b> {date} <br>
                        <b> {lavel} : </b> {name} <br>
                        <span style=color:#ff0000><b>Flood Danger Signal : {Warn} </b></span> <br>
                        <b>Water Depth : </b> {WD_1} ft to {WD_2} ft<br>
                        <b>Flood Duration : </b> {Du_1} days to {Du_2} days<br>
                        <b>Water Speed : </b> {VL} <br>
                        <b>Damage : </b> {Dg} </p>
                        </body>
                        '''.format(
                            date = self.dateEdit.text(),
                            lavel = self.MapLavel,
                            name = lavel_name,
                            Warn = str(int(tbl.Warning[0])),
                            WD_1 = str(tbl.WD1[0]),
                            WD_2 = str(tbl.WD2[0]),
                            Du_1 = str(int(tbl.Du1[0])),
                            Du_2 = str(int(tbl.Du2[0])),
                            VL = tbl.VL[0],
                            Dg = tbl.Damage[0]
                        )
                    # print(tbl.WD1[0], tbl.WD2[0])
                    self.TextBox.show()
                    self.TextBox.clear()
                    self.TextBox.moveCursor(QtGui.QTextCursor.Start)
                    self.TextBox.append(text)

                    self.savePB.show()
                    self.savePB.setText("Save Warning")
                    self.save_opt = 'Warning'

                else:
                    self.MapPath(JamunaWL, RButton)

                    # Map Preparation
                    self.PixMap = QtGui.QPixmap(self.FilePath)
                    self.ImView.setPixmap(self.PixMap)
                    self.ImView.adjustSize()
                    self.savePB.show()
                    self.savePB.setText("Save Map")
                    self.save_opt = 'Map'

        else:
            self.JamunaLineEdit.clear()
            self.TextBox.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
