#coding:utf-8
'''
2016.5.12 clz
'''
import wx

from Cura.gui import configBase
from Cura.util import profile
from Cura.util import machineCom

class configDialog(wx.Dialog):

    def __init__(self, parent):
        super(configDialog, self).__init__(None, title=_('C4M config'), style=wx.DEFAULT_DIALOG_STYLE)
        wx.EVT_CLOSE(self, self.OnClose)
        self.parent = parent

        self.panel = configBase.configPanelBase(self)
        self.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        self.GetSizer().Add(self.panel, 1, wx.EXPAND)
        self.nb = wx.Notebook(self.panel)
        self.panel.SetSizer(wx.BoxSizer(wx.VERTICAL))
        self.panel.GetSizer().Add(self.nb, 1, wx.EXPAND)

        self.slicerTab = slicerTab(self.nb, self._update)
        self.machineTab = machineTab(self.nb, self._update)
        self.nb.AddPage(self.slicerTab, "Slicer")
        self.nb.AddPage(self.machineTab, "Machine")
        self.nb.SetSize(self.GetSize())
        # self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self._changed)
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self._changed)
        self.currentTab = 0;

        self.buttonPanel = wx.Panel(self.panel)
        self.panel.GetSizer().Add(self.buttonPanel)

        self.buttonPanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))

        self.okButton = wx.Button(self.buttonPanel, -1, 'Ok')
        self.okButton.Bind(wx.EVT_BUTTON, lambda e: self.Close(), self.okButton)
        self.buttonPanel.GetSizer().Add(self.okButton, flag=wx.ALL, border=5)

        # self.cancelButton = wx.Button(self.buttonPanel, -1, 'Cancel')
        # self.cancelButton.Bind(wx.EVT_BUTTON, lambda e: self.OnCancel())
        # self.buttonPanel.GetSizer().Add(self.cancelButton, flag=wx.ALL, border=5)
        # self.applyButton = wx.Button(self.buttonPanel, -1, 'Apply')
        # self.applyButton.Bind(wx.EVT_BUTTON, lambda e: self.OnApply())
        # self.buttonPanel.GetSizer().Add(self.applyButton, flag=wx.ALL, border=5)

        self.nb.Fit()
        self.Fit()

    def OnClose(self, e):
        self.Destroy()

    def ChangeTab(self):
        self.nb.SetSelection(1)

    def _changed(self, e):
        # self.currentTab=self.currentTab+1
        # if self.currentTab==2: self.currentTab=0
        # print(self.currentTab)
        pass

    def _update(self):
        # del self.slicerTab
        # self.slicerTab = slicerTab(self.nb, self._update)
        # del self.machineTab
        # self.machineTab = machineTab(self.nb, self._update)
        # self.nb.DeleteAllPages()
        # self.nb.AddPage(self.slicerTab, "Slicer")
        # self.nb.AddPage(self.machineTab, "Machine")
        # self.nb.Page
        # self.nb.SetSelection(self.currentTab)
        # if self.currentTab == 0:
        # if self.currentTab==1:
        pass

    # def OnCancel(self, e):
    #     pass
    #
    # def OnApply(self, e):
    #     pass

