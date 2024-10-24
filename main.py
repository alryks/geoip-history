import argparse
from dotenv import find_dotenv, load_dotenv
import os

import ipaddress
import datetime
from pathlib import Path

from urllib.parse import urlencode, urlunparse
import requests

from tempfile import NamedTemporaryFile, TemporaryDirectory
import json

import subprocess

from tqdm import tqdm


geoip_config = {
    "input": [
        {
            "type": "v2rayGeoIPDat",
            "action": "add",
        }
    ],
    "output": [
        {
            "type": "text",
            "action": "output"
        }
    ]
}


class CheckAmountAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values < 1:
            raise argparse.ArgumentTypeError(f"Amount should be greater than 0")
        setattr(namespace, self.dest, values)


def check_path(path):
    path = Path(path)
    if path.is_file():
        return path.absolute()
    raise argparse.ArgumentTypeError(f"File {path} does not exist")


def parse_args():
    global args

    dotenv_path = find_dotenv()
    if dotenv_path:
        load_dotenv(dotenv_path)
    if 'GITHUB_TOKEN' not in os.environ:
        raise KeyError('GITHUB_TOKEN not found in environment variables')

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('ip', nargs='*', type=ipaddress.ip_address, help='IP address')
    parser.add_argument('--date', default=datetime.datetime(1900, 1, 1), type=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'), help='Date in format YYYY-MM-DD')
    parser.add_argument('--amount', action=CheckAmountAction, default=float('inf'), type=int, help='Amount of the latest releases to check')

    parser.add_argument('--owner', default='v2fly', type=str, help='Owner of the repository')
    parser.add_argument('--repo', default='geoip', type=str, help='Repository name')
    parser.add_argument('--filename', default='geoip.dat', type=str, help='Name of the geoip database file')

    parser.add_argument('--exec', default='geoip', type=check_path, help='Name of the geoip executable')

    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()


def build_url(netloc, url='', query=None):
    if not query:
        query = {}
    query = urlencode(query)
    return urlunparse(('https', netloc, url, '', query, ''))


def geoip(url):
    result = {ip: '' for ip in args.ip}
    left_ips = set(args.ip)

    with NamedTemporaryFile("w") as config_file:
        with TemporaryDirectory() as output_dir:
            geoip_config['input'][0]['args'] = {'uri': url}
            geoip_config['output'][0]['args'] = {'outputDir': output_dir}
            config_file.write(json.dumps(geoip_config, indent=4))
            config_file.flush()

            subprocess.run([f'{args.exec}', '-c', config_file.name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            for file in Path(output_dir).iterdir():
                if not file.is_file():
                    continue
                with file.open() as f:
                    for network in f.readlines():
                        network = ipaddress.ip_network(network.strip())
                        for ip in left_ips.copy():
                            if ip not in network:
                                continue
                            result[ip] = file.stem
                            left_ips.remove(ip)
                            if not left_ips:
                                return result
    return result


def geoip_until_date():
    geoip_urls = []

    page = 1
    while True:
        url = build_url('api.github.com', url=f'repos/{args.owner}/{args.repo}/releases', query={'per_page': 100, 'page': page})

        releases = requests.get(url, headers={'Authorization': f'Bearer {os.environ["GITHUB_TOKEN"]}'}).json()
        if isinstance(releases, dict) or not releases:
            break

        for release in releases:
            release_date = datetime.datetime.strptime(release['published_at'], '%Y-%m-%dT%H:%M:%SZ')
            if release_date < args.date:
                continue

            for asset in release['assets']:
                if asset['name'] == args.filename:
                    geoip_urls.append({
                        'url': asset['browser_download_url'],
                        'date': release_date
                    })
                    break

        page += 1

    if args.amount > len(geoip_urls):
        args.amount = len(geoip_urls)
    counted_geoip_urls = []
    if args.amount == 1:
        counted_geoip_urls.append(geoip_urls[0])
    else:
        for i in range(args.amount):
            counted_geoip_urls.append(geoip_urls[min(len(geoip_urls) - 1, (i * len(geoip_urls)) // (args.amount - 1))])

    if args.verbose:
        geoip_urls_text = "\n".join([f'{url["date"]}: {url["url"]}' for url in counted_geoip_urls])
        print(f"Following geoip databases are found after {datetime.datetime.strftime(args.date, '%Y-%m-%d')}:\n{geoip_urls_text}\n")

    history = {ip: [] for ip in args.ip}

    for url in tqdm(counted_geoip_urls, leave=args.verbose):
        countries = geoip(url['url'])
        for ip, country in countries.items():
            history[ip].append({
                'date': url['date'],
                'country': country
            })

    for ip in history:
        history[ip].sort(key=lambda x: x['date'])

    history_filtered = {ip: [] for ip in history}
    for ip in history:
        for record in history[ip]:
            if not history_filtered[ip] or record['country'] != history_filtered[ip][-1]['country']:
                history_filtered[ip].append(record)

    history_text = "\n\n".join([f'History of {ip} IP address location changes:\n' + "\n".join([f'{datetime.datetime.strftime(record["date"], "%Y-%m-%d")}: {record["country"]}' for record in history_filtered[ip]]) for ip in history_filtered])

    print(history_text)


def main():
    parse_args()
    geoip_until_date()


if __name__ == '__main__':
    main()
