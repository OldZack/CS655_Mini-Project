sudo apt-get update 
sudo apt-get install -y python3-pip libjpeg8-dev zlib1g-dev nginx 
pip3 install setuptools 
pip3 install wheel celery 
pip3 install torch==1.10.0+cpu torchvision==0.11.1+cpu torchaudio==0.10.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html 
pip3 install requests 
python3 worker.py