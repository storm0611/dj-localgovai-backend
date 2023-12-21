#!/usr/bin/env bash

cd ~/openssl-1.1.1u
./config --prefix=/usr/local
make -j $(nproc)
sudo make install_sw install_ssldirs
sudo ldconfig -v
export SSL_CERT_DIR=/etc/ssl/certs
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
cd ~/crash_bandicoot/api.localgovai/
source ./venv/bin/activate
python manage.py runserver 0.0.0.0:8000
