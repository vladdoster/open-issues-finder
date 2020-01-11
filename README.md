# Potential Contributor

Having trouble finding an OS project to contribute too? Have projects sent to you that need help!

This app allows you to plug in your programming interests and issue labels to help you find Open Source projects to contribute to. 

![](https://github.com/vladdoster/potential_contributions/blob/master/assets/email_screenshot.png)

### Usage

1. Fill out the config.ini with your interests. The interests and labels have some prepopulated to show you what it expects.

2. Run the script with Python >= 3.6

```
python potential_contributions.py
```

3. Look in your email for a list of potential projects to contribute too!         

### Cronjob
To set as a cronjob, the following is how I have it setup. It run everyday at 9am.
```
0 9 * * * /usr/bin/python3.8 /home/<USERNAME>/.local/bin/potential_contributions.py >/dev/null 2>&1
```

### TODO
- Check if issues are stale or have a PR open
- [x] Make systemd unit file or a cronjob so it runs periodically
