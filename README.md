Crowdsourcing Application

1. Clone the directory api and install pipenv using the following command
    pip3 install pipenv

2. To open the pipenv virtual enviornment use the command
    pipenv shell

3. Use the command 'exit' to close the virtual enviornment.

4. In the virtual enviornment install all the required packages using the command 
    pipenv install 


API Details

1. Get Image API
	- Request type - GET
	- Request parameter 	- id which is an integer

2. Save Annotation
	- Request type - POST
	- Request Parameters 	- image_id the id returned from Get Image
				- label which is a string 
				- canvas_size a 2D of the 3 corners of the canvas
				- x_cor list of x coordinates
				- y_cor list of y coordinates

3. For Accessing the Save API use token no. 123456
				
			
