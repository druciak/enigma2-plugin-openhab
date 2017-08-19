from distutils.core import setup, Extension
import setup_translate

pkg = 'Extensions.openHAB'
setup (name = 'enigma2-plugin-extensions-openhab',
       version = '0.2',
       description = 'Simple openHAB client for Enigma2',
       package_dir = {pkg: 'src'},
       packages = [pkg],
       package_data = {pkg: ['../LICENSE', '*.png', '../po/*/LC_MESSAGES/*.mo']},
       cmdclass = setup_translate.cmdclass, # for translation
)
