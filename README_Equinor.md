# Installation on Equinor PCs running Windows 10

## Prequisites

 -  Download the ```dmss``` source code and unzip it (or use git from the command line)
 - Install Docker, then navigate to its:
   - ```Settings > Resources > Proxies``` and set ```http://www-proxy.statoil.no``` under ```Web Server``` and ```Secure Web Server```. 
   - ```Settings > Resources > File Sharing``` and add the drive (e.g. ```C:\```) where the ```dmss``` source code is located
 
## Building and starting

Open a command prompt and navigate to the ```dmss``` source code folder. Then type 

```sh
.\generate-api.bat
docker-compose -f docker-compose.win10.yml build
docker-compose -f docker-compose.win10.yml -f docker-compose.override.yml up
``` 
