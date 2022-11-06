sudo cp . /opt/controlSystem
sudo cd /opt/controlSystem

sudo setfacl -R -m u:control:rwx myfolder # Change username control for the specific User of the machine

sudo apt install python3-pip
sudo pip3 install -r /opt/controlSystem/requirements.txt

sudo cp /opt/controlSystem/services/send_sensible_data/send_sensible_data.service /etc/systemd/system/send_sensible_data.service
sudo cp /opt/controlSystem/services/receive_operations/receive_operations.service /etc/systemd/system/receive_operations.service
sudo cp /opt/controlSystem/services/receive_operations/receive_operations.socket /etc/systemd/system/receive_operations.socket

sudo systemctl daemon-reload
sudo systemctl enable send_sensible_data.service
sudo systemctl enable receive_operations.socket
sudo systemctl enable receive_operations.service
sudo systemctl start send_sensible_data.service
sudo systemctl start send_sensible_data.socket
sudo systemctl start send_sensible_data.service
