# -*- coding: UTF-8 -*-
from . import _, config_root, PLUGIN_BASE, PLUGIN_VERSION

from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.ConfigList import ConfigListScreen
from Components.config import config, getConfigListEntry
from Components.Button import Button
from Components.Label import Label

class SetupWindow(Screen, ConfigListScreen):

    skin="""
        <screen position="center,center" size="560,400" title="openHAB client setup">
            <ePixmap pixmap="skin_default/buttons/red.png" position="0,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />
            <ePixmap pixmap="skin_default/buttons/green.png" position="140,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />
            <widget name="key_red" position="0,0" zPosition="1" size="140,40" 
                font="Regular;20" valign="center" halign="center" backgroundColor="#9f1313" transparent="1"
                shadowColor="#000000" shadowOffset="-1,-1" />
            <widget name="key_green" position="140,0" zPosition="1" size="140,40"
                font="Regular;20" valign="center" halign="center" backgroundColor="#1f771f" transparent="1"
                shadowColor="#000000" shadowOffset="-1,-1" />
            <widget name="config" position="10,40" size="540,320" scrollbarMode="showOnDemand" />
            <widget name="info" position="10,370" size="540,20" zPosition="4" font="Regular;18" foregroundColor="#cccccc" />
        </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        
        self.list = [
            getConfigListEntry(_("Host"), config_root.host),
            getConfigListEntry(_("Port"), config_root.port),
            getConfigListEntry(_("User"), config_root.user),
            getConfigListEntry(_("Password"), config_root.password),
            getConfigListEntry(_("Sitemap"), config_root.sitemap),
            getConfigListEntry(_("Enable debug"), config_root.debug),
        ]
        ConfigListScreen.__init__(self, self.list)
        
        self["config"].list = self.list
        self["info"] = Label(_("Plugin: %(name)s , Version: %(version)s") % dict(name=PLUGIN_BASE, version=PLUGIN_VERSION))

        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Save"))
        self["key_yellow"] = Button(" ")
        self["key_blue"] = Button(" ")

        self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
        {
            "save": self.save,
            "green": self.save,
            "cancel": self.cancel,
            "red": self.cancel,
        }, -2)

    def save(self):
        self.saveAll()
        self.close(True)

    def cancel(self):
        for x in self["config"].list:
            x[1].cancel()
        self.close(False)
