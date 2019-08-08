# pandaMalbox
This repo contains various scripts that can be used to work with the [PANDA](https://github.com/panda-re/panda) reverse engineering framework. The content is based on our blogpost with additional information [here](www.adalogics.com).

## Running the scripts

```
# Get this repo
git clone https://github.com/AdaLogics/pandaIntro
cd pandaIntro

# Clone PANDA
git clone https://github.com/panda-re/panda
./panda/panda/scripts/install_ubuntu.sh


# Now install our stuff
download_windows.sh

```
At this point we need to create a snapshot that is useful for analysis. To do this, please follow the instructions [here](www.adalogics.com).

Then we can continue with creating a recording and replaying this recording.
```
# Make a recording of the sample
cd sample_app
unzip msg_app.zip
cd ..

python vm_record.py -sample sample_app/msg_app.exe

python vm_replay.py -recording sample

less panda_replay.stdout
...
```
