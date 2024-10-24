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

1. **Save the `geoip` executable:**  Place the `geoip` executable in a suitable location or add its directory to your system's PATH.


2. **Run the script:**
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
* `--exec <path/to/geoip>`: Specify the path to the `geoip` executable. (Required if it's not in your PATH)
* `--verbose`: Enable verbose output.


## Example

```bash
python main.py 1.1.1.1 8.8.8.8 --date 2020-01-01 --amount 20 --exec /path/to/your/executable/geoip --verbose
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.  Note that the `v2fly/geoip` project and its data are subject to their own separate licenses ([CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) and the MaxMind GeoLite2 license).
