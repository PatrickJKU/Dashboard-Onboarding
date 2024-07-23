# Dashboard-Onboarding
Leverage the power of LLMs in an onboarding process for PowerBI dashboards.

# Usage
This repository contains scripts to run an assistant for PowerBI dashboard onboarding. 

## Requirements
You need an OpenAI API Key. Either use one from your organization or create your own. You can find more information about billing etc. on the official OpenAI Webpage.
To create your own key, log in to OpenAI with your account and go to [OpenAI API Keys](https://platform.openai.com/api-keys). Copy the secret key ID. Next go to your Workstation's "Environment Variables" and add the variable named "OPENAI_API_KEY", paste your secret key in the value field. The application will now have access to your OPENAI API profile to upload files and create assistants.

## Create the .exe 
to create the executable, you will need to install the python environment from the .yml file in this repository. It contains the package "pyinstaller" that is used to bundle python files to executables. 
Open a terminal in the directory you cloned this repository into, make sure the provided environment is active. Now call `pyinstaller --clean GPT_V2.spec`. This command will run several minutes to create your portable application. After the creation is finished you can find your .exe file in the newly created *dist* folder. 
**Note** The *GPT_V2.exe* file needs to be in the same directory as the two folders *Dashboard Files* and *Instructions* in order to run properly. Sharing these three items results in a working environment without the need of additional frameworks. 