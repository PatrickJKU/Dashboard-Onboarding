# Dashboard-Onboarding
Leverage the power of LLMs in an onboarding process for PowerBI dashboards.

## Instructions
Make sure to have your OpenAI API Key stored in the system environments variable as "OPEN_AI_API_KEY", or change the code part according to your specified name. 
This notebook will create an OpenAI Assistant that serves as a bot during an onboarding process. It creates exercises based on your level of expertise and helps you solve them. 
Due to thread saving it is possible to come back to the conversation at any time. Specify a unique user name and id to restore any previous conversations. 

A sample conversation is stored in the notebook to get a glance on what a beginner onboarding might look like. Note that an onboarding process with the current model might cost up to ~1€, depending on how many intermediate questions are asked and the level of detail requested in the explanations. 

## Limitations
Currently the bot shows very high variance in different onboarding conversations at the same expertise level, which might result in high variance in terms of user satisfaction. Also if the user makes wrong statesments about the specific dashboard, it is likely that the bot cannot catch them due to the lack of underlying data. However the tour through PowerBI in general and applying it on the sample dashboard gives very good instructions and feeling of making progress. 

## Further Work
Make the tour less expensive by capping the maximum number of generated tokens per message. 
Give more detailed explanation to the bot to ensure it can catch false statements about the dashboard and correct the user. 
