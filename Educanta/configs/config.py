import os
import configparser

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

dbdev_host = config["dbdev"]["host"]
dbdev_name = config["dbdev"]["name"]
dbdev_user = config["dbdev"]["user"]
dbdev_password = config["dbdev"]["password"]
dbdev_port = config["dbdev"]["port"]

# aws_access_key_id = config["aws"]["aws_access_key_id"]
# aws_secret_access_key = config["aws"]["aws_secret_access_key"]
# template_bucket = config["aws"]["template_bucket"]