#!/bin/sh
bench build --apps omnimail
sudo supervisorctl stop all
sudo supervisorctl start all