---
Author: Vlad Doster <mvdoster@gmail.com>
Date: 2020-06-30 19:15:59
Last Modified by: Vlad Doster <mvdoster@gmail.com>
Last Modified time: 2020-07-01 02:24:04

---

<div align=center>

# Open Issue Finder

### Plug in your programming interests & select issue labels to be used to find projects fitting your criteria. Hopefully it helps ease the trouble of finding an engaging project that needs help!

<img src=".repo-assets/stdout_scrot.png"
     data-canonical-src=".repo-assets/stdout_scrot.png"
     width="700"
     height="300" />
     
<img src=".repo-assets/email_scrot.png"
     data-canonical-src=".repo-assets/email_scrot.png"
     width="700"
     height="300" />
     
</div>

## Usage

1. Fill out the [config.ini](config.ini) with your interests. The interests and labels have some prepopulated to show you what it expects.
2. Requires only >=Python 3.x.x and no external dependencies!

```bash
python3 open-issue-finder
```

3. If no email credentials supplied, projects are logged to stdout and a .txt file is written with name of `open-issue-projects.txt`.
   If email credentials supplied, look in your email for a list of potential projects looking for contributors!

## Run on a schedule

1. Make script executable:

```bash
chmod +x open-issues-finder
```

2. Copy to desired host location:
   **Note**: `open-issues-finder` and `config.ini` should be in same directory.
   **Sys-Admins** would say it should be placed in `/usr/bin`, but I prefer `$HOME/.local/bin/`. It really comes down to preference.

```bash
cp open-issues-finder config.ini $HOME/.local
```

### Cron job

----

The following is how have it running on my VPS. It runs everyday at 9am.

```bash
0 9 * * * /usr/bin/python3.8 /home/vlad/.local/bin/open-issues-finder >/dev/null 2>&1
```

1. [Get up to speed on what cron is](https://wiki.archlinux.org/index.php/Cron)
2. [crontab guru - online crontab editor](https://crontab.guru/)

### Systemd service

----

1. Create the `.service` file in `/etc/systemd/system`. I'd name it something like `potential-contributor.service`

```bash
touch /etc/systemd/system/open-issues-finder.{service,timer}
```

2. Edit the `.service` file

```bash
vim -O open-issues-finder.service potential-contributor.timer
```

3. The contents would look like this.

##### /etc/systemd/system/potential-contributor.service

```bash
[Unit]
Description=Find projects with open issues and align with your programming interests

[Service]
Type=oneshot
ExecStart=/usr/bin/open-issues-finder

[Install]
WantedBy=multi-user.target
```

##### /etc/systemd/system/open-issues-finder.timer

```bash
[Unit]
Description=Run open-issues-finder every 24 hours
Requires=potential-contributor.service

[Timer]
Unit=potential-contributor.service
OnUnitInactiveSec=24h
AccuracySec=1s

[Install]
WantedBy=timers.target
```

If, for some reason your system is not playing nicely with `ExecStart` + `absolute path` or you just want to be different. Pass `ExecStart` a direct sh command

```bash
ExecStart=/bin/sh -c "python3 /usr/bin/open-issues-finder"
```

4. Exit vim. I'll wait...

5. Enable & start newly created service

```bash
systemctl enable --now open-issues-finder.service open-issues-finder.timer
```

----

### TODO

- [ ] : Clean up edge cases around GitHub throttling
- [ ] : Allow for the file to keep growing so you can have a list of possible projects.
- [ ] : Add CLI options such as `--help` and `--verbose`

----

### Open an issue if you see something I can add/fix to better this project!

