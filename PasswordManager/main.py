import CLIManager as cli
import CredManager

cli.title()
master_username, master_password = '', ''
if cli.check_existing_user():
    master_username, master_password = cli.prompt_for_master()
    while master_password == '' or master_username == '' or \
            (not CredManager.check_master(master_username, master_password)):
        master_username, master_password = cli.prompt_for_master()

else:
    cli.register()

while True:
    selected_option = cli.main_menu()
    if selected_option == '1':
        cli.store_new_cred(master_username)
        cli.wait()
    elif selected_option == '2':
        CredManager.get_cred(master_username)
        cli.wait()
    elif selected_option == '3':
        break
    else:
        print('Please Select valid option(1/2/3)')



