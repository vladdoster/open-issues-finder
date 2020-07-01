---
Author: Vlad Doster <mvdoster@gmail.com>
Date: 2020-06-30 19:15:59
Last Modified by: Vlad Doster <mvdoster@gmail.com>
Last Modified time: 2020-07-01 02:24:04
---

# Potential Contributor

Having trouble finding an OS project to contribute too? Have projects sent to you that need help!

This script allows you to plug in your programming interests & issue labels which is used to find projects fitting your criteria. Hopefully it helps you find an engaging project, fast!

![Stdout](.repo-assets/stdout_scrot.png)
![Email](.repo-assets/email_scrot.png)

## Usage

1. Fill out the [config.ini](cofig.ini) with your interests. The interests and labels have some prepopulated to show you what it expects.
2. Requires only >=Python 3.x.x and no external dependencies!

```bash
python3 open-issue-finder
```

3. If no email credentials supplied, projects are logged to stdout and a .txt file is written with name of `open-issue-projects.txt`.
   If email credentials supplied, look in your email for a list of potential projects looking for contributors!

## Set and forget

1. Make script executable:

```bash
chmod +x potential-contributions-finder
```

2. Copy to desired host location:
   **Note**: `potential-contributions-finder` and `config.ini` should be in same directory.
   **Sys-Admins** would say it should be placed in `/usr/bin`, but I prefer `$HOME/.local/bin/`. It really comes down to preference.

```bash
cp potential-contributions-finder confing.ini $HOME/.local/vim
```

### Use a `cronjob` to run script on a schedule.

The following is how have it running on my VPS. It runs everyday at 9am.

```bash
0 9 * * * /usr/bin/python3.8 /home/vlad/.local/bin/potential_contributions.py >/dev/null 2>&1
```

1. [Get up to speed on what cron is](https://wiki.archlinux.org/index.php/Cron)
2. [crontab guru - online crontab editor](https://crontab.guru/)

### Systemd service

1. Create the `.service` file in `/etc/systemd/system`. I'd name it something like `potential-contributor.service`

```bash
touch /etc/systemd/system/potential-contributor.{service,timer}
```

2. Edit the `.service` file

```bash
vim -O potential-contributor.service potential-contributor.timer
```

3. The contents would look like this.

##### /etc/systemd/system/potential-contributor.service

```bash
[Unit]
Description=Send N \# of projects that align with programming interests

[Service]
Type=oneshot
ExecStart=/usr/bin/potential-contributions-finder

[Install]
WantedBy=multi-user.target
```

##### /etc/systemd/system/potential-contributor.timer

```bash
[Unit]
Description=Run potential-contributions-finder every 24 hours
Requires=potential-contributor.service

[Timer]
Unit=potential-contributor.service
OnUnitInactiveSec=24h
AccuracySec=1s

[Install]
WantedBy=timers.target
```

If, for some reason your system is not playing nicely with `ExecStart` + `absolute path`. Pass `ExecStart` a direct sh command

```bash
ExecStart=/bin/sh -c "python3 /usr/bin/potential-contributions-finder"
```

4. Exit vim. I'll wait...

5. Enable & start newly created service

```bash
systemctl enable potential-contributor.service potential-contributor.timer

systemctl start potential-contributor.service potential-contributor.timer
```

### TODO

[ ]: Clean up edge cases around GitHub throttling
[ ]: Allow for the file to keep growing so you can have a list of possible projects.
[ ]: Add CLI options such as `--help` and `--verbose`

### Open an issue if you see something I can add/fix to better this project!

