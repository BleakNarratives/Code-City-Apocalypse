Here is a simple example for your requirement in Bash on Ubuntu using `wake_lock` feature to make it termux native while making use of Terminus from GitHub repository as well, which will allow you create other agents and generate bash scripts with the #!/bin/bash shebang.  You can adjust this according to your requirements:
```Bash
#!/usr/bin/env bash
set -eo pipefail
IFS=$'\n'
  
# Terminus library is not included in Ubuntu, you need install it first (you may use APT or direct git clone) 
TERMINUS_URL="https://github.com/sirikata/terminus-toolkit/"
GITCLONECMD = "git clone ${TERMINUS_URL}"   # Git command for cloning repo into current dir, you can replace with wget or curl if needed 
# Clone the terminus repository to a directory and move it out of there. Make sure all commands run from here in scripts that use this script as parent shell (e.g., bash -c "$script")   # Use git clone --depth=1 $TERMINUS_URL && cd terminus-toolkit/
`git clone https://github.com/sirikata/terminus-toolkit`  ; `cd terminus-toolkit'   
make                                                                                                        # Build the toolkits (you may use make -j for parallel jobs)  
./bin/termi --help                                                             # Test if all worked well and show usage. You should not run this command in a production environment, it is just here to help understand what you can do!   
 
# Now we will create the bash script with sleep functionality as an example of self-healing recovery from Termux crash  
sleep $((RANDOM % 10))s # Generate random delay for safer execution. Replace 's' in seconds to use different unit (e.g., m, h)   
termux-wake-lock                                                                                      # Lock screen while we are running this script - no one else can interact with it until the lock is released  
echo "Recovery started"  && sleep $((RANDOM % 10))s                                                    # Sleep for random time to avoid conflicts in debugging. Replace 's' as above   
./terminus run --command "/system/bin/sh -c '/data/data/com.termux/files/usr/bin/python ~/recovery_script2.py & sleep 60'" && echo "Recovery finished" # Execute your python script here  
sleep $((RANDOM % 10))s                                                                                     # Random delay to avoid conflicts in debugging   
termux-wake-unlock                                                              # Unlock screen after running this, no one else can interact with it until the lock is released. This will bring your Termux back online  
```     Please note that you need git installed on Ubuntu for these commands and some other dependencies as well to make them work properly in a termux environment (like python).  The Python script `recovery_script2.py` should be replaced with the actual task or operation of yours, which can also run from Termux shell after sleep period is over by calling your command/python function etc...