class slicerTab(configBase.configPanelBase):
    def __init__(self, parent, callback):
        super(slicerTab, self).__init__(parent, callback)
        self._callback = callback

        self.panel = configBase.configPanelBase(self, callback)
        left, right, main = self.panel.CreateConfigPanel(self)

        configBase.TitleRow(left, 'Material')
        radiobutton_panel = left
        self.pla_button = wx.RadioButton(radiobutton_panel, -1, 'PLA', style=wx.RB_GROUP)
        self.abs_button = wx.RadioButton(radiobutton_panel, -1, 'ABS')
        self.tpu_button = wx.RadioButton(radiobutton_panel, -1, 'TPU')
        material=profile.getPreference('simpleModeMaterial')
        if material=='PLA':
            self.pla_button.SetValue(True)
        elif material == 'ABS':
            self.abs_button.SetValue(True)
        elif material == 'TPU':
            self.tpu_button.SetValue(True)

        sizer = radiobutton_panel.GetSizer()
        radiobutton_panel.GetSizer().Add(self.pla_button, (sizer.GetRows(), 0), border=10,
                                    flag=wx.LEFT)
        sizer.SetRows(sizer.GetRows() + 1)
        radiobutton_panel.GetSizer().Add(self.abs_button, (sizer.GetRows(), 0), border=10,
                                    flag=wx.LEFT)
        sizer.SetRows(sizer.GetRows() + 1)
        radiobutton_panel.GetSizer().Add(self.tpu_button, (sizer.GetRows(), 0), border=10,
                                    flag=wx.LEFT)
        sizer.SetRows(sizer.GetRows() + 1)

        configBase.TitleRow(left, 'Basic')
        self.layer_height = configBase.SettingRow(left, 'layer_height')
        self.wall_thickness = configBase.SettingRow(left, 'wall_thickness')
        self.print_temperature = configBase.SettingRow(left, 'print_temperature')
        self.print_speed = configBase.SettingRow(left, 'print_speed')

        configBase.TitleRow(left, 'Advanced')
        self.print_bed_temperature=configBase.SettingRow(left,'print_bed_temperature')
        self.support = configBase.SettingRow(left, 'support')
        self.platform_adhesion = configBase.SettingRow(left, 'platform_adhesion')
        self.fill_density = configBase.SettingRow(left, 'fill_density')
        self.retraction_enable = configBase.SettingRow(left, 'retraction_enable')

        self.pla_button.Bind(wx.EVT_RADIOBUTTON, self._update)
        self.abs_button.Bind(wx.EVT_RADIOBUTTON, self._update)
        self.tpu_button.Bind(wx.EVT_RADIOBUTTON, self._update)

        main.Fit()

    def _update(self, e):
        if self.pla_button.GetValue():
            profile.putPreference('simpleModeMaterial','PLA')
            profile.putProfileSetting('print_temperature', '205')
            profile.putProfileSetting('print_bed_temperature', '0')
            profile.putProfileSetting('print_speed', '80')
            profile.putProfileSetting('inset0_speed', '50')
            profile.putProfileSetting('infill_speed', '0')
            profile.putProfileSetting('raft_airgap', '0.1')
            self.print_temperature.SetValue('205')
            self.print_bed_temperature.SetValue('0')
            self.print_speed.SetValue('80')
            # self.inset0_speed.SetValue('50')
            # self.infill_speed.SetValue('0')
            # self.raft_airgap.SetValue('0.1')
        elif self.abs_button.GetValue():
            profile.putPreference('simpleModeMaterial', 'ABS')
            profile.putProfileSetting('print_temperature', '235')
            profile.putProfileSetting('print_bed_temperature', '60')
            profile.putProfileSetting('print_speed', '80')
            profile.putProfileSetting('inset0_speed', '50')
            profile.putProfileSetting('infill_speed', '0')
            profile.putProfileSetting('raft_airgap', '0.05')
            self.print_temperature.SetValue('235')
            self.print_bed_temperature.SetValue('60')
            self.print_speed.SetValue('80')
            # self.inset0_speed.SetValue('50')
            # self.infill_speed.SetValue('0')
            # self.raft_airgap.SetValue('0.05')
        elif self.tpu_button.GetValue():
            profile.putPreference('simpleModeMaterial', 'TPU')
            profile.putProfileSetting('print_temperature', '235')
            profile.putProfileSetting('print_bed_temperature', '0')
            profile.putProfileSetting('print_speed', '50')
            profile.putProfileSetting('inset0_speed', '40')
            profile.putProfileSetting('infill_speed', '60')
            profile.putProfileSetting('raft_airgap', '0.05')
            self.print_temperature.SetValue('235')
            self.print_bed_temperature.SetValue('0')
            self.print_speed.SetValue('50')
            # self.inset0_speed.SetValue('40')
            # self.infill_speed.SetValue('60')
            # self.raft_airgap.SetValue('0.05')

        self._callback()

