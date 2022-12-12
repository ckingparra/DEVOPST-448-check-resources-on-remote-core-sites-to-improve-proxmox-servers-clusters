DEVOPST-488 Check resources on remote core sites to improve proxmox servers / clusters
**************************************************************************************

Ticket: https://stacklocity1.atlassian.net/browse/DEVOPST-448

To work on this project, do the following.
::

  # Go to the project directory
  $ cd $projdir

  # Set up environment with poetry and other os packages.
  $ nix-shell

  # Enter a python venv created from pyproject.toml and start
  # a bash shell inside of it.
  $ poetry shell

  # Edit the file with a terminal to the left, and the cursor
  # placed on the definition of the less function.
  $ vim -c 'vert term bpython' '+/def less(/' ./add_to_hostgroup.py 
