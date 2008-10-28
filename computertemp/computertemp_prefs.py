# -*- coding: UTF-8 -*-

"""
Copyright (C) 2005-2008 Adolfo González Blázquez <code@infinicode.org>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

If you find any bugs or have any suggestions email: code@infinicode.org
"""

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from computertemp import computertemp_globals as glob

class ComputertempPrefs:

    def __init__(self, app):
        
        self.app = app
        self.preferences_create()

        
    def preferences_create(self):
        self.prefs_window = gtk.Window()
        self.prefs_window.set_title(_('Computer Temperature Monitor Preferences'))
        self.prefs_window.set_default_size(300,50)
        self.prefs_window.set_resizable(False)
        self.prefs_window.set_border_width(12)
        self.prefs_window.set_icon_from_file(glob.pixmaps_dir + "/temp_00.png")
        self.prefs_window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.prefs_window.connect("delete-event", self.preferences_delete)
        
        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_TOP)
        self.notebook.show()
        
        self.create_display_tab()
        self.create_log_tab()
        self.create_alarm_tab()
        
        closebutton = gtk.Button(stock=gtk.STOCK_CLOSE)
        closebutton.connect('clicked', self.button_close_clicked)
        closebutton.set_flags(gtk.CAN_DEFAULT)
        
        buttonbox = gtk.HButtonBox()
        buttonbox.set_spacing(12)
        buttonbox.set_layout(gtk.BUTTONBOX_END)
        buttonbox.pack_start(closebutton)
        
        mainvbox = gtk.VBox()
        mainvbox.set_spacing(12)
        mainvbox.pack_start(self.notebook, expand=True)
        mainvbox.pack_start(buttonbox, expand=False)
        self.prefs_window.add(mainvbox)
        
        closebutton.grab_focus()
        closebutton.grab_default()
        
    # Callback: Preferences OK clicked
    def button_close_clicked(self, widget):

        self.app.log_filename = self.logentry.get_text()
        self.app.setlogfilename()

        self.app.log_info = self.logformat_entry.get_text()
        self.app.setloginfo()
        
        self.app.thermalzone = self.thermalcombo.get_active()
        self.app.timeout = self.spintime.get_value_as_int()*1000
        self.app.min_temp = self.spinmin.get_value_as_int()
        self.app.max_temp = self.spinmax.get_value_as_int()
        self.app.alarm_limit = self.alarm_limit_spin.get_value_as_int()
        self.app.alarm_command = self.alarm_command_entry.get_text()
        
        self.app.gconf.save_prefs_all()
        self.preferences_hide()
        
        
    # Callback: Preferences Hardware Sensor combobox changed
    def sensorcombo_changed(self, widget):
        if self.app.sensor !=  widget.get_active():
            self.app.sensor =  widget.get_active()
            self.app.thermalzone = 0
            
            try:
                self.app.tempmon.set_sensor_active(self.app.tempmon.sensors[widget.get_active()][0])
            except IndexError: pass
            
            while self.thermalcombo.get_active_text() != None:
                self.thermalcombo.remove_text(self.thermalcombo.get_active())
                self.thermalcombo.set_active(self.thermalcombo.get_active()+1)
            
            if self.app.tempmon_enabled:
                for i in xrange(len(self.app.thermal_zones)):
                    self.thermalcombo.append_text(self.app.tempmon.get_zone_display_name(i))
            else:
                self.thermalcombo.append_text(_('No Thermal zones!'))
            self.thermalcombo.set_active(0)
            
            self.app.tempzone = 0    # Reset internal thermal zone for icon display
            self.app.update_icon()
            self.app.update_text()
            self.app.update_tooltip()
            self.app.gconf.save_prefs_sensor()
        
        
    # Callback: Preferences Thermal file combobox changed
    def thermalcombo_changed(self, widget):
    	self.app.tempzone = 0    # Reset internal thermal zone for icon display
        self.app.thermalzone = widget.get_active()
        self.app.update_icon()
        self.app.update_text()
        self.app.update_tooltip()
        self.app.gconf.save_prefs_thermalzone()

    # Callback: Preferences display mode combobox changed
    def dispcombo_changed(self, widget):
        self.app.visualization_mode = widget.get_active()
        self.app.update_icon()
        self.app.update_text()
        self.app.update_tooltip()
        self.app.gconf.save_prefs_visualization_mode()
        
    # Callback: Preferences display units combobox changed
    def unitscombo_changed(self, widget):
        self.app.visualization_units = widget.get_active()    
        self.app.update_icon()
        self.app.update_text()
        self.app.update_tooltip()
        self.app.gconf.save_prefs_visualization_units()

    # Callback: timeout changed     
    def spintime_changed(self, widget):
        self.app.timeout = self.spintime.get_value_as_int()*1000
        #gobject.source_remove(self.app.timeout_source)
        #self.app.timeout_source = gobject.timeout_add(self.app.timeout, self.app.update_temp)
        self.app.timeout_count = 0
        self.app.gconf.save_prefs_timeout()

    # Callback: min temp changed     
    def spinmin_changed(self, widget):
        temp = widget.get_value_as_int()
        if temp >= self.app.max_temp:
                self.app.min_temp = self.app.max_temp - 1
                self.spinmin.set_value(self.app.max_temp - 1)
        else:
            self.app.min_temp = widget.get_value_as_int()
        self.app.update_icon()
        self.app.update_text()
        self.app.update_tooltip()
        self.app.gconf.save_prefs_min_temp()
    
    # Callback: max temp changed     
    def spinmax_changed(self, widget):
        temp = widget.get_value_as_int()
        if temp <= self.app.min_temp:
                self.app.max_temp = self.app.min_temp + 1
                self.spinmax.set_value(self.app.min_temp + 1)
        else:
            self.app.max_temp = widget.get_value_as_int()
        self.app.update_icon()
        self.app.update_text()
        self.app.update_tooltip()
        self.app.gconf.save_prefs_max_temp()
        
    # Callback: Check on logging
    def logcheck_toggled(self, widget):
        self.app.logging = self.logcheck.get_active()
        self.autologcheck.set_sensitive(self.app.logging)
        if self.app.logging:
            self.autologcheck.set_active(self.app.autologname)
            self.logtime_label.set_sensitive(True)
            self.logtime_spin.set_sensitive(True)
            self.loglabel.set_sensitive(True)
            self.logentry.set_sensitive(not self.app.autologname)
            self.logformat_label.set_sensitive(True)
            self.logformat_entry.set_sensitive(True)
            self.lognamelabel.set_sensitive(True)
            self.loginfolabel.set_sensitive(True)
            parsedlogname = self.app.parselogfilename(self.app.log_filename)
            self.lognamelabel.set_markup('<small><i><b>Log: </b>'+parsedlogname+'</i></small>')
            parsedinfo = self.app.parseloginfo(self.app.log_info)
            self.loginfolabel.set_markup('<small><i><b>Log info: </b>'+parsedinfo+'</i></small>')
        else:
            self.logtime_label.set_sensitive(False)
            self.logtime_spin.set_sensitive(False)
            self.loglabel.set_sensitive(False)
            self.logentry.set_sensitive(False)
            self.lognamelabel.set_text('')
            self.loginfolabel.set_text('')
            self.logformat_label.set_sensitive(False)
            self.logformat_entry.set_sensitive(False)
        self.app.gconf.save_prefs_logging()
    
    
    # Callback: Check on auto log name
    def autologcheck_toggled(self, widget):
        self.app.autologname = self.autologcheck.get_active()
        self.app.setlogfilename()
        #self.loglabel.set_sensitive(not self.app.autologname)
        self.logentry.set_text(self.app.log_filename)
        self.logentry.set_sensitive(not self.app.autologname)
        self.app.gconf.save_prefs_autologname()
        
    def logtime_spin_changed(self, widget):
        self.app.timeout_log = widget.get_value_as_int() * 1000
        self.app.timeout_log_count = 0
        self.app.gconf.save_prefs_timeout_log()
        #self.app.reset_alarm()
        
    # Callback: log filename entry has changed
    def logentry_changed(self, widget):
        text = self.logentry.get_text()
        if text != '':
            parsedlogname = self.app.parselogfilename(text)
        else:
            parsedlogname = self.app.parselogfilename(self.app.log_filename_default)
        self.lognamelabel.set_markup('<small><i><b>Log: </b>'+parsedlogname+'</i></small>')
        
        
    def logformat_changed(self, widget):
        text = self.logformat_entry.get_text()
        if text != '':
            parsedloginfo = self.app.parseloginfo(text)
        else:
            parsedloginfo = self.app.parseloginfo(self.app.log_info_default)
        self.loginfolabel.set_markup('<small><i><b>Log format: </b>'+parsedloginfo+'</i></small>')
        
        
    def alarm_enabled_check_toggled(self, widget):    
        self.app.alarm_enabled = self.alarm_enabled_check.get_active()
        self.alarm_command_label.set_sensitive(self.app.alarm_enabled)
        self.alarm_command_entry.set_sensitive(self.app.alarm_enabled)
        self.alarm_limit_label.set_sensitive(self.app.alarm_enabled)
        self.alarm_limit_spin.set_sensitive(self.app.alarm_enabled)
        self.alarm_when_label.set_sensitive(self.app.alarm_enabled)
        self.alarm_when_combo.set_sensitive(self.app.alarm_enabled)
        self.alarm_repeat_check.set_sensitive(self.app.alarm_enabled)
        self.app.gconf.save_prefs_alarm_enabled()
        self.app.reset_alarm()
        self.app.menu_set()
        
    def alarm_limit_spin_changed(self, widget):
        self.app.alarm_limit = widget.get_value_as_int()
        self.app.gconf.save_prefs_alarm_limit()
        self.app.reset_alarm()
        
    def alarm_when_combo_changed(self, widget):
        self.app.alarm_when = widget.get_active()    
        self.app.gconf.save_prefs_alarm_when()
        self.app.reset_alarm()
        
    def alarm_repeat_check_toggled(self, widget):    
        self.app.alarm_repeat = self.alarm_repeat_check.get_active()
        self.app.gconf.save_prefs_alarm_repeat()
        self.app.reset_alarm()
    
    def preferences_show(self, event,data=None):
        self.prefs_window.show_all()
        
    def preferences_hide(self):
        self.prefs_window.hide()
        
    def preferences_delete(self, widget, data=None):
        self.preferences_create()
        return False


    def populate_sensor_combobox(self):
        
        if self.app.tempmon_enabled:
            for i in xrange(len(self.app.tempmon.sensors)):
                self.sensorcombo.append_text(self.app.tempmon.sensors[i][0])
            self.sensorcombo.set_active(self.app.sensor)
        else:
            self.sensorcombo.append_text(_('No Thermal zones!'))
            self.sensorcombo.set_active(0)

    def populate_thermal_combobox(self):

        if self.app.tempmon_enabled:
            for i in xrange(len(self.app.thermal_zones)):
                self.thermalcombo.append_text(self.app.tempmon.get_zone_display_name(i))
            self.thermalcombo.set_active(self.app.thermalzone)
        else:
            self.thermalcombo.append_text(_('No Thermal zones!'))
            self.thermalcombo.set_active(0)
        

    # Display preferences
    def create_display_tab(self):

        sizegroup1 = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)            
        sizegroup2 = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)    

        # Thermal Zone frame
        temp_frame = gtk.Frame()
        temp_frame.set_shadow_type(gtk.SHADOW_NONE)
        temp_frame_label = gtk.Label(_('<b>Thermal Zone Configuration</b>'))
        temp_frame_label.set_alignment(xalign=0, yalign=0.5)
        temp_frame_label.set_use_markup(True)
        temp_frame_alig = gtk.Alignment(0.5,0.5,1,1)
        temp_frame_alig.set_padding(6,0,12,0)    
        temp_frame.set_label_widget(temp_frame_label)
        temp_frame.add(temp_frame_alig)
        
        # Select Sensor to monitor
        sensorlabel = gtk.Label(_('Select Sensor to monitor:'))
        sensorlabel.set_alignment(xalign=0, yalign=0.5)
        self.sensorcombo = gtk.combo_box_new_text()
        self.thermalcombo = gtk.combo_box_new_text()
        
        self.sensorcombo.connect("changed",self.sensorcombo_changed)
        self.thermalcombo.connect("changed",self.thermalcombo_changed)
        
        self.populate_sensor_combobox()

        sensor_hbox = gtk.HBox()
        sensor_hbox.set_spacing(12)
        sensor_hbox.pack_start(sensorlabel)
        sensor_hbox.pack_start(self.sensorcombo)
        
        sizegroup1.add_widget(sensorlabel)        
        sizegroup2.add_widget(self.sensorcombo)
        
        # Select thermal zone
        thermallabel = gtk.Label(_('Select Thermal Zone:'))
        thermallabel.set_alignment(xalign=0, yalign=0.5)
        self.thermalcombo = gtk.combo_box_new_text()
        self.thermalcombo.connect("changed",self.thermalcombo_changed)

        self.populate_thermal_combobox()
            
        thermal_hbox = gtk.HBox()
        thermal_hbox.set_spacing(12)
        thermal_hbox.pack_start(thermallabel)
        thermal_hbox.pack_start(self.thermalcombo)
        
        sizegroup1.add_widget(thermallabel)        
        sizegroup2.add_widget(self.thermalcombo)
        
        thermal_vbox = gtk.VBox()
        thermal_vbox.set_spacing(12)
        thermal_vbox.pack_start(sensor_hbox, expand=False)
        thermal_vbox.pack_start(thermal_hbox, expand=False)
        
        temp_frame_alig.add(thermal_vbox)
        
        #################################
        # Display options frame
        disp_frame = gtk.Frame()
        disp_frame.set_shadow_type(gtk.SHADOW_NONE)
        disp_frame_label = gtk.Label(_('<b>Display Configuration</b>'))
        disp_frame_label.set_alignment(xalign=0, yalign=0.5)
        disp_frame_label.set_use_markup(True)
        disp_frame_alig = gtk.Alignment(0.5,0.5,1,1)
        disp_frame_alig.set_padding(6,0,12,0)    
        disp_frame.set_label_widget(disp_frame_label)
        disp_frame.add(disp_frame_alig)
        
        # Display mode
        dispmodelabel = gtk.Label(_('Display mode:'))
        dispmodelabel.set_alignment(xalign=0, yalign=0.5)
        self.dispcombo = gtk.combo_box_new_text()
        self.dispcombo.connect("changed",self.dispcombo_changed)
        self.dispcombo.append_text(_('Graphic'))
        self.dispcombo.append_text(_('Text'))
        self.dispcombo.append_text(_('Graphic and Text'))
        self.dispcombo.set_active(self.app.visualization_mode)
        dispcombo_hbox = gtk.HBox()
        dispcombo_hbox.set_spacing(12)
        dispcombo_hbox.add(dispmodelabel)
        dispcombo_hbox.add(self.dispcombo)

        sizegroup1.add_widget(dispmodelabel)        
        sizegroup2.add_widget(self.dispcombo)
        
        # Display units
        unitslabel = gtk.Label(_('Display units:'))
        unitslabel.set_alignment(xalign=0, yalign=0.5)
        self.visualization_unitscombo = gtk.combo_box_new_text()
        self.visualization_unitscombo.connect("changed",self.unitscombo_changed)
        self.visualization_unitscombo.append_text(_('Celsius %s') % "°C")
        self.visualization_unitscombo.append_text(_('Fahrenheit %s') % "°F")
        self.visualization_unitscombo.set_active(self.app.visualization_units)
        unitscombo_hbox = gtk.HBox()
        unitscombo_hbox.set_spacing(12)
        unitscombo_hbox.add(unitslabel)
        unitscombo_hbox.add(self.visualization_unitscombo)

        sizegroup1.add_widget(unitslabel)        
        sizegroup2.add_widget(self.visualization_unitscombo)
        
        # Update time
        updatelabel = gtk.Label(_('Update every (secs):'))
        updatelabel.set_alignment(xalign=0, yalign=0.5)
        updatelabel.set_width_chars(20)
        adj = gtk.Adjustment(self.app.timeout/1000, 1.0, 3600.0, 1.0, 5.0, 0.0)
        self.spintime = gtk.SpinButton(adj, 0, 0)
        self.spintime.connect('value_changed',self.spintime_changed)
        update_hbox = gtk.HBox()
        update_hbox.set_spacing(12)
        update_hbox.pack_start(updatelabel)
        update_hbox.pack_start(self.spintime)
        
        sizegroup1.add_widget(updatelabel)        
        sizegroup2.add_widget(self.spintime)

        # Min temp
        mintemplabel = gtk.Label(_('Minimal Temperature:'))
        mintemplabel.set_alignment(xalign=0, yalign=0.5)
        adjmin = gtk.Adjustment(self.app.min_temp, 1.0, 200.0, 1.0, 5.0, 0.0)
        self.spinmin = gtk.SpinButton(adjmin, 0, 0)
        self.spinmin.connect('value_changed',self.spinmin_changed)
        mintemp_hbox = gtk.HBox()
        mintemp_hbox.set_spacing(12)
        mintemp_hbox.pack_start(mintemplabel)
        mintemp_hbox.pack_start(self.spinmin)    
        
        sizegroup1.add_widget(mintemplabel)        
        sizegroup2.add_widget(self.spinmin)
        
        # Max temp
        maxtemplabel = gtk.Label(_('Maximal Temperature:'))
        maxtemplabel.set_alignment(xalign=0, yalign=0.5)
        adjmax = gtk.Adjustment(self.app.max_temp, 1.0, 200.0, 1.0, 5.0, 0.0)
        self.spinmax = gtk.SpinButton(adjmax, 0, 0)
        self.spinmax.connect('value_changed',self.spinmax_changed)
        maxtemp_hbox = gtk.HBox()
        maxtemp_hbox.set_spacing(12)
        maxtemp_hbox.pack_start(maxtemplabel)
        maxtemp_hbox.pack_start(self.spinmax)
        
        sizegroup1.add_widget(maxtemplabel)        
        sizegroup2.add_widget(self.spinmax)    
        
        disp_vbox = gtk.VBox()
        disp_vbox.set_spacing(12)
        disp_vbox.pack_start(dispcombo_hbox, expand=False)
        disp_vbox.pack_start(unitscombo_hbox, expand=False)
        disp_vbox.pack_start(update_hbox, expand=False)
        disp_vbox.pack_start(mintemp_hbox, expand=False)
        disp_vbox.pack_start(maxtemp_hbox, expand=False)
        disp_frame_alig.add(disp_vbox)
        
        # Main VBox
        main_vbox = gtk.VBox()
        main_vbox.set_spacing(12)
        main_vbox.set_border_width(12)
        main_vbox.pack_start(temp_frame, expand=False)
        main_vbox.pack_start(disp_frame, expand=False)
        
        tablabel = gtk.Label(_('Display'))
        self.notebook.append_page(main_vbox, tablabel)

    
    def create_log_tab(self):

        log_frame = gtk.Frame()
        log_frame.set_shadow_type(gtk.SHADOW_NONE)
        log_frame.set_border_width(12)
        log_frame_label = gtk.Label(_('<b>Logging Configuration</b>'))
        log_frame_label.set_alignment(xalign=0, yalign=0.5)
        log_frame_label.set_use_markup(True)
        log_frame_alig = gtk.Alignment(0.5,0.5,1,1)
        log_frame_alig.set_padding(6,0,12,0)    
        log_frame.set_label_widget(log_frame_label)
        log_frame.add(log_frame_alig)
        
        # Log text entry
        self.logcheck = gtk.CheckButton(_('Log temperatures to a text file'))
        self.logcheck.set_active(self.app.logging)
        
        self.autologcheck = gtk.RadioButton(None, _('Use date for log file name'))
        self.autologcheck.set_active(self.app.autologname)
        self.autologcheck.set_sensitive(self.app.logging)
        
        self.logtime_label = gtk.Label(_('Update log every (seconds):'))
        self.logtime_label.set_alignment(xalign=0, yalign=0.5)
        adj = gtk.Adjustment(self.app.timeout_log/1000, 1.0, 3600.0, 1.0, 5.0, 0.0)
        self.logtime_spin = gtk.SpinButton(adj, 0, 0)
        self.logtime_label.set_sensitive(self.app.logging)
        self.logtime_spin.set_sensitive(self.app.logging)
        logtimehbox = gtk.HBox()
        logtimehbox.set_spacing(12)
        logtimehbox.pack_start(self.logtime_label)
        logtimehbox.pack_start(self.logtime_spin)
        
        self.loglabel = gtk.RadioButton(self.autologcheck, _('Set path for log file manually'))
        self.loglabel.set_active(not self.app.autologname)
        self.loglabel.set_sensitive(self.app.logging)
        
        self.logentry = gtk.Entry()    
        self.logentry.set_text(self.app.log_filename)
        self.logentry.set_sensitive(not self.app.autologname and self.app.logging)
        self.logentry.set_activates_default(True)
        
        self.logentrytooltip = gtk.Tooltips()
        self.logentrytooltip.set_tip(self.logentry, self.app.tips_logname)
        
        self.lognamelabel = gtk.Label()
        self.lognamelabel.set_use_markup(True)
        self.lognamelabel.set_alignment(xalign=0, yalign=0.5)
        parsedlogname = self.app.parselogfilename(self.app.log_filename)
        if self.app.logging:
            self.lognamelabel.set_markup('<small><i><b>Log: </b>'+parsedlogname+'</i></small>')

        # Log format
        self.logformat_label = gtk.Label(_('Log format:'))
        self.logformat_label.set_alignment(xalign=0, yalign=0.5)
        self.logformat_label.set_sensitive(self.app.logging)
        
        self.logformat_entry = gtk.Entry()
        self.logformat_entry.set_text(self.app.log_info)
        self.logformat_entry.set_sensitive(self.app.logging)
        self.logformat_entry.set_activates_default(True)
        
        self.logformattooltip = gtk.Tooltips()
        self.logformattooltip.set_tip(self.logformat_entry, self.app.tips_loginfo)
        
        logformathbox = gtk.HBox()
        logformathbox.set_spacing(12)
        logformathbox.pack_start(self.logformat_label, expand=False)
        logformathbox.pack_start(self.logformat_entry, expand=True)
        
        self.loginfolabel = gtk.Label()
        self.loginfolabel.set_use_markup(True)
        self.loginfolabel.set_alignment(xalign=0, yalign=0.5)
        parsedinfo = self.app.parseloginfo(self.app.log_info)
        if self.app.logging:
            self.loginfolabel.set_markup('<small><i><b>Log info: </b>'+parsedinfo+'</i></small>')
        
        # Signal handlers
        self.logcheck.connect('toggled',self.logcheck_toggled)
        self.autologcheck.connect("toggled",self.autologcheck_toggled)
        self.logtime_spin.connect('value_changed',self.logtime_spin_changed)
        self.logentry.connect('changed', self.logentry_changed)
        self.logformat_entry.connect('changed', self.logformat_changed)

        
        log_filename_vbox = gtk.VBox()
        log_filename_vbox.set_spacing(12)
        log_filename_vbox.pack_start(logtimehbox)
        log_filename_vbox.pack_start(self.autologcheck)
        log_filename_vbox.pack_start(self.loglabel)
        log_filename_vbox.pack_start(self.logentry)
        log_filename_vbox.pack_start(self.lognamelabel)
        log_filename_vbox.pack_start(logformathbox)
        log_filename_vbox.pack_start(self.loginfolabel)
        
        log_filename_alig = gtk.Alignment(0.5,0.5,1,1)
        log_filename_alig.set_padding(6,0,24,0)
        log_filename_alig.add(log_filename_vbox)
        
        log_vbox = gtk.VBox()
        log_vbox.set_spacing(12)
        log_vbox.pack_start(self.logcheck, expand=False)
        log_vbox.pack_start(log_filename_alig, expand=False)
        log_vbox.set_homogeneous(False)

        log_frame_alig.add(log_vbox)
        
        logtablabel = gtk.Label(_('Log'))
        self.notebook.append_page(log_frame, logtablabel)
        
        
    def create_alarm_tab(self):
        
        sizegroup1 = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)            
        sizegroup2 = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL) 
        
        alarm_frame = gtk.Frame()
        alarm_frame.set_shadow_type(gtk.SHADOW_NONE)
        alarm_frame.set_border_width(12)
        alarm_frame_label = gtk.Label(_('<b>Alarm Configuration</b>'))
        alarm_frame_label.set_alignment(xalign=0, yalign=0.5)
        alarm_frame_label.set_use_markup(True)
        alarm_frame_alig = gtk.Alignment(0.5,0.5,1,1)
        alarm_frame_alig.set_padding(6,0,12,0)    
        alarm_frame.set_label_widget(alarm_frame_label)
        alarm_frame.add(alarm_frame_alig)
        
        main_vbox = gtk.VBox()
        main_vbox.set_spacing(12)
        
        # Enable alarm?
        self.alarm_enabled_check = gtk.CheckButton(_('Enable alarm for this sensor?'))
        self.alarm_enabled_check.set_active(self.app.alarm_enabled)
        self.alarm_enabled_check.connect("toggled",self.alarm_enabled_check_toggled)
        
        # Alarm limit
        self.alarm_limit_label = gtk.Label(_('Limit temperature:'))
        self.alarm_limit_label.set_alignment(xalign=0, yalign=0.5)
        self.alarm_limit_label.set_sensitive(self.app.alarm_enabled)
        alarm_limit_adj = gtk.Adjustment(self.app.alarm_limit, -50.0, 200.0, 1.0, 5.0, 0.0)
        self.alarm_limit_spin = gtk.SpinButton(alarm_limit_adj, 0, 0)
        self.alarm_limit_spin.connect('value_changed',self.alarm_limit_spin_changed)
        self.alarm_limit_spin.set_sensitive(self.app.alarm_enabled)
        alarm_limit_hbox = gtk.HBox()
        alarm_limit_hbox.set_spacing(12)
        alarm_limit_hbox.pack_start(self.alarm_limit_label)
        alarm_limit_hbox.pack_start(self.alarm_limit_spin)
        sizegroup1.add_widget(self.alarm_limit_label)        
        sizegroup2.add_widget(self.alarm_limit_spin)
        
        # Raise alarm when...
        self.alarm_when_label = gtk.Label(_('Raise alarm when temperature is:'))
        self.alarm_when_label.set_alignment(xalign=0, yalign=0.5)
        self.alarm_when_label.set_sensitive(self.app.alarm_enabled)
        self.alarm_when_combo = gtk.combo_box_new_text()
        self.alarm_when_combo.connect("changed",self.alarm_when_combo_changed)
        self.alarm_when_combo.append_text(_('smaller than limit'))
        self.alarm_when_combo.append_text(_('greater than limit'))
        self.alarm_when_combo.set_active(self.app.alarm_when)
        self.alarm_when_combo.set_sensitive(self.app.alarm_enabled)
        alarm_when_hbox = gtk.HBox()
        alarm_when_hbox.set_spacing(12)
        alarm_when_hbox.add(self.alarm_when_label)
        alarm_when_hbox.add(self.alarm_when_combo)
        sizegroup1.add_widget(self.alarm_when_label)        
        sizegroup2.add_widget(self.alarm_when_combo)
        
        # Command to execute
        self.alarm_command_label = gtk.Label(_('Enter command to execute:'))
        self.alarm_command_label.set_alignment(xalign=0, yalign=0.5)
        self.alarm_command_label.set_sensitive(self.app.alarm_enabled)
        self.alarm_command_entry = gtk.Entry()
        self.alarm_command_entry.set_text(self.app.alarm_command)
        self.alarm_command_entry.set_sensitive(self.app.alarm_enabled)
        self.alarm_command_entry.set_activates_default(True)
        alarm_command_hbox = gtk.HBox()
        alarm_command_hbox.set_spacing(12)
        alarm_command_hbox.pack_start(self.alarm_command_label)
        alarm_command_hbox.pack_start(self.alarm_command_entry)
        sizegroup1.add_widget(self.alarm_command_label)
        sizegroup2.add_widget(self.alarm_command_entry)
        
        # Repeat the alarm?
        self.alarm_repeat_check = gtk.CheckButton(_('Repeat the alarm command?'))
        self.alarm_repeat_check.set_active(self.app.alarm_enabled)
        self.alarm_repeat_check.connect("toggled",self.alarm_repeat_check_toggled)
        self.alarm_repeat_check.set_sensitive(self.app.alarm_enabled)
        
        second_vbox = gtk.VBox()
        second_vbox.set_spacing(12)
        second_vbox.pack_start(alarm_limit_hbox, expand=False)
        second_vbox.pack_start(alarm_when_hbox, expand=False)
        second_vbox.pack_start(alarm_command_hbox, expand=False)
        second_vbox.pack_start(self.alarm_repeat_check, expand=False)
        
        second_alig = gtk.Alignment(0.5,0.5,1,1)
        second_alig.set_padding(6,0,24,0)
        second_alig.add(second_vbox)
        
        main_vbox.pack_start(self.alarm_enabled_check, expand=False)
        main_vbox.pack_start(second_alig, expand=False)
        
        alarm_frame_alig.add(main_vbox)
        
        alarmlabel = gtk.Label(_('Alarm'))
        self.notebook.append_page(alarm_frame, alarmlabel)
