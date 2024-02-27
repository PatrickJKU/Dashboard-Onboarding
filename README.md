# Dashboard-Onboarding
Leverage the power of LLMs in an onboarding process for PowerBI dashboards.

The environment file is designed such that both frameworks are working properly. If you only plan on using the GPT4 Assistant it is not recommended to use it, since not many packages and dependencies are required. However if you wish to use GraphText it might save a lot of time using this environment file. 

# GPT4 Assistant
## Instructions
Make sure to have your OpenAI API Key stored in the system environments variable as "OPENAI_API_KEY", or change the code part according to your specified name. 

### Create an Assistant
If you want to create a new assistant use the provided jupyter notebook. Copy the files you want to use for your assistant into GPT Assistant/Dashboard Files, recommended are JSON files containing information about elements of the dashboard and csv files containing triggered action - state pairs to navigate the dashboard. 
Give your assistant a name and change the instruction prompt according to your specific needs. Leave it as it is if you just want to set up the dashboard assistant.
Now just execute the first five cells of the notebook and check on the openAI website if your assistant has been created successfully. [OpenAI Assistants](https://platform.openai.com/assistants)


### Use an exisiting Assistant
If you already have a working assistant, you can start using it by setting it in different ways. 
- Use in jupyter notebook
Run the notebook and start talkin to the GPT with the "generate_response" function like provided in the examples at the bottom of the notebook. 
- Use Grado interface
You can also use the embedded grado interface of the notebook for your conversation
- Use Grado web interface
Note that this is only possible with conda environments atm. 
If you do not want to use the notebook, you can start the assistant via Dashboard_Onboarding_conda.bat. This will open the web interface, but you have to follow some setup steps first

Open the GPT.py file and paste the id of your assistant into line 98 to retrieve the correct one. 
Locate your conda installation path and copy it. Open Dashboard_Onboarding_conda.bat and paste the path in line 2. Change the environment name in line 4 to the conda environment name you are working in. It is recommended to use the provided .yml file in this case. 

You can now execute the batch file, it will open the local server where Grado is running. Refresh the page after some seconds in order to see the interface. Enter your username and id and start chatting!

## Limitations
Currently the bot shows very high variance in different onboarding conversations at the same expertise level, which might result in high variance in terms of user satisfaction. Also if the user makes wrong statesments about the specific dashboard, it is likely that the bot cannot catch them due to the lack of underlying data. However the tour through PowerBI in general and applying it on the sample dashboard gives very good instructions and feeling of making progress. 

## Further Work
Make the tour less expensive by capping the maximum number of generated tokens per message. 
Give more detailed explanation to the bot to ensure it can catch false statements about the dashboard and correct the user. 

# GraphText
