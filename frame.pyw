# print("file frame.pyw")

import subprocess
import sys
import os
import re
import ensurepip
import time
from threading import Thread
# import logic       # SEE THE END OF FILE
from pathlib import Path
from tkinter import Tk, Frame, Button, Label, BOTH, Listbox, Scrollbar, filedialog, messagebox
from tkinter import ttk

def start_gui():
    root = Tk()
    app = Gui(parent=root)

    app.mainloop()


# #################################################
# GUI
# #################################################
class Gui(Frame):
    """ main GUI window
    parent - object in which you want to place this Execution
    """
    def __init__(self, parent=None):
        super().__init__()
        self.root = self.winfo_toplevel()
        self.parent = parent

        self.logic = logic.Logic(start_scan=False)

        self.create_gui_structure()

        self.gui_root_configure()
        self.window_move_to_center()

    def gui_root_configure(self):
        if self.root != self.parent:      # if it is independent window (without insertion in outside project)
            return

        # IF YOU WANT TO DISABLE - CHANGE TO NONE or COMMENT OUT
        # ROOT_METHODS = many of them can named with WM! geometry=WM_geometry
        self.root.title("NET SCAN (PING)")
        # self.root.iconbitmap(r'ERROR.ico')    =ONLY FILENAME! NO fileobject
        # self.root.protocol('WM_DELETE_WINDOW', self.program_exit)  # intersept gui exit()

        # self.root.geometry("800x500+100+100")           #("WINXxWINY+ShiftX+ShiftY")
        # self.root.geometry("800x500")                 #("WINXxWINY")
        # self.root.geometry("+100+100")                #("+ShiftX+ShiftY")
        # self.root.resizable(width=True, height=True)    # block resizable! even if fullscreen!!!
        # self.root.maxsize(1000, 1000)
        self.root.minsize(800, 500)

        # self.root.overrideredirect(False)   # borderless window, without standard OS header and boarders
        self.root.state('zoomed')   # normal/zoomed/iconic/withdrawn
        # self.root.iconify()       # ICONIFY/deiconify = hide down window, minimize
        # self.root.withdraw()      # WITHDRAW/deiconify = hide out window, don't show anywhere
        # self.root.deiconify()     # restore window

        # WM_ATTRIBUTES = root.wm_attributes / root.attributes
        # self.root.wm_attributes("-topmost", False)
        # self.root.wm_attributes("-disabled", False)     # disable whole gui
        # self.root.wm_attributes("-fullscreen", False)
        # self.root.wm_attributes("-transparentcolor", None)

        # WGT_PARAMETERS = ROOT.CONFIG(bg="red") / ROOT["bg"]="red"
        # self.root["bg"] = "#009900"
        # self.root["fg"] = None
        # self.root["width"] = None
        # self.root["height"] = None
        # self.root["bind"] = None
        self.root["relief"] = "raised"  # "flat"/"sunken"/"raised"/"groove"/"ridge"
        self.root["borderwidth"] = 5
        # self.root["cursor"] = None   # 'watch'=the best / "xterm" / "arrow"=standard
        return

    def window_move_to_center(self):
        if self.root != self.parent:      # if it is independent window (without insertion in outside project)
            return

        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) / 2
        y = (screen_height - window_height) / 2
        self.root.geometry('+%d+%d' % (x, y))
        return

    # #################################################
    # FRAMES
    # #################################################
    def create_gui_structure(self):
        self.color_bg_mainframe()
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure([0, 1, ], weight=0)       # INFO, CONNECTION
        self.parent.rowconfigure([2, 3, ], weight=1)       # VERSIONS, FILES
        self.parent.rowconfigure([4, ], weight=10)         # MODULES
        pad_external = 2

        # ======= FRAME-0 (ADAPTERS) ======================
        self.frame_info = Frame(self.parent)
        self.frame_info.grid(row=0, sticky="nsew", padx=pad_external, pady=2)

        self.fill_frame_info(self.frame_info)

        # ======= FRAME-1 (CONNECTION) ====================
        self.frame_connection = Frame(self.parent)
        self.frame_connection.grid(row=1, sticky="nsew", padx=pad_external, pady=1)

        self.fill_frame_connection(self.frame_connection)

        # ======= FRAME-2 (VERSIONS) ====================
        self.frame_versions = Frame(self.parent)
        self.frame_versions.pack_propagate(0)
        self.frame_versions.grid(row=2, sticky="snew", padx=pad_external, pady=2)

        self.fill_frame_versions(self.frame_versions)

        # ======= FRAME-3 (FILES) ====================
        self.frame_files = Frame(self.parent)
        self.frame_files.pack_propagate(1)
        self.frame_files.grid(row=3, sticky="snew", padx=pad_external, pady=2)

        self.fill_frame_files(self.frame_files)

        # ======= FRAME-4 (MODULES) ====================
        self.frame_modules = Frame(self.parent)
        self.frame_modules.grid(row=4, sticky="snew", padx=pad_external, pady=2)

        self.fill_frame_modules(self.frame_modules)
        return

    def color_bg_mainframe(self):
        self.parent["bg"] = "#009900" if self.logic.count_found_modules_bad == 0 else "#FF0000"

    # #################################################
    # frame INFO
    def fill_frame_info(self, parent):
        btn = Button(parent, text=f"skip\n checking\n modules")
        btn["bg"] = "#aaaaFF"
        btn["command"] = self.root.destroy
        btn["state"] = None if self.root == self.parent else "disabled"
        btn.pack(side="left")

        self.lable_frame_info = Label(parent)
        self.lable_frame_info["font"] = ("", 15)
        self.lable_frame_info.pack(side="left", fill="x", expand=1)
        self._fill_lable_frame_info()
        return

    def _fill_lable_frame_info(self):
        if self.logic.count_found_modules_bad > 0:
            self.lable_frame_info["text"] = f"BAD SITUATION:\nYOU NEED INSTALL some modules"
            self.lable_frame_info["bg"] = "#FF9999"
        else:
            self.lable_frame_info["text"] = f"GOOD:\nALL MODULES ARE PRESENT!"
            self.lable_frame_info["bg"] = "#55FF55"
            return

    # #################################################
    # frame VERSIONS
    def fill_frame_versions(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure([1], weight=1)
        parent.grid_rowconfigure([0, 2], weight=0)

        lable = Label(parent)
        lable["text"] = f"FOUND python [{self.logic.count_python_versions}]VERSIONS:\n" \
                        f"Active .exe=[{sys.executable}]"
        lable.grid(column=0, row=0, columnspan=2, sticky="snew")

        self.listbox_versions = Listbox(parent, height=4, bg=None, font=('Courier', 9))
        self.listbox_versions.grid(column=0, row=1, sticky="snew")

        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.listbox_versions.yview)
        self.scrollbar.grid(column=1, row=1, sticky="sn")

        self.listbox_versions['yscrollcommand'] = self.scrollbar.set

        # STATUS FRAME
        frame_status_version = Frame(parent)
        frame_status_version.grid(column=0, columnspan=2, row=2, sticky="ew")

        btn = Button(frame_status_version, text=f"RESTART by selected")
        btn["bg"] = "#aaaaFF"
        btn["command"] = lambda: self.program_restart(python_exe=self.status_versions["text"]) if self.listbox_versions.curselection() != () else None
        btn.pack(side="left")

        self.status_versions = ttk.Label(frame_status_version, text="...SELECT item...", anchor="w")
        self.status_versions.pack(side="left")
        self.listbox_versions.bind("<<ListboxSelect>>", self.change_status_versions)

        self.fill_listbox_versions()
        return

    def fill_listbox_versions(self):
        self.listbox_versions.delete(0, self.listbox_versions.size()-1)
        versions_dict = self.logic.python_versions_found
        for ver in versions_dict:
            self.listbox_versions.insert('end', ver.ljust(10, " ") + versions_dict[ver][0].ljust(14, " ") + versions_dict[ver][1])
            if ver.endswith("*"):
                if self.logic.count_found_modules_bad == 0:
                    self.listbox_versions.itemconfig('end', bg="#55FF55")
                else:
                    self.listbox_versions.itemconfig('end', bg="#FF9999")
        return

    def change_status_versions(self, event):
        #print(self.listbox_versions.curselection())
        selected_list = (0,) if self.listbox_versions.curselection() == () else self.listbox_versions.curselection()
        selected_version = self.listbox_versions.get(selected_list)
        for ver in self.logic.python_versions_found:
            if selected_version.startswith(ver):
                self.status_versions["text"] = self.logic.python_versions_found[ver][1]
        return

    # #################################################
    # frame FILES
    def fill_frame_files(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure([1], weight=1)
        parent.grid_rowconfigure([0, 2], weight=0)

        self.lable_frame_files = Label(parent)
        self.lable_frame_files.grid(column=0, row=0, columnspan=2, sticky="snew")
        self._fill_lable_frame_files()

        self.listbox_files = Listbox(parent, height=6, bg="#55FF55", font=('Courier', 9))
        self.listbox_files.grid(column=0, row=1, sticky="snew")

        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.listbox_files.yview)
        self.scrollbar.grid(column=1, row=1, sticky="sn")

        self.listbox_files['yscrollcommand'] = self.scrollbar.set

        # STATUS FRAME
        frame_status_files = Frame(parent)
        frame_status_files.grid(column=0, columnspan=2, row=2, sticky="ew")

        btn = Button(frame_status_files, text=f"NEW FileAsLINK")
        btn["bg"] = "#aaaaFF"
        btn["command"] = lambda: self.change_path(mode="file")
        btn.pack(side="left")

        btn = Button(frame_status_files, text=f"NEW PATH")
        btn["bg"] = "#aaaaFF"
        btn["command"] = lambda: self.change_path(mode="folder")
        btn.pack(side="left")

        self.status_files = ttk.Label(frame_status_files, text="...SELECT item...", anchor="w")
        self.status_files.pack(side="left")
        self.listbox_files.bind("<<ListboxSelect>>", self.change_status_files)

        btn = Button(frame_status_files, text=f"TRY without overcount")
        btn["bg"] = "#aaaaFF"
        btn["state"] = "disabled"
        #btn["command"] = lambda: self.logic.count_found_files_overcount_limit = 0;
        btn.pack(side="right")

        self.fill_listbox_files()
        return

    def _fill_lable_frame_files(self):
        lbl = self.lable_frame_files
        mark = "!!!DETECTED OVERCOUNT!!!"
        gap = " "*20
        line1 = f"FOUND python [{self.logic.count_found_files}]FILES:"
        line2 = f"Active link path=[{self.path_link_applied}]"
        if self.logic.count_found_files_overcount:
            line1 = mark + gap + line1 + gap + mark
            lbl["bg"] = "#FF9999"

        lbl["text"] = line1 + "\n" + line2
        return

    def fill_listbox_files(self):
        self.listbox_files.delete(0, self.listbox_files.size()-1)
        files_dict = self.logic.python_files_found_dict
        for file in files_dict:
            file_str = str(file) + " *" if file == Path(self.path_link_applied) else file
            self.listbox_files.insert('end', file_str)
            if not files_dict[file].isdisjoint(self.logic.modules_found_infiles_bad):
                self.listbox_files.itemconfig('end', bg="#FF9999")
        return

    def change_status_files(self, event):
        #print(self.listbox_files.curselection())
        selected_list = (0,) if self.listbox_files.curselection() == () else self.listbox_files.curselection()
        selected_filename = self.listbox_files.get(*selected_list)
        self.status_files["text"] = self.logic.python_files_found_dict[Path(selected_filename.replace(" *", ""))]
        return

    def change_path(self, mode):
        if mode == "file":
            path_new = filedialog.Open(self.root, filetypes=[('*.py* files', '.py*')]).show()
        elif mode == "folder":
            path_new = filedialog.askdirectory()

        if path_new == '':
            return

        self.update_total_gui_data(path_new)
        return

    def update_total_gui_data(self, path_link):
        self.apply_path(path_link)

        self._fill_lable_frame_info()
        self._fill_lable_frame_files()
        self._fill_lable_frame_modules()

        self.fill_listbox_versions()
        self.fill_listbox_files()
        self.fill_listbox_modules()

        self.color_bg_mainframe()
        return

    # #################################################
    # frame MODULES
    def fill_frame_modules(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure([1], weight=10)
        parent.grid_rowconfigure([0, 2], weight=0)

        self.lable_frame_modules = Label(parent)
        self.lable_frame_modules.grid(column=0, row=0, columnspan=2, sticky="snew")
        self._fill_lable_frame_modules()

        self.listbox_modules = Listbox(parent, height=8, bg="#55FF55", font=('Courier', 9))
        self.listbox_modules.grid(column=0, row=1, sticky="snew")

        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.listbox_modules.yview)
        self.scrollbar.grid(column=1, row=1, sticky="sn")

        self.listbox_modules['yscrollcommand'] = self.scrollbar.set

        # STATUS FRAME
        frame_status_modules = Frame(parent)
        frame_status_modules.grid(column=0, columnspan=2, row=2, sticky="ew")

        lbl = Label(frame_status_modules)
        lbl["text"] = f"In ACTIVE python version"
        lbl.pack(side="left")

        btn_module_install = Button(frame_status_modules, text=f"INSTALL")
        btn_module_install["bg"] = "#aaaaFF"
        btn_module_install["command"] = lambda: self.btn_module_action("install")
        btn_module_install.pack(side="left")

        btn_module_upgrade = Button(frame_status_modules, text=f"upgrade")
        btn_module_upgrade["bg"] = "#aaaaFF"
        btn_module_upgrade["command"] = lambda: self.btn_module_action("upgrade")
        btn_module_upgrade.pack(side="left")

        btn_module_delete = Button(frame_status_modules, text=f"DELETE")
        btn_module_delete["bg"] = "#aaaaFF"
        btn_module_delete["command"] = lambda: self.btn_module_action("delete")
        btn_module_delete.pack(side="left")

        lbl = Label(frame_status_modules)
        lbl["text"] = f"module: "
        lbl.pack(side="left")

        self.status_modules = ttk.Label(frame_status_modules, text="...SELECT item...", anchor="w")
        self.status_modules.pack(side="left")
        self.listbox_modules.bind("<<ListboxSelect>>", self.change_status_modules)

        self.fill_listbox_modules()
        self.change_status_modules(None)
        return

    def _fill_lable_frame_modules(self):
        self.lable_frame_modules["text"] = f"FOUND importing [{self.logic.count_found_modules}]MODULES:\n"\
            "(GREEN - Installed, RED - Not installed, LightRED - Definitely can be installed!)"
        return

    def fill_listbox_modules(self):
        self.listbox_modules.delete(0, self.listbox_modules.size()-1)
        for module in self.logic.ranked_modules_dict:
            #[CanImport=True/False, Placement=ShortPathName, InstallNameIfDetected]
            can_import, short_pathname, detected_installname = self.logic.ranked_modules_dict[module]
            bad_module_index = 0
            if can_import:
                self.listbox_modules.insert('end', "%-20s \t[%s]" % (module, short_pathname))
            else:
                self.listbox_modules.insert(bad_module_index, "%-20s \t[%s]" % (module, short_pathname))
                color = "#FF9999" if detected_installname is None else "#FFcc99"
                self.listbox_modules.itemconfig(bad_module_index, bg=color)
                bad_module_index += 1
        return

    def change_status_modules(self, event):
        #print(self.listbox_modules.curselection())
        selected_list = (0,) if self.listbox_modules.curselection() == () else self.listbox_modules.curselection()
        selected_data = self.listbox_modules.get(*selected_list)
        selected_module_w_spaces = selected_data.split("\t")[0]
        self.selected_module = re.sub(r"\s", "", selected_module_w_spaces)
        self.status_modules["text"] = self.selected_module
        return

    def btn_module_action(self, mode):
        if mode not in ("install", "upgrade", "delete"):
            sys.stderr.write("WRONG PARAMETER MODE")
            return
        elif mode == "install":
            mode_cmd = "install"
        elif mode == "upgrade":
            mode_cmd = "install --upgrade"
        elif mode == "delete":
            mode_cmd = "uninstall"

        modulename = self.selected_module
        module_data = self.logic.ranked_modules_dict[self.selected_module]
        modulename_cmd = modulename if module_data[2] is None else module_data[2]

        python_exe = sys.executable

        cmd = f"{python_exe} -m pip {mode_cmd} {modulename_cmd}"
        my_process = subprocess.Popen(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

        if mode == "delete":
            my_stdout, my_stderr = my_process.communicate(input="y")
        else:
            my_stdout = my_process.stdout.readlines()
            my_stderr = my_process.stderr.readlines()
            my_process.wait()

        # print(my_stdout, my_stderr)
        if my_stderr in ([], "") and my_process.poll() == 0:
            self.logic.rank_modules_dict()  # update data
            self.logic.generate_modules_found_infiles_bad()
            self.fill_listbox_modules()
            self.fill_listbox_files()
            #self.program_restart()
        else:
            txt = f"Can't {mode.upper()} module.\n"\
                    "Мay be it is already IN_TARGET position or have ERROR.\n"\
                    + "*"*50 + "\n"\
                    f"stdout={my_stdout}\n\n"\
                    f"stderr={my_stderr}"
            messagebox.showinfo(title='INFO', message=txt)
        return


if __name__ == '__main__':
    access_this_module_as_import = False
    import logic
    start_gui()
else:
    from . import logic
    access_this_module_as_import = True
