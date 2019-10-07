import user_interface

gui = user_interface.user_interface()

if gui.reply == 0:
    gui.convert_single_file()
else:
    gui.convert_directory()