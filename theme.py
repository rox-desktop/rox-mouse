import os
import rox
from rox import OptionsBox, g
import string

from rox.basedir import xdg_data_dirs

def build_theme_button(box, node, label):
    b = g.Button()
    b.set_label(label)
    box.may_add_tip(b, node)
    def open_theme_folder(self):
        from rox import filer
        filer.open_dir(os.path.join(os.path.expanduser("~"), '.icons'))
    #def get():
    #		return 'false'
    #def set():
            
    #box.handlers[option] = (get, set)
    b.connect('clicked', open_theme_folder)
    return [b]

def add_icon_themes(themes, dir):
    if not os.path.isdir(dir):
        return
    for theme in os.listdir(dir):
        if theme.startswith('.'): continue
        leaf = os.path.join(dir, theme)
        if os.path.isdir(os.path.join(leaf, 'cursors')) or \
           theme == "core_theme" and os.path.exists(os.path.join(leaf, 'index.theme')):
            themes[theme] = True          

def build_icon_theme(box, node, label, option):
    hbox = g.HBox(False, 4)

    hbox.pack_start(g.Label(_(label)), False, True, 0)

    button = g.OptionMenu()
    hbox.pack_start(button, True, True, 0)

    menu = g.Menu()
    button.set_menu(menu)

    themes = {}
    add_icon_themes(themes, os.path.expanduser('~/.icons'))
    add_icon_themes(themes, '/usr/share/icons')
    add_icon_themes(themes, '/usr/share/pixmaps')   
    add_icon_themes(themes, '/usr/X11R6/lib/X11/icons')
    add_icon_themes(themes, '/usr/X11/lib/X11/icons')

    names = themes.keys()
    names.sort()
    for name in names:
        if name == "core_theme":
            del names[names.index(name)]
            names.insert(0, _("Core Theme"))

    names.insert(0, _("No Theme"))

    for name in names:
        item = g.MenuItem(name)
        menu.append(item)
        item.show_all()

    def update_theme():
        i = -1
        for kid in menu.get_children():
            i += 1
            item = kid.child

            # The label actually moves from the menu!!
            if not item:
                item = button.child
            label = item.get_text()
            if label == option.value or label == _("No Theme"):
                button.set_history(i)
    
    def read_theme(): 
        rox.info(_("Currently running applications must be restarted for\n"
			"the new cursor theme to apply to them\n"))
        return button.child.get_text()

    box.handlers[option] = (read_theme, update_theme)

    button.connect('changed', lambda w: box.check_widget(option))

    return [hbox]

OptionsBox.widget_registry['icon-theme'] = build_icon_theme
OptionsBox.widget_registry['folder-button'] = build_theme_button
