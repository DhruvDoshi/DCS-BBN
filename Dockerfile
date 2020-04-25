FROM ubuntu 
CMD echo "Welcome to the DCS-BBN Installation"
CMD apt-get -y update && apt-get -y upgrade && apt-get install -y python3.6 && apt-get install -y git && apt install -y python3-pip && git clone https://github.com/DhruvDoshi/DCS_BBN.git && cd DCS_BBN && pip3 install flask && pip3 install flask_cors && pip3 install requests && pip3 install pycrypto && python3 node.py  
