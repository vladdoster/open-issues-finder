#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Vlad Doster <mvdoster@gmail.com>
# Date: 2020-06-30 20:03:53
# Last Modified by: Vlad Doster <mvdoster@gmail.com>
# Last Modified time: 2020-06-30 20:16:43

import configparser
import itertools
import logging
import random
import smtplib
import sys
import time
from collections import namedtuple
from multiprocessing.pool import ThreadPool as Pool

import httpx

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def main():
    cfg = configparser.ConfigParser(allow_no_value=True).read("config.ini")
    interests, labels = (
        get_section(cfg, section="Interests"),
        get_section(cfg, section="Labels"),
    )
    send_email(
        cfg,
        multiprocess_links(
            gen_gh_interests_urls(cfg=cfg, interests=interests, labels=labels)
        ),
    )


def gen_gh_interests_urls(cfg, interests, labels):
    gh_api_query_link = "https://api.github.com/search/issues?q={0}+label:{1}+state:open&sort=created&order=desc"
    try:
        return [
            gh_api_query_link.format(random.choice(interests), random.choice(labels))
            for _ in itertools.repeat(None, int(cfg["User"]["projects_limit"]))
        ]
    except ValueError:
        sys.exit(
            logger.error(
                "Invalid project limit value set in config.ini. It should be an integer."
            )
        )


def multiprocess_links(urls):
    logger.info("Looking high and low for cool projects...")
    return [x for x in Pool(10).imap_unordered(get_gh_link, urls) if x is not None]


def get_gh_link(url):
    time.sleep(random.randint(1, 2))
    try:
        r = httpx.get(url)
        r.raise_for_status()
        return random.choice(r.json().get("items")).get("html_url")
    except httpx.exceptions.HTTPError as e:
        logger.warning("Encountering Github API throttling\n{0}".format(e))
    except Exception as e:
        logger.error(
            "Uh-oh, {0!r} experienced an unexpected bit flip from a solar flare.{1}".format(
                sys.argv[0], e
            )
        )


def get_section(cfg, section):
    try:
        entries = cfg.items(section)
        if entries:
            return [str(x[0]).lower() for x in entries]
        logger.error("Add at least one {0} in your config.ini".format(section[:-1]))
    except configparser.NoSectionError:
        logger.error("Add a [{0}] section to your config.ini".format(section))
    except OSError:
        logger.error("No config.ini was located.")
    finally:
        sys.exit(0)


def send_email(cfg, links):
    EmailCreds = namedtuple("EmailCreds", ["name", "email", "passwd"])
    e_c = EmailCreds(
        name=cfg["User"]["name"],
        email=cfg["User"]["email"],
        passwd=cfg["User"]["email_passwd"],
    )
    if any(credential == "" for credential in list(e_c)):
        logger.info(
            """
        Potential Contributor found the following {0} OS projects you might be interested in contributing too.

        Links:
        {1}
        """.format(
                len(links),
                "\n".join(
                    "{0}. {1}".format(idx, link) for idx, link in enumerate(links, 1)
                ),
            )
        )
        sys.exit(
            logger.warning(
                "One of the Email credentials in config.ini is empty in config.ini. Please reconcile and re-run. Exiting..."
            )
        )
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    # If using gmail, generate an app password @ https://myaccount.google.com/apppasswords
    server.login(user=e_c.email, password=e_c.passwd)
    server.sendmail(
        from_addr=e_c.email,
        to_addrs=e_c.email,
        msg="""
        Subject: Potential Contributor

        Hi {0},
        Potential Contributor found the following {1} OS projects you might be interested in contributing too.

        Links:
        {2}
        """.format(
            e_c.name,
            len(links),
            "\n".join(
                "{0}. {1}".format(idx, link) for idx, link in enumerate(links, 1)
            ),
        ),
    )
    server.quit()
    sys.exit(logger.info("Successfully sent list of project to {0}".format(e_c.name)))


if __name__ == "__main__":
    main()
