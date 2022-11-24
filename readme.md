# Ping to check hosts

# Install/setup

Create a new python virtual environment

```bash
python3 -m venv .venv
```

Activate virtual environment

```bash
source .venv/bin/activate
```

Install required packages

```bash
pip install -r requirements.txt
```

# How to use

To run this script you also need pass a file that contains hosts you want to check. Per default unreachables host will be saved to a txt file.

```bash
python main.py IPs.txt
```

## Print unreachables host in console

To print out unreachables host in the console you can use the option flag --no-save-results-to-file

```bash
python main.py IPs.txt --no-save-results-to-file
```
