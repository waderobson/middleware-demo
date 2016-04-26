"""Let zarox tell you what munki is getting."""
import subprocess

def say(*args):
    cmd = ['/usr/bin/say', '-v', 'Zarvox'] + list(args)
    proc = subprocess.Popen(cmd, shell=False, bufsize=1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (output, err) = proc.communicate()
    return (proc.returncode, output, err)

def process_request_options(options):
    url = options.get('url')
    if 'swscan.apple.com' not in url:
            say(url)
    return options