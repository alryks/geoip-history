# GeoIP History Tracker

This Python script tracks the historical location of IP addresses using GeoIP databases from the [v2fly/geoip](https://github.com/v2fly/geoip) project. It leverages the `geoip` command-line tool provided by the v2fly project to convert historical GeoIP data files into a readable text format and then analyzes these files to determine the location of specified IPs at different points in time.

## Features

* Tracks the location history of multiple IP addresses.
* Specifies a start date to limit the historical search.
* Controls the number of historical releases to analyze (for performance).
* Provides verbose output for debugging and detailed information.
* Filters redundant location entries (e.g., consecutive identical locations).


## Prerequisites

* **Python 3.6+:**  Ensure you have Python 3.6 or a later version installed.
* **Required Python packages:** Install the necessary Python packages using:
    ```bash
    pip install -r requirements.txt
    ```
* **Go:** [Install Go](https://go.dev/doc/install) according to the instructions on the official website.
* **Git:** [Install Git](https://git-scm.com/downloads) according to the instructions on the official website.
* **v2fly/geoip:** Clone and build the `geoip` executable from the [v2fly/geoip](https://github.com/v2fly/geoip) repository. Follow the instructions below.
* **GitHub Personal Access Token:** Create a personal access token on GitHub with the `repo` scope. This is required to access the release assets of the v2fly/geoip repository. Store this token in your environment as `GITHUB_TOKEN`.  See [Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) for details.



## Building the `geoip` Executable

1. **Clone the repository:**
   ```bash
   git clone https://github.com/v2fly/geoip.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd geoip
   ```

3. **Download dependencies:**
   ```bash
   go mod download
   ```

4. **Build the executable:**
   ```bash
   go build
   ```
   This creates the `geoip` executable in the current directory.


## Usage

1. **Save the `geoip` executable:**  Place the `geoip` executable in a suitable location.

2. **Set your GitHub token:** Create `.env` file with `GITHUB_TOKEN=<YOUR_TOKEN>` in it.
   
   OR

   **Run script with environmental variable:** `GITHUB_TOKEN=<YOUR_TOKEN> python main.py ...`

4. **Run the script:**
   ```bash
   python main.py <IP_ADDRESS_1> <IP_ADDRESS_2> ... [OPTIONS] 
   ```
   Replace `<IP_ADDRESS_1> <IP_ADDRESS_2> ...` with the IP addresses you want to track.

**Options:**

* `--date YYYY-MM-DD`: Specify the start date for the history search (default: 1900-01-01).
* `--amount N`: Limit the number of latest releases to check (default: unlimited).  Use this to improve performance.  The script selects releases across the date range, not simply the *N* most recent.
* `--owner <owner>`: Specify the GitHub repository owner (default: v2fly).
* `--repo <repo>`: Specify the GitHub repository name (default: geoip).
* `--filename <filename>`: Specify the GeoIP database filename within the releases (default: geoip.dat).
* `--exec <path/to/geoip>`: Specify the path to the `geoip` executable.
* `--verbose`: Enable verbose output.


## Example

```bash
python main.py 1.1.1.1 8.8.8.8 --date 2020-01-01 --amount 20 --exec /path/to/your/executable/geoip --verbose
```

<details>
<summary>    

### Output

</summary>
<br>

```
Following geoip databases are found after 2020-01-01:
2024-10-24 00:52:44: https://github.com/v2fly/geoip/releases/download/202410240052/geoip.dat
2024-08-15 00:44:29: https://github.com/v2fly/geoip/releases/download/202408150044/geoip.dat
2024-05-23 00:41:27: https://github.com/v2fly/geoip/releases/download/202405230041/geoip.dat
2024-02-08 00:38:44: https://github.com/v2fly/geoip/releases/download/202402080038/geoip.dat
2023-11-02 00:38:10: https://github.com/v2fly/geoip/releases/download/202311020038/geoip.dat
2023-08-03 00:45:10: https://github.com/v2fly/geoip/releases/download/202308030045/geoip.dat
2023-04-27 00:45:07: https://github.com/v2fly/geoip/releases/download/202304270044/geoip.dat
2023-02-08 10:47:15: https://github.com/v2fly/geoip/releases/download/202302081046/geoip.dat
2022-10-20 01:06:16: https://github.com/v2fly/geoip/releases/download/202210200105/geoip.dat
2022-07-14 00:57:50: https://github.com/v2fly/geoip/releases/download/202207140057/geoip.dat
2022-04-07 00:44:21: https://github.com/v2fly/geoip/releases/download/202204070043/geoip.dat
2022-01-06 00:34:11: https://github.com/v2fly/geoip/releases/download/202201060033/geoip.dat
2021-10-14 00:27:24: https://github.com/v2fly/geoip/releases/download/202110140026/geoip.dat
2021-08-25 05:33:07: https://github.com/v2fly/geoip/releases/download/202108250532/geoip.dat
2021-06-17 00:23:11: https://github.com/v2fly/geoip/releases/download/202106170022/geoip.dat
2021-04-13 02:30:59: https://github.com/v2fly/geoip/releases/download/202104130230/geoip.dat
2021-03-04 00:19:42: https://github.com/v2fly/geoip/releases/download/202103040019/geoip.dat
2020-12-17 00:18:54: https://github.com/v2fly/geoip/releases/download/202012170018/geoip.dat
2020-10-06 08:07:33: https://github.com/v2fly/geoip/releases/download/202010060806/geoip.dat
2020-07-24 04:12:23: https://github.com/v2fly/geoip/releases/download/202007240411/geoip.dat

100%|███████████████████████████████████████████████████████████████████████| 20/20 [01:39<00:00,  4.95s/it]
History of 1.1.1.1 IP address location changes:
2020-07-24: us
2023-11-02: hu
2024-05-23: cz
2024-10-24: nl

History of 8.8.8.8 IP address location changes:
2020-07-24: au
2021-03-04: cz
2021-04-13: au
2023-02-08: nl
2024-05-23: de
2024-10-24: nl
```

*The info about these IP Addresses is an example and is incorrect!*

</details>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.  Note that the `v2fly/geoip` project and its data are subject to their own separate licenses ([CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) and the MaxMind GeoLite2 license).
