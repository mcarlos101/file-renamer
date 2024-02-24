import os, re, logging
from pathlib import Path
import os.path
from abc import ABC, abstractmethod  # import Abstract Base Classes
from PySide6.QtCore import Slot
from lib.exceptions import AppError
from lib.case_insensitive import CaseInsensitive


class File(ABC):

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class Files(File):

	def __init__(self, platform, ui):
		logging.info("Files __init__")
		self.platform = platform
		self.filelist = []  # List of files in directory
		self.changed = {}
		self.file = dict(
			path="", base="", dir="", name="", ext="", id="", new="",
			current=""
		)
		self.limit = 1000  # max number in self.filelist
		self.separator = r"[- \.]"  # hyphen or space or dot

		self.app_error = AppError()
		self.error = dict(name="", exit=True, err="", file="")

		# Regex id
		self.regexid = r'\[.+\]'
        
		# Check case insensitive file systems such as Windows & macOS
		self.case_insensitive = CaseInsensitive()
		self.case_insensitive_val = "UNKOWN"        

	def validate(self, value):
		logging.info("validate")

	def __iter__(self):
		self.filelist = []
		return self

	@Slot()
	def print_title(self, title, ui, widget):
		logging.info("Print Title")
		ui.dir_output.clear()
		text = '<span style="font-weight: bold">' + title + '</span>'
		ui.dir_output.append(text)
		ui.dir_output.append("")

	def find(self, path, ui, widget):
		self.filelist.clear()
		self.changed.clear()
		count = 0
		try:
			if ui.recursively.isChecked():
				for file in Path(path).rglob('*'):
					if os.path.isfile(file):
						if count <= self.limit:
							self.filelist.append(file)
							count += 1
						else:
							self.filelist.clear()
							ui.dir_output.clear()
							raise AppError()
			else:
				for file in Path(path).iterdir():
					if os.path.isfile(file):
						if count <= self.limit:
							self.filelist.append(file)
							count += 1
						else:
							self.filelist.clear()
							raise AppError()
			if count == 0:
				raise FileNotFoundError()
		except FileNotFoundError:
			ui.rename_btn.setEnabled(False)
			self.filelist.clear()
			ui.dir_output.clear()
			text = '<span style="color: red; font-weight: bold">NO FILES FOUND!</span>'
			ui.dir_output.append(text)
		except AppError:
			self.filelist.clear()
			msg = 'FILE LIMIT REACHED: ' + str(self.limit)
			self.app_error.print(ui, msg)
		else:
			self.filelist.sort()
			path = ui.dir_txt.displayText()
			self.case_insensitive_val = self.case_insensitive.check(path)
			logging.info(
				'self.case_insensitive_val: %s', self.case_insensitive_val
			)            

	@Slot()
	def list(self, path, ui, widget):
		text = ""
		if self.filelist:
			title = "List Files"
			self.print_title(title, ui, widget)
			for file in self.filelist:
				ui.dir_output.append(str(file))
			ui.dir_output.append("")
			text = 'Total Files: ' + str(len(self.filelist))
			ui.dir_output.append(text)
			ui.dir_output.append("")

	def split_name(self, path, ui, widget, title):
		logging.info("Split Name")
		filename = ""
		try:
			if os.path.exists(path):
				base = os.path.basename(path)
				split_tup = os.path.splitext(base)
				self.file["path"] = path
				self.file["base"] = base
				self.file["dir"] = os.path.dirname(path)
				self.file["name"] = split_tup[0]
				self.file["ext"] = split_tup[1]

				filename = ""
				if ui.extension.isChecked():
					filename = self.file['name']
				else:
					filename = self.file['base']
				result = re.search(self.regexid, filename)
				if result:
					self.file['id'] = result.group()
				else:
					self.file['id'] = ""
			else:
				raise FileNotFoundError()
		except FileNotFoundError:
			logging.info("FileNotFoundError")
			return None
		else:
			return self.file

	@Slot()
	def compare(self, file, data, ui, widget, title, case_change):
		logging.info("Compare")
		logging.info("data: %s", data)
		file["current"] = ""
		text = ""
		file_exists = True
		logging.info('file["name"]: %s', file["name"])
		logging.info('file["base"]: %s', file["base"])
		logging.info('file["new"] : %s', file["new"])
		logging.info('file["dir"] : %s', file["dir"])
		logging.info('ui.extension.isChecked(): %s', ui.extension.isChecked())
		if ui.extension.isChecked():
			if file["name"] != file["new"] and file['new'] != "":
				file["current"] = file["name"] + file["ext"]
		else:
			if file["base"] != file["new"] and file['new'] != "":
				file["current"] = file["base"]
			else:
				file["current"] = file["base"]

		logging.info('file["current"]: %s', file["current"])

		logging.info('self.platform: %s', self.platform)

		logging.info('self.case_insensitive_val: %s', self.case_insensitive_val)
		if self.case_insensitive_val:
			logging.info('file["current"].lower(): %s', file["current"].lower())
			logging.info('file["new"].lower()    : %s', file["new"].lower())
			if file["current"] == file["new"]:
				logging.info('No change')
				file_exists = True
			elif file["current"] != file["new"]:
				logging.info('Changed')
				# Track lower or title case change
				logging.info('case_change: %s', case_change)
				if case_change:
					if file["current"].lower() == file["new"].lower():
						file_exists = False
						logging.info('file_exists: %s', file_exists)
					elif file["current"].lower() != file["new"].lower():
						file_exists = False
						logging.info('file_exists: %s', file_exists)
				else:
					file_exists = False
					logging.info('file_exists: %s', file_exists)
		else:
			file_exists = os.path.exists((Path(os.path.join(file["dir"]), file["new"])))
			logging.info('file_exists full path: %s', file_exists)

		logging.info('file_exists: %s', file_exists)
		if file_exists is False:
			data["count"] += 1
			num = data["count"]
			self.changed[num] = {}
			self.changed[num]["path"] = Path(os.path.join(file["dir"]), file["current"])
			self.changed[num]["new"] = Path(os.path.join(file["dir"]), file["new"])
			logging.info('self.changed[num]["path"]: %s', self.changed[num]["path"])
			logging.info('self.changed[num]["new"]: %s', self.changed[num]["new"])
			logging.info('data["count"]: %s', data["count"])
			text = '<span style="color: blue; font-weight: bold;">Preview</span>'
			ui.dir_output.append(text)
			ui.dir_output.append(str(self.changed[num]["path"]))
			ui.dir_output.append(str(self.changed[num]["new"]))
			ui.dir_output.append("")

	@Slot()
	def rename(self, path, ui, widget, title):
		logging.info("Rename")
		count = 0
		current_file = ""
		new_file = ""
		for key in self.changed.keys():
			current_file = self.changed[key]['path']
			new_file = self.changed[key]['new']
			if self.case_insensitive_val:
				tmp_file = str(current_file) + '.tmp'
				os.replace(current_file, tmp_file)
				os.replace(tmp_file, new_file)
			else:
				os.replace(current_file, new_file)
			count += 1
			text = '<span style="color: red; font-weight: bold;">Renamed</span>'
			ui.dir_output.append(text)
			ui.dir_output.append(os.path.basename(self.changed[key]['path']))
			ui.dir_output.append(os.path.basename(self.changed[key]['new']))
			ui.dir_output.append("")
			ui.rename_btn.setEnabled(False)

	@Slot()
	def preview(self, data, ui, widget, title):
		logging.info("Preview")
		logging.info('data: %s', data)
		if data["count"] == 0:
			ui.dir_output.append("No changes")
			ui.dir_output.append("")
			ui.rename_btn.setEnabled(False)
		elif data["count"] > 0:
			ui.rename_btn.setEnabled(True)
		else:
			logging.info("Nada")
