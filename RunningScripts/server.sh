sudo apt-get update
sudo apt-get install -y python3-pip
pip3 install flask
rm -rf CS655_Mini-Project
git clone https://github.com/OldZack/CS655_Mini-Project.git
python3 CS655_Mini-Project/Server/routes.py
