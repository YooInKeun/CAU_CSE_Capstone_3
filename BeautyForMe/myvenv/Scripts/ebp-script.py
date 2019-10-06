#!c:\users\keun0\appdata\local\cau_cse_capstone_3\beautyforme\myvenv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'awsebcli==3.15.3','console_scripts','ebp'
__requires__ = 'awsebcli==3.15.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('awsebcli==3.15.3', 'console_scripts', 'ebp')()
    )
