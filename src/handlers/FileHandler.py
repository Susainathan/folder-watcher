import logging, os, shutil
import xml.etree.ElementTree as ET
from zipfile import ZipFile, is_zipfile, BadZipFile
 
 
class FileHandler():

    def __init__(self, file_config) -> None:
        self.logger = logging.getLogger("xmlc-watcher.%s" % (__name__))
        self.input_file_path = file_config["watchPath"]
        self.destination_base_path = file_config["destinationPath"]


    def validate_and_process(self, input_file_path):
        file_path = None
        with open(input_file_path, "r") as txt_f:
            file_name =  txt_f.readline()
            file_path = self.input_file_path+"/"+file_name.strip()
        
        return self.unzip_and_copy(file_path)

    def unzip_and_copy(self, input_file_path):
        xml_data = None
        if is_zipfile(input_file_path):
            try:
                with ZipFile(input_file_path, 'r') as zObject: 
                    base_path = zObject.namelist()
                    if len(base_path) > 0:
                        transection_file, docx_file = self.get_file_names(base_path)
                        xml_data = zObject.read(transection_file)
                        article_info = self.get_article_details(xml_data)
                        return self.copy_file_to_app_path(docx_file, zObject, article_info), article_info
                    else:
                        self.logger.error("Empty zip file given.", stack_info=True)
            except BadZipFile as e:
                self.logger.error("Unable to unzip the file. Invalid zip file.", stack_info=True)
                return None, None
        else:
            self.logger.error("Given file is not valid zip file", stack_info=True)
            return None, None

    def get_file_names(self, base_path):
        transection_file = None
        docx_file = None
        for i in base_path:
            if transection_file and docx_file:
                break
            elif isinstance(i, str) and i.endswith("acs_transaction.xml"):
                transection_file = i
            elif isinstance(i, str) and i.endswith(".docx"):
                docx_file = i
        return transection_file, docx_file

    
    def get_article_details(self, transection_xml_data):
        xml_tree  =ET.fromstring(transection_xml_data.decode("UTF-8"))
        jid_string = (xml_tree.find("manuscriptInfo/journal").text).upper()
        jid = ""
        for item in jid_string.split(" "):
            jid += item[0].upper()

        article_info = {
            "aid": (xml_tree.find("manuscriptInfo/mscNo").text).lower()[2:],
            "jid": jid
            }

        return article_info

    def copy_file_to_app_path(self, docx_file, zObject, article_info):
        file_name = article_info["jid"].lower()+article_info["aid"]+".docx"
        
        destination_path = self.destination_base_path.replace("{{JID}}", article_info["jid"]).replace("{{AID}}", article_info["aid"])

        try:
            os.makedirs(destination_path, exist_ok=True)
            with zObject.open(docx_file) as source, open(destination_path+"/"+file_name, "wb") as target:
                shutil.copyfileobj(source, target)
                self.logger.info("File copied successfully.")
                return True
        except Exception as e:
            self.logger.error("Unable to copy file from source path.", stack_info=True)
            return
