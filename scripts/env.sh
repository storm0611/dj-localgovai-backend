sudo systemctl stop django-local.service
sudo rm -rf /etc/systemd/system/django-local.service
sudo cp django-local.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable django-local.service
sudo systemctl start django-local.service
sudo systemctl status django-local.service