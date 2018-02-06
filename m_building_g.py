import sys
import random, math, json
from PySide2 import QtWidgets

import PySide2.QtCore  as qc
import PySide2.QtGui  as qg
import maya.cmds  as mc
import pymel.core as pm

import maya.OpenMaya as om
import maya.OpenMayaUI as mui

dialog = None;

# UI class
#------------------------------------------------------------------------------#

class MbuildingG(QtWidgets.QDialog):
	def __init__(self):
		QtWidgets.QDialog.__init__(self);
		self.setWindowFlags(qc.Qt.WindowStaysOnTopHint);
		self.setWindowTitle('Module Building G');
		self.setFixedHeight(750);
		self.setFixedWidth(400);


		self.setLayout(QtWidgets.QVBoxLayout());
		self.layout().setContentsMargins(5,5,5,5);
		self.layout().setSpacing(0);
		self.layout().setAlignment(qc.Qt.AlignTop);

		main_widget=QtWidgets.QWidget();
		main_widget.setLayout(QtWidgets.QVBoxLayout());
		main_widget.layout().setContentsMargins(0,0,0,0);
		main_widget.layout().setSpacing(2);
		main_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Fixed);
		self.layout().addWidget(main_widget);

		head_splitter = Splitter("Project and individual layer setting");
		main_widget.layout().addWidget(head_splitter);

		proj_setting_layout = QtWidgets.QHBoxLayout()
		proj_setting_layout.setContentsMargins(4,6,4,10)
		proj_setting_layout.setSpacing(2)
		main_widget.layout().addLayout(proj_setting_layout)

		name_text_lb = QtWidgets.QLabel('Building Grp Name:')
		self.module_grp_name = QtWidgets.QLineEdit()
		self.module_grp_name.setText( "fin_building_grp" )
		proj_setting_layout.addWidget(name_text_lb)
		proj_setting_layout.addWidget(self.module_grp_name)
		proj_setting_layout.layout().addStretch()

		pre_setting_layout = QtWidgets.QHBoxLayout()
		pre_setting_layout.setContentsMargins(4,0,4,0)
		pre_setting_layout.setSpacing(2)
		main_widget.layout().addLayout(pre_setting_layout)


		relate_setting_layout = QtWidgets.QVBoxLayout()
		relate_setting_layout.setContentsMargins(0,0,8,0)
		relate_setting_layout.setSpacing(2)
		pre_setting_layout.layout().addLayout(relate_setting_layout)

		self.create_relation_Table();
		relate_setting_layout.layout().addWidget(self.relat_tableWidget);

		relate_btn_setting_layout = QtWidgets.QHBoxLayout()
		relate_btn_setting_layout.setContentsMargins(8,5,8,5)
		relate_btn_setting_layout.setSpacing(2)
		relate_setting_layout.layout().addLayout(relate_btn_setting_layout)

		add_relate_btn = QtWidgets.QPushButton('Add to relation')
		add_relate_btn.setFixedHeight(30)
		add_relate_btn.setFixedWidth(100)
		relate_btn_setting_layout.layout().addWidget(add_relate_btn);

		relate_btn_setting_layout.layout().addStretch();

		del_relate_btn = QtWidgets.QPushButton('Delete relation')
		del_relate_btn.setFixedHeight(30)
		del_relate_btn.setFixedWidth(100)
		relate_btn_setting_layout.layout().addWidget(del_relate_btn);


		layer_setting_layout = QtWidgets.QVBoxLayout()
		layer_setting_layout.setContentsMargins(5,0,5,0)
		layer_setting_layout.setSpacing(2)
		pre_setting_layout.layout().addLayout(layer_setting_layout)

		top_splitter = Splitter("build layer");
		layer_setting_layout.layout().addWidget(top_splitter);

		del_btn = QtWidgets.QPushButton('Delete layer')
		del_btn.setFixedHeight(35)
		del_btn.setFixedWidth(90)
		layer_setting_layout.layout().addWidget(del_btn);

		dup_btn = QtWidgets.QPushButton('Duplicate layer')
		dup_btn.setFixedHeight(35)
		dup_btn.setFixedWidth(90)
		layer_setting_layout.layout().addWidget(dup_btn);

		layer_setting_layout.layout().addStretch()

		add_btn = QtWidgets.QPushButton('Add layer')
		add_btn.setFixedHeight(55)
		add_btn.setFixedWidth(90)
		layer_setting_layout.layout().addWidget(add_btn);

		top_splitter = Splitter("Single layer buidling data table");
		main_widget.layout().addWidget(top_splitter);

		main_table_layout = QtWidgets.QVBoxLayout()
		main_table_layout.setContentsMargins(4,0,4,0)
		main_table_layout.setSpacing(2)
		main_widget.layout().addLayout(main_table_layout)

		self.createTable();
		main_table_layout.layout().addWidget(self.tableWidget);


		btm_splitter = Splitter("Height setting and finalize the build");
		main_widget.layout().addWidget(btm_splitter);

		post_setting_layout = QtWidgets.QHBoxLayout()
		post_setting_layout.setContentsMargins(4,0,4,0)
		post_setting_layout.setSpacing(2)
		main_widget.layout().addLayout(post_setting_layout)

		post_setting_left_layout = QtWidgets.QVBoxLayout()
		post_setting_left_layout.setContentsMargins(4,0,4,0)
		post_setting_left_layout.setSpacing(2)
		post_setting_layout.layout().addLayout(post_setting_left_layout)

		post_setting_left_upper_layout = QtWidgets.QHBoxLayout()
		post_setting_left_upper_layout.setContentsMargins(4,0,4,0)
		post_setting_left_upper_layout.setSpacing(2)
		post_setting_left_layout.layout().addLayout(post_setting_left_upper_layout)

		height_text_lb = QtWidgets.QLabel('Layer height:')
		self.layer_height_name = QtWidgets.QLineEdit()
		self.layer_height_name.setText( '0' )
		post_setting_left_upper_layout.addWidget(height_text_lb)
		post_setting_left_upper_layout.addWidget(self.layer_height_name)
		post_setting_left_upper_layout.addStretch()

		save_load_layout = QtWidgets.QHBoxLayout()
		save_load_layout.setContentsMargins(4,0,4,0)
		save_load_layout.setSpacing(2)
		post_setting_left_layout.layout().addLayout(save_load_layout)

		save_btn = QtWidgets.QPushButton('Save data')
		save_btn.setFixedHeight(28)
		save_btn.setFixedWidth(110)
		save_load_layout.layout().addWidget(save_btn);

		load_btn = QtWidgets.QPushButton('Load data')
		load_btn.setFixedHeight(28)
		load_btn.setFixedWidth(110)
		save_load_layout.layout().addWidget(load_btn);

		save_load_layout.addStretch()


		post_setting_right_layout = QtWidgets.QVBoxLayout()
		post_setting_right_layout.setContentsMargins(4,0,4,0)
		post_setting_right_layout.setSpacing(2)
		post_setting_layout.layout().addLayout(post_setting_right_layout)

		build_btn = QtWidgets.QPushButton('Build layer')
		build_btn.setFixedHeight(45)
		build_btn.setFixedWidth(130)
		post_setting_right_layout.layout().addWidget(build_btn);


		add_relate_btn.clicked.connect(self.add_relate);
		del_relate_btn.clicked.connect(self.del_relate);
		build_btn.clicked.connect(self.build_layer);
		add_btn.clicked.connect(self.add_row);
		del_btn.clicked.connect(self.del_row);
		dup_btn.clicked.connect(self.dup_row);
		save_btn.clicked.connect(self.save_data);
		load_btn.clicked.connect(self.load_data);



	def create_relation_Table(self):
		self.relat_tableWidget = QtWidgets.QTableWidget()
		self.relat_tableWidget.setRowCount(0)
		self.relat_tableWidget.setColumnCount(2)
		self.relat_tableWidget.setColumnWidth(0, 90)

		header = self.relat_tableWidget.horizontalHeader()   
		header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

		self.relat_tableWidget.setHorizontalHeaderLabels(['Module Name', 'Object Name'])

		self.relat_tableWidget.move(0,0)
		self.relat_tableWidget.setFixedHeight(180)

	def createTable(self):
		# Create table
		self.tableWidget = QtWidgets.QTableWidget()
		self.tableWidget.setRowCount(0)
		self.tableWidget.setColumnCount(4)
		self.tableWidget.setColumnWidth(1, 80)
		self.tableWidget.setColumnWidth(2, 80)
		self.tableWidget.setColumnWidth(3, 80)
		self.tableWidget.setHorizontalScrollBarPolicy(qc.Qt.ScrollBarAlwaysOff)
		self.tableWidget.setHorizontalHeaderLabels(['Module Name', 'traverse X', 'rotate Y', 'pre offset X'])
		header = self.tableWidget.horizontalHeader()       
		header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

		self.tableWidget.move(0,0)
		self.tableWidget.setFixedHeight(375)


	def add_row(self):
		rowPosition = self.tableWidget.rowCount()

		for item in self.tableWidget.selectedIndexes():
			rowPosition = int(item.row()) + 1;
			break;

		self.tableWidget.insertRow(rowPosition)

		tableItem = QtWidgets.QLineEdit()
		tableItem.setText( "Null" )
		self.tableWidget.setCellWidget(rowPosition ,0 , tableItem)

		tableItem = QtWidgets.QLineEdit()
		tableItem.setText( "0" )
		self.tableWidget.setCellWidget(rowPosition ,1 , tableItem)

		tableItem = QtWidgets.QLineEdit()
		tableItem.setText( "0" )
		self.tableWidget.setCellWidget(rowPosition ,2 , tableItem)

		tableItem = QtWidgets.QLineEdit()
		tableItem.setText( "0" )
		self.tableWidget.setCellWidget(rowPosition ,3 , tableItem)


		self.tableWidget.setRowHeight(rowPosition, 25)

	def del_row(self):
		del_target = [];

		for item in self.tableWidget.selectedIndexes():
			rowNumb = int(item.row());
			if rowNumb not in del_target:
				del_target.append(rowNumb);

		del_target.sort(reverse=True)
		if len(del_target) > 0:
			for rowN in del_target:
				self.tableWidget.removeRow(rowN)

	def dup_row(self):
		dup_target = [];

		for item in self.tableWidget.selectedIndexes():
			rowNumb = int(item.row());
			if rowNumb not in dup_target:
				dup_target.append(rowNumb);

		if len(dup_target) > 0:
			for rowN in dup_target:
				old_item = [	str(self.tableWidget.cellWidget(rowN , 0).text()),
								str(self.tableWidget.cellWidget(rowN , 1).text()),
								str(self.tableWidget.cellWidget(rowN , 2).text()),
								str(self.tableWidget.cellWidget(rowN , 3).text())
							]

				rowPosition = self.tableWidget.rowCount()
				self.tableWidget.insertRow(rowPosition)

				tableItem = QtWidgets.QLineEdit()
				tableItem.setText( old_item[0] )
				self.tableWidget.setCellWidget(rowPosition ,0 , tableItem)

				tableItem = QtWidgets.QLineEdit()
				tableItem.setText( old_item[1] )
				self.tableWidget.setCellWidget(rowPosition ,1 , tableItem)

				tableItem = QtWidgets.QLineEdit()
				tableItem.setText( old_item[2] )
				self.tableWidget.setCellWidget(rowPosition ,2 , tableItem)

				tableItem = QtWidgets.QLineEdit()
				tableItem.setText( old_item[3] )
				self.tableWidget.setCellWidget(rowPosition ,3 , tableItem)

				self.tableWidget.setRowHeight(rowPosition, 25)


	def add_relate(self):
		rowPosition = self.relat_tableWidget.rowCount()

		for item in self.relat_tableWidget.selectedIndexes():
			rowPosition = int(item.row()) + 1;
			break;

		self.relat_tableWidget.insertRow(rowPosition)

		tableItem = QtWidgets.QLineEdit()
		tableItem.setText( "Part" )
		self.relat_tableWidget.setCellWidget(rowPosition ,0 , tableItem)

		tableItem = QtWidgets.QLineEdit()
		tableItem.setText( "Object" )
		self.relat_tableWidget.setCellWidget(rowPosition ,1 , tableItem)

		self.relat_tableWidget.setRowHeight(rowPosition, 20)

	def del_relate(self):
		del_target = [];

		for item in self.relat_tableWidget.selectedIndexes():
			rowNumb = int(item.row());
			if rowNumb not in del_target:
				del_target.append(rowNumb);

		del_target.sort(reverse=True)
		if len(del_target) > 0:
			for rowN in del_target:
				self.relat_tableWidget.removeRow(rowN)


	def build_layer(self):
		mc.undoInfo( ock = 1 )

		relation_dict = {};
		rowCount = self.relat_tableWidget.rowCount()
		for i in range (0, rowCount):
			try:
				relation_dict[str(self.relat_tableWidget.cellWidget(i , 0).text())].append(str(self.relat_tableWidget.cellWidget(i , 1).text()));
			except:
				relation_dict[str(self.relat_tableWidget.cellWidget(i , 0).text())] = [str(self.relat_tableWidget.cellWidget(i , 1).text())];
			

		layer_path_data = [];
		rowCount = self.tableWidget.rowCount()
		for i in range (0, rowCount):
			layer_path_data.append([	str(self.tableWidget.cellWidget(i , 0).text()),
										str(self.tableWidget.cellWidget(i , 1).text()),
										str(self.tableWidget.cellWidget(i , 2).text()),
										str(self.tableWidget.cellWidget(i , 3).text())	]);
		

		build_function( relation_dict = relation_dict,
						layer_path_data = layer_path_data,
						layer_height = float(self.layer_height_name.text()),
						grp_name = str(self.module_grp_name.text())
						);

		mc.undoInfo( cck = 1 )


	def save_data(self):
		fileName = QtWidgets.QFileDialog.getSaveFileName( 	self,
															"Save current setting",
															"",
															"*.json"
														)

		if fileName:
			data = {};
			data['proj_name'] = str(self.module_grp_name.text())
			data['layer_height'] = str(self.layer_height_name.text())

			relation_dict = {};
			rowCount = self.relat_tableWidget.rowCount()
			for i in range (0, rowCount):
				try:
					relation_dict[str(self.relat_tableWidget.cellWidget(i , 0).text())].append(str(self.relat_tableWidget.cellWidget(i , 1).text()));
				except:
					relation_dict[str(self.relat_tableWidget.cellWidget(i , 0).text())] = [str(self.relat_tableWidget.cellWidget(i , 1).text())];
			
			data['relation_table'] = relation_dict;

			layer_path_data = [];
			rowCount = self.tableWidget.rowCount()
			for i in range (0, rowCount):
				layer_path_data.append([	str(self.tableWidget.cellWidget(i , 0).text()),
											str(self.tableWidget.cellWidget(i , 1).text()),
											str(self.tableWidget.cellWidget(i , 2).text()),
											str(self.tableWidget.cellWidget(i , 3).text())	]);
			
			data['layer_path_data'] = layer_path_data;

			# Writing JSON data
			with open(str(fileName[0]), 'w') as f:
				json.dump(data, f)


	def load_data(self):
		fileName = QtWidgets.QFileDialog.getOpenFileNames(	self,
															"Load current setting",
															"",
															"*.json"
														)
		if fileName:
			data = {}
			# Reading data back
			with open( str(fileName[0][0]), 'r') as f:
				data = json.load(f);

			self.module_grp_name.setText( data['proj_name'] );
			self.layer_height_name.setText( data['layer_height'] )

			while (self.relat_tableWidget.rowCount() > 0) :
				self.relat_tableWidget.removeRow(0);
			

			for relation_name in data['relation_table']:
				for module_name in data['relation_table'][relation_name]:
					rowPosition = self.relat_tableWidget.rowCount();
					self.relat_tableWidget.insertRow(rowPosition);

					tableItem = QtWidgets.QLineEdit()
					tableItem.setText( relation_name )
					self.relat_tableWidget.setCellWidget(rowPosition ,0 , tableItem)

					tableItem = QtWidgets.QLineEdit()
					tableItem.setText( module_name )
					self.relat_tableWidget.setCellWidget(rowPosition ,1 , tableItem)

					self.relat_tableWidget.setRowHeight(rowPosition, 20)

			for data_row in data['layer_path_data']:
				rowPosition = self.tableWidget.rowCount()
				self.tableWidget.insertRow(rowPosition)

				tableItem = QtWidgets.QLineEdit()
				tableItem.setText( data_row[0] )
				self.tableWidget.setCellWidget(rowPosition ,0 , tableItem)

				tableItem = QtWidgets.QLineEdit()
				tableItem.setText( data_row[1] )
				self.tableWidget.setCellWidget(rowPosition ,1 , tableItem)

				tableItem = QtWidgets.QLineEdit()
				tableItem.setText( data_row[2] )
				self.tableWidget.setCellWidget(rowPosition ,2 , tableItem)

				tableItem = QtWidgets.QLineEdit()
				tableItem.setText( data_row[3] )
				self.tableWidget.setCellWidget(rowPosition ,3 , tableItem)


				self.tableWidget.setRowHeight(rowPosition, 25)




