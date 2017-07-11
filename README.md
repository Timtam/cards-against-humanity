# cards-against-humanity
An open-source implementation of the popular Cards Against Humanity game.
If you don't know what this actually is, look at the corresponding [website](https://cardsagainsthumanity.com/).
# Development
Initial development of this project will occur during the summer semester 2017 by students of the Anhalt University of Applied Sciences.
We aim to provide the following features:
* packaging support to make it possible to run server and/or client even without any further installations (possibly with cx_Freeze)
* accessibility improvements so blind and visually impaired players can play this game too
* one database per server support, meaning that different servers can provide different card databases
* database editing utility so users can edit their database to add new and unique cards (black as well as white ones)
* multi-platform support (Windows Linux, OS X, maybe mobile devices like Android too)

After finishing development at the end of the summer semester this code will be free to everyone to modify or use without limitation, though it would be nice to reference back to the roots of the project.

# Licensing
The code found under this project stands under the MIT license which can be found [inside of this repository too](./LICENSE).
The only exception is the accessible_output library, which contains an enhanced version of the accessible_output library by Christopher Toth, which is licensed under a Python Software Foundation License (PSF) and therefore needs to be handled as such.

All sound effects are licensed under a Royalty-Free License and are licensed to Toni Barth and may therefore not be used in cloned projects, you'll have to replace them in order to continue development of this project elsewhere.

The lock icon found [here](./assets/images/lock.png) is licensed under a Creative Commons (Attribution-Share Alike 3.0 Unported) license by WPZOOM and can be found on [IconFinder](https://iconfinder.com) too.

# Dependencies
Server and client are written in Python 2 and depend on multiple packages, which need to be installed before running the game. All required packages are annotated inside the requirements.txt file, which can be run through pip to install all requirements.
```
pip install -r requirements.txt
```
The only thing which is left now is to install wxPython. For Windows it might be the best idea to download the binary package from [the wxPython download page](https://wxpython.org/download.php).
For other operating systems, please follow the official [wxPython installation notes](https://wiki.wxpython.org/How%20to%20install%20wxPython).
# accessibility notes
## Screen Reader support
We provide accessibility by supporting several screen readers, including the following:
* JAWS
* NVDA
* Speechd (Linux)
* Supernova
* System Access
* Virgo
* VoiceOver (OS X)
* Window Eyes

Of course we'll try to support as many platforms as possible, so if you encounter any accessibility problems with any platform/screen reader, don't hesitate to contact us, or at least open an issue.

## Keystrokes
Keep in mind that the accessibility features are only enabled if using the client-accessible launcher. If only using the client launcher, the accessibility features will be disabled. That's just to prevent sighted people into stumbling into a world of stuttering speech which would disgust them that much that they'll throw this game away immediately.
### General Keys
* Tab and shift+tab to navigate through all of the controls
* Ctrl to repeat the currently selected control
* Arrow up and down to scroll through text controls with multiple lines of text
* Home and end to jump to the beginning or end of text controls or input fields
* Return to submit buttons
* Backspace and delete to handle input fields (same as usual)
* Letters and digits to enter into input fields

Take note that some input fields may be digit-only input fields and therefore only accept numbers.
### Game view Keys
The game view specifies some additional keys to navigate more quickly:
* Number keys 1 through 0 to select white cards 1 to 10
* B to select the black card immediately

Keep in mind that this list could change at any time and if you miss some keys here which you think could be helpful, just add an issue and we'll do our best.