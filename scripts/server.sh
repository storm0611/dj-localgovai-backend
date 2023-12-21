#!/usr/bin/env bash

./config --prefix=/usr/local
make -j $(nproc)
sudo make install_sw install_ssldirs
sudo ldconfig -v
export SSL_CERT_DIR=/etc/ssl/certs
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
cd ~/dj-localgovai-backend/
source ./venv/bin/activate
pip install -r req.txt
python manage.py runserver 0.0.0.0:8000