#------------------------------------------------------------------------------#


#------------------------------------------------------------------------------#

class Splitter(QtWidgets.QWidget):
	def __init__(self, text=None, shadow=True, color=(150, 150, 150)):
		QtWidgets.QWidget.__init__(self)

		self.setMinimumHeight(2)
		self.setLayout(QtWidgets.QHBoxLayout())
		self.layout().setContentsMargins(0,0,0,0)
		self.layout().setSpacing(0)
		self.layout().setAlignment(qc.Qt.AlignVCenter)

		first_line = QtWidgets.QFrame()
		first_line.setFrameStyle(QtWidgets.QFrame.HLine)
		self.layout().addWidget(first_line)

		main_color   = 'rgba( %s, %s, %s, 255)' %color
		shadow_color = 'rgba( 45,  45,  45, 255)'

		bottom_border = ''
		if shadow:
		    bottom_border = 'border-bottom:1px solid %s;' %shadow_color

		style_sheet = "border:0px solid rgba(0,0,0,0); \
						background-color: %s; \
						max-height:1px; \
						%s" %(main_color, bottom_border)

		first_line.setStyleSheet(style_sheet)

		if text is None:
		    return

		first_line.setMaximumWidth(5)

		font = qg.QFont()
		font.setBold(True)

		text_width = qg.QFontMetrics(font)
		width = text_width.width(text) + 6

		label = QtWidgets.QLabel()
		label.setText(text)
		label.setFont(font)
		label.setMaximumWidth(width)
		label.setAlignment(qc.Qt.AlignHCenter | qc.Qt.AlignVCenter)

		self.layout().addWidget(label)

		second_line = QtWidgets.QFrame()
		second_line.setFrameStyle(QtWidgets.QFrame.HLine)
		second_line.setStyleSheet(style_sheet)
		self.layout().addWidget(second_line)


class SplitterLayout(QtWidgets.QHBoxLayout):
	def __init__(self):
		QtWidgets.QHBoxLayout.__init__(self)
		self.setContentsMargins(40,2,40,2)

		splitter = Splitter(shadow=False, color=(60,60,60))
		splitter.setFixedHeight(1)

		self.addWidget(splitter)


#------------------------------------------------------------------------------#

def build_function(relation_dict = None, layer_path_data = None, layer_height = 0, grp_name = ''):
	# [a, b] a is Translate X, b is Translate Z
	current_position = [0, 0, 0];
	# angle is rotate Y
	current_angle = 0;


	print layer_path_data;
	print relation_dict;

	w = QtWidgets.QWidget()

	if not mc.objExists(grp_name):
		mc.group( em = 1, name = grp_name )

	index = 0;
	for path in layer_path_data:
		module_name = path[0];
		module_travese = float(path[1]);
		module_travese_angle = float(path[2]);
		modula_pre_offset = float(path[3]);

		object_names = relation_dict[module_name];
		object_name = random.choice(object_names);

		mc.select( clear = 1 );
		mc.select( object_name, r = 1 );
		meshes = mc.ls(sl=1, dag=1, type=['mesh']);
		neo_meshes = mc.duplicate( meshes );

		pre_offset_dis = [	modula_pre_offset* math.cos(float(math.radians(current_angle))),
							-modula_pre_offset* math.sin(float(math.radians(current_angle)))
							]

		current_angle = current_angle + float(module_travese_angle);

		for neo_mesh in neo_meshes:

			if not mc.objExists(neo_mesh):
				QtWidgets.QMessageBox.warning(w, "Message", "Module: WTF is not found")
				return;

			mc.select( neo_mesh, r=True )
			finished_mesh = mc.rename( neo_mesh[:-1] + '_h_' + str(layer_height) + '_' + str(index) )

			mc.rotate( 0, str(current_angle) + 'deg', 0,  finished_mesh); 
			mc.move(  current_position[0] + pre_offset_dis[0], layer_height, current_position[2] + pre_offset_dis[1], finished_mesh, absolute = 1);

			mc.parent( finished_mesh, grp_name )

			index += 1;

		current_position = [current_position[0] + module_travese* math.cos(float(math.radians(current_angle))) +  pre_offset_dis[0],
							layer_height,
							current_position[2] - module_travese* math.sin(float(math.radians(current_angle))) +  pre_offset_dis[1]];


	#QtWidgets.QMessageBox.warning(w, "Message", "Module: WTF is not found")
	QtWidgets.QMessageBox.information(w, "Message", "Build finish")
	w.show()





# recraete and destory the UI
#------------------------------------------------------------------------------#
def create():
	global dialog
	if dialog is None:
		dialog = MbuildingG()
	dialog.show()

def delete():
	global dialog
	if dialog is None:
		return
	dialog.deleteLater()
	dialog = None
#------------------------------------------------------------------------------#