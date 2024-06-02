from integrations.google_driver import upload_to_drive

def send_to_drive(data):
    """Function for sending files to google driver
    Busniess logic Domain
    """
    upload_to_drive(**data)
