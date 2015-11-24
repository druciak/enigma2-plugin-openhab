# -*- coding: UTF-8 -*-

from Components.config import config, ConfigSubsection, ConfigText, ConfigNumber, ConfigPassword, ConfigYesNo
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
import os, gettext, time

PLUGIN_BASE = "openHAB"
PLUGIN_VERSION = "1.0"

LOG_FILE = "/tmp/%s.log" % PLUGIN_BASE

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

def debug(message):
    if config_root.debug.value:
        with open(LOG_FILE, "aw") as f:
            f.write(time.ctime() + ": " + message + "\n")

def initConfig():
    config_root = config.plugins.openHAB = ConfigSubsection()
    config_root.host = ConfigText(fixed_size=False)
    config_root.port = ConfigNumber(8080)
    config_root.user = ConfigText(fixed_size=False)
    config_root.password = ConfigPassword()
    config_root.sitemap = ConfigText(default="default", fixed_size=False)
    config_root.refresh = ConfigNumber(3)
    config_root.debug = ConfigYesNo(default=False)
    return config_root

config_root = initConfig()
localeInit()
language.addCallback(localeInit)
