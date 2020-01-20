import configparser
import pprint
import smtplib
from multiprocessing.pool import ThreadPool as Pool
from random import *
from time import sleep

import httpx
from httpx import get

pp = pprint.PrettyPrinter(indent=1)


def main():
    cfg = configparser.ConfigParser(allow_no_value=True)
    cfg.read('config.ini')
    interests, labels = get_section(cfg, section='Interests'), get_section(cfg, section='Labels')
    links = multiprocess_links(gen_gh_interests_urls(cfg=cfg, interests=interests, labels=labels))
    pp.pprint(links)
    send_email(cfg, links)


def gen_gh_interests_urls(cfg, interests, labels):
    projects_limit = cfg['User']['projects_limit']
    links = []
    for x in range(int(projects_limit)):
        interest, label = choice(interests), choice(labels)
        links.append(
            f"https://api.github.com/search/issues?q={interest}+label:{label}+state:open&sort=created&order=desc")
    return links


def multiprocess_links(urls):
    results = []
    pool = Pool(10)
    for result in pool.imap_unordered(get_gh_link, urls):
        if result is not None:
            results.append(result)
    return results


def get_gh_link(url):
    sleep(randint(1, 2))
    try:
        r = get(url)
        r.raise_for_status()
        r = r.json()
        gh_link = choice(r.get('items')).get('html_url')
        return gh_link
    except httpx.exceptions.HTTPError as e:
        print(f"Requesting from Github too often")
    except Exception as e:
        print(f"Something unexpected occurred...\n{e}")


def get_section(cfg, section):
    entries = []
    try:
        # Normalize interests strings
        entries = cfg.items(section)
    except configparser.NoSectionError:
        print(f"Error: Add a [{section}] section to your config.ini")
        exit(1)
    except OSError:
        print("Error: No config.ini found.")
        exit(1)

    # Make sure user provides >= 1 interest
    # I learned that you should not do len(entries)==0, but just not. Python will return false if len == 0
    if not entries:
        print(f"Add at least one {section[:-1]} in your config.ini")
        exit(1)
    return [str(x[0]).lower() for x in entries]


def send_email(cfg, links):
    email, name, password = cfg["User"]["email"], cfg["User"]["name"], cfg["User"]["Email_Pass"]
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # If using Gmail, generate an app password @ https://myaccount.google.com/apppasswords
    server.login(user=email, password=password)
    links = '\n'.join(links)
    server.sendmail(
        from_addr=email,
        to_addrs=email,
        msg=f"""Subject: Potential Contributor\n\nHi {name},\nWe found the following projects you might be interested in contributing too.\n\n{links}""")
    server.quit()
    print("Successfully sent Github repos to your email!")


if __name__ == '__main__':
    main()
