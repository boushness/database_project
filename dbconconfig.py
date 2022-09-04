import configparser

config = configparser.ConfigParser()
config["DEFAULT"] = {
    "host" : "localhost",
    "database" : "ruckmans"
}
with open("dbcon.cfg", "w") as configfile:
    config.write(configfile)