class machineTab(configBase.configPanelBase):
    def __init__(self, parent, callback):
        super(machineTab, self).__init__(parent, callback)
        self._callback = callback

        self.panel = configBase.configPanelBase(self, callback)
        self.left, self.right, self.main = self.panel.CreateConfigPanel(self)

        configBase.TitleRow(self.left, 'Model')
        radiobutton_panel = self.left
        self.sail_button = wx.RadioButton(radiobutton_panel, -1, 'mostfun Sail', style=wx.RB_GROUP)
        self.pro_button = wx.RadioButton(radiobutton_panel, -1, 'mostfun Pro')
        machine_name = profile.getMachineSetting('machine_name')
        if machine_name == 'mostfun Sail':
            self.sail_button.SetValue(True)
        elif machine_name == 'mostfun Pro':
            self.pro_button.SetValue(True)

        sizer = radiobutton_panel.GetSizer()
        sizer.Add(self.sail_button, (sizer.GetRows(), 0), border=10,flag=wx.LEFT)
        sizer.SetRows(sizer.GetRows() + 1)
        sizer.Add(self.pro_button, (sizer.GetRows(), 0), border=10,flag=wx.LEFT)
        sizer.SetRows(sizer.GetRows() + 1)

        configBase.TitleRow(self.left, 'Building size')
        self.machine_width = configBase.SettingRow(self.left, 'machine_width')
        self.machine_depth = configBase.SettingRow(self.left, 'machine_depth')
        self.machine_height = configBase.SettingRow(self.left, 'machine_height')


        #连接设置，包含 sail串口设置 & pro网络设置
        # self.connection_setting = wx.Panel(self.panel)
        # sizer=self.panel.GetSizer()
        #
        # sizer.Add(self.connection_setting,(sizer.GetRows(), 0))
        # sizer.SetRows(sizer.GetRows() + 1)
        # # sizer.Layout()
        #
        # # self.connection_setting = wx.Panel(self.left)
        # # sizer = wx.GridBagSizer(2, 2)
        # self.connection_setting.SetSizer(sizer)

        # if machine_name == 'mostfun Sail':

        # 添加mostfun Sail 串口选择
        self.Cs_title = configBase.TitleRow(self.left, _("Communication settings"))
        self.serial_port = configBase.configRow(self.left, 'serial_port', ['AUTO'] + machineCom.serialList())
        self.serial_baud = configBase.configRow(self.left, 'serial_baud', ['AUTO'] + map(str, machineCom.baudrateList()))
        # self.serial_port = configBase.SettingRow(self.left, 'serial_port',['AUTO'] + machineCom.serialList())

        # elif machine_name == 'mostfun Pro':

        # 添加mostfun Pro 地址及密码配置
        self.Ns_title = configBase.TitleRow(self.left, _("Network settings"))
        # configBase.SettingRow(left, 'serial_port', ['AUTO'] + machineCom.serialList())
        # configBase.SettingRow(left, 'serial_baud', ['AUTO'] + map(str, machineCom.baudrateList()))

        if machine_name == 'mostfun Sail':
            self.Ns_title.Hide()

            self.Cs_title.Show()
            self.serial_baud.Show()
            self.serial_port.Show()
        elif machine_name == 'mostfun Pro':
            self.Cs_title.Hide()
            self.serial_baud.Hide()
            self.serial_port.Hide()

            self.Ns_title.Show()
        self.left.Layout()

        self.sail_button.Bind(wx.EVT_RADIOBUTTON, self._update)
        self.pro_button.Bind(wx.EVT_RADIOBUTTON, self._update)

        # sizer.Layout()

        self.main.Fit()

    def _update(self, e):
        if self.sail_button.GetValue():
            profile.putMachineSetting('machine_width', '130')
            profile.putMachineSetting('machine_depth', '130')
            profile.putMachineSetting('machine_height', '110')
            self.machine_width.SetValue('130')
            self.machine_depth.SetValue('130')
            self.machine_height.SetValue('110')
            profile.putMachineSetting('machine_name', 'mostfun Sail')
            profile.putMachineSetting('machine_type', 'mostfun')
            profile.putMachineSetting('has_heated_bed', 'False')
            profile.putMachineSetting('extruder_amount', '1')

            self.Ns_title.Hide()

            self.Cs_title.Show()
            self.serial_baud.Show()
            self.serial_port.Show()

            # self.panel.Layout()
            self.left.Layout()
            # self.panel.GetSizer.Layout()

        if self.pro_button.GetValue():
            profile.putMachineSetting('machine_width', '220')
            profile.putMachineSetting('machine_depth', '180')
            profile.putMachineSetting('machine_height', '155')
            self.machine_width.SetValue('220')
            self.machine_depth.SetValue('180')
            self.machine_height.SetValue('155')
            profile.putMachineSetting('machine_name', 'mostfun Pro')
            profile.putMachineSetting('machine_type', 'mostfun')
            profile.putMachineSetting('has_heated_bed', 'True')

            self.Cs_title.Hide()
            self.serial_baud.Hide()
            self.serial_port.Hide()
            self.Ns_title.Show()

            # self.panel.Layout()
            self.left.Layout()

        self._callback()


