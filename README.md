# CS655 Image Recognition Application

This is the CS655 mini project that takes a image as input and displays its category and the RTT to get the result. User need to set up sever and worker nodes in our GENI slice, then use the web page to access useage.

## Usage Instructions
1. Find our GENI slice [MiniProjectImageRec](https://portal.geni.net/secure/slice.php?slice_id=fea4f5a4-6be4-487f-9be4-fc4009396d66) under project CS655-Fall2022, log into both server and worker nodes.
2. Run following commands on the worker node:
      ```bash
        sudo wget https://raw.githubusercontent.com/OldZack/CS655_Mini-Project/main/RunningScripts/worker.sh
        sudo bash worker.sh
      ```
3. Run following commands on the server node:
      ```bash
        sudo wget https://raw.githubusercontent.com/OldZack/CS655_Mini-Project/main/RunningScripts/server.sh
        sudo bash server.sh
      ```
4. Open our web interface in the browser with following url: http://72.36.65.74:5000/
5. Click "Choose File" to choose any .jpg or .png image, then click "Upload".
6. The recognition result and RTT will be displayed on the screen.


## Team Members
