# -*- coding: UTF-8 -*-

from Components.config import config, ConfigSubsection, ConfigText, ConfigNumber, ConfigPassword, ConfigSelection
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
import os, gettext, time

PLUGIN_BASE = "openHAB"
PLUGIN_VERSION = "0.4"

LOG_FILE = "/tmp/%s.log" % PLUGIN_BASE
OFF_LEVEL = 0
DEBUG_LEVEL = 1
TRACE_LEVEL = 2

PluginLanguageDomain = PLUGIN_BASE
PluginLanguagePath = "Extensions/%s/locale" % PLUGIN_BASE

def localeInit():
    gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))

def _(txt):
    t = gettext.dgettext(PluginLanguageDomain, txt)
    if t == txt:
        print "[" + PluginLanguageDomain + "] fallback to default translation for ", txt
        t = gettext.gettext(txt)
    return t

def initLog():
    try:
        os.remove(LOG_FILE)
    except OSError:
        pass

def debug(message, *args):
    if config_root.debug.value >= DEBUG_LEVEL:
        log(message, *args)

def trace(message, *args):
    if config_root.debug.value >= TRACE_LEVEL:
        log(message, *args)

def log(message, *args):
    with open(LOG_FILE, "aw") as f:
        f.write((time.ctime() + ": " + message + "\n") % args)

def initConfig():
    config_root = config.plugins.openHAB = ConfigSubsection()
    config_root.host = ConfigText(fixed_size=False)
    config_root.port = ConfigNumber(8080)
    config_root.user = ConfigText(fixed_size=False)
    config_root.password = ConfigPassword()
    config_root.sitemap = ConfigText(default="default", fixed_size=False)
    config_root.refresh = ConfigSelection(default=3, choices=[1, 2, 3, 5, 10])
    config_root.dimmer_step = ConfigSelection(default=5, choices=[1, 2, 3, 5, 10])
    config_root.debug = ConfigSelection(default=OFF_LEVEL, choices=[(OFF_LEVEL, _("no")), 
                                                                    (DEBUG_LEVEL, _("debug")), 
                                                                    (TRACE_LEVEL, _("trace"))])
    return config_root

config_root = initConfig()
localeInit()
language.addCallback(localeInit)
