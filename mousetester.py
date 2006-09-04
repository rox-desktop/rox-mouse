import rox
from rox import OptionsBox, g

def tester_clicked(button, event):
	label = button.child

	if event.type == g.gdk.BUTTON_PRESS:
		label.set_text(_("Single click!"))
	elif event.type == g.gdk._2BUTTON_PRESS:
		label.set_text(_("Double click!!"))
	elif event.type == g.gdk._3BUTTON_PRESS:
		label.set_text(_("Triple click!!!"))
	
	return True

def reset_tester(button, event = None):
	label = button.child

	label.set_text(_("Double-click here to test mouse"))

def build_mouse_tester(box, node, label):
	assert not label

	widget = g.Button("")
	widget.connect("button-press-event", tester_clicked)
	widget.connect("leave-notify-event", reset_tester)
	reset_tester(widget)

	return [widget]

OptionsBox.widget_registry['mouse-tester'] = build_mouse_tester
