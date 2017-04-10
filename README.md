
# Install
pip install -r requirements.txt

# Troubleshoot:
get WD=-1 or the message No space left on device (ENOSPC) whenever I try to add a new watch
You must have reached your quota of watches, type sysctl -n fs.inotify.max_user_watches to read your current limit and type sysctl -n -w fs.inotify.max_user_watches=16384 to modify (increase) it.

```
sysctl -n -w fs.inotify.max_user_watches=16384
```
