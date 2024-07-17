rem Define here the path to your conda installation
set CONDAPATH=C:\Users\pmair\miniconda3
rem Define here the name of the environment
set ENVNAME=PR

rem The following command activates the base environment.
rem call C:\ProgramData\Miniconda3\Scripts\activate.bat C:\ProgramData\Miniconda3
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)

rem Activate the conda environment
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%

rem Run a python script in that environment
python -m webbrowser http://127.0.0.1:7860
python GPT.py