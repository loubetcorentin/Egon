# 👁️🥚Egon

This repo contains the 2025 rework of the Egon codebase.

## Env
We are using a conda env with poetry for the libraries. 

## Install
install Conda
```
conda create -n egon python=3.12 ##### 3.12 !!!! or death
conda activate egon
pip install poetry 
poetry install
```


## File Structure

main.py: the main file that starts all the threads

threads/ : the different threads of the project.
- brain_thread.py manage "decision making and emotional state" of Egon by reading inputs from the memory and sending signals to the emotion state machine and the outputs (motors, sounds, lights?)
- vision_thread.py processes the camera feed and writes its detections to the short term memory.
- forgetting thread.py slowly erase data from the memory 
- consolee_thread.py manage nice console output with the rich library 

modules/ : modules and classes used by the threads
- emotional_state.py : the state machine of possible emotions and their transitions
- logger.py : manage logging in console and log file egon.log
- short_term_memory.py : stores the things seen by the 


