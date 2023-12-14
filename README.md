# GreenTeamBookStoreInventory
Hello to anyone wanted to run and host their own version of our website.

Before trying to host your own server, you will need to have a bare minimum of python installed. But it is recommended to have VS Code installed.

To start setting up your own sever, follow the steps below:

1: Download and extract the repository into any directory you have.

2: Open the now extracted project, and navigate to GreenTeamBookStoreInventory inside File Explorer.

3: Click on the File Explorer's Address bar while inside the program and type 'cmd' (without the '), and hit enter. That should open a command prompt.

4: Run the command python -m venv .

5: Then, enter Scripts\activate

5.1: You might run into an error of: 'Cannot be loaded because running scripts is disabled on this system'. Should that happen, you will need to open a seperate powershell console, and make sure its run as an administrator, and change the execution policy.

5.2: The command to do that is: Set-ExecutionPolicy Unrestricted

5.3: Then simply follow the instructions of the command and go back to step 5 and it should work.

6: Now you should be inside of the virtual enviroment, which you should tell by now having a (someName) at the far left.

7: You will now want to install from the Requirements.txt file in the project, by running the command:
 pip install -r .\requirements.txt

8: Now that you have the neccesary requirements, navigate to the GreenTeamProject folder (cd G*), and run the following command: python manage.py runserver

9: Your device should now be hosting a local version of the website, hosted at 127.0.0.1:8000.
