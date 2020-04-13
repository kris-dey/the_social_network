# the_social_network

To run the app, you first need to make sure that Python3 and Pip3 are installed.     
  
Python3:  
```sh
sudo apt-get install python3.6  
```
Pip3:  
```sh
sudo apt install python3-pip  
```  
  
Then, cd into the directory in your terminal.  
  
Before running the app, you need to install the dependences. Run the following command:  
```sh  
pip3 install -r requirements.txt  
```   
Now you can run the app locally with this command:  
```sh  
python3 manage.py runserver  
```  
Navigate to http://127.0.0.1:8000/ use the web-app  
  
  
All the up-to-date code is available at https://github.com/krishanu-dey/the_social_network  
  
The web-app is also deployed on heroku, so you can access it at: https://the-social-network-42.herokuapp.com/  
Any new pushes to the master repo would automatically trigger a re-deploy on heroku with the new changes! :)
