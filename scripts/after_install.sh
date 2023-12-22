#!/usr/bin/env bash

# kill any servers that may be running in the background 
sudo pkill -f runserver

# kill frontend servers if you are deploying any frontend

cd /root/openssl-1.1.1u
./config --prefix=/usr/local
make -j $(nproc)
sudo make install_sw install_ssldirs
sudo ldconfig -v
export SSL_CERT_DIR=/etc/ssl/certs
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

cd /root/dj-localgovai-backend/

# activate virtual environment
python -m venv venv
source venv/bin/activate

install req.txt
pip install -r /root/dj-localgovai-backend/req.txt

# run server
screen -d -m python manage.py runserver 0.0.0.0:8000