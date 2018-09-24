import json
import os

class miaConfig:
    CONFIG_FILE = 'globalConfig.json'
    
    def __init__(self):
        gconfig=self.__tryToLoadJsonFile(self.__getCurrentDirectory() + self.CONFIG_FILE)
        rconfig = self.__tryToLoadJsonFile(self.__getCurrentDirectory() + gconfig['REMOTE_CONFIG_FILE'])
        mconfig=self.__tryToLoadJsonFile(self.__getCurrentDirectory() + gconfig['MASKED_FILE'])   
        if not(rconfig==None):
            gconfig.update(rconfig)
        self.config=gconfig
        if not(mconfig==None):
            gconfig.update(mconfig)
           
    # Get the directory this script comes from
    def __getCurrentDirectory(self):
      return os.path.dirname(os.path.realpath(__file__))+'/'

    # Get and load Json file
    def __tryToLoadJsonFile( self , jsonFilePath):  
        if os.path.exists( jsonFilePath ):
          try:
              with open( jsonFilePath ) as jsonFile:
                  
                  return json.load( jsonFile )
                             
          except Exception as e:
              print( "Unable to load file. Exception was " + str( e ) ) 
          else:
              print( "Unable to locate file: " + jsonFilePath)

    def GetConfig(self,Value):
        return self.config[Value]
    
    def PrintConfig(self):
         print (json.dumps(self.config,indent=4, sort_keys=True))

if __name__ == '__main__':
    conf=miaConfig()
    conf.PrintConfig()                
    
    