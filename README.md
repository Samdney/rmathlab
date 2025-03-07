# rmathlab

`rmathlab.py` **is a Linux toolset for the Remarkable 2 tablet, which enables math handwriting recognition and LaTeX generation over USB via Mathpix.** It pulls a specific file as PDF from your Remarkable 2 tablet to your current working directory on your computer, and then sends it to Mathpix for receiving handwriting recognition in different file formats. Available formats are: tex, mmd, docx, html, lines.json, lines.mmd.json (default: tex).

## Requirements

* [Passwordless SSH access](https://remarkablewiki.com/tech/ssh#passwordless_login_with_ssh_keys) to your reMarkable with `ssh <your SSH_NAME>`.
* Access to the reMarkable's official PDF renderer through its [USB web interface](https://remarkablewiki.com/tech/webinterface).
* [rsync](https://rsync.samba.org/) (comes with most Linux distributions, by default).
* [Mathpix APP_ID and APP_KEY](https://mathpix.com/) Create an account at Mathpix and receive an APP_ID and APP_KEY.

## Disclaimer

* Usage of `rmathlab.py` on your own risk. The author doesn't take any responsibility for possible damage.
* To use `rmathlab.py` you need an [Mathpix](https://mathpix.com/) API id and key. Each request by this API key for handwriting recognition to Mathpix costs fees. Keep your fees in mind. The author doesn't take any responsibility for emerging costs.

## Usage and operation

* Connect the Remarkable 2 tablet via USB and enable USB connection via `Menue -> Settings -> Storage -> USB Connection`
* Then run `rmathlab.py <filename>` to request handwriting recognition by Mathpix for the file `<filename>`. Read `rmathlab.py --help` to see how you can change its default behavior.
* At the first run, you will be asked for your SSH_NAME, Mathpix APP_ID and APP_KEY, which will be written to a configfile `config.ini`. You can also create the configfile manually by adding it to your `rmathlab`app directory (default: `/home/<user>/.rmathlab`), with the content
  
  ```
  [ssh]
  SSH_NAME = <your SSH_name>
  
  [mathpix]
  APP_ID   = <your Mathpix APP_ID>
  APP_KEY  = <your Mathpix APP_KEY>
  ```

## Acknowledgement

`rmathlab` uses some parts of [rmirro](https://github.com/hersle/rmirro) for Remarkable communication. 
