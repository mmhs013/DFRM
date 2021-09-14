pyinstaller DFRM_GUI_File_gui.spec
echo D | xcopy .\DFRM_Database .\dist\DFRM_Database /E
copy .\DFRM_GUI.ui .\dist\DFRM_GUI.ui