# For Saving Downloaded JSON file from Google into Codespaces:
# - Just copy paste it as is

# For Saving Downloaded JSON file from Google into local-secrets.env:
# - You need to find replace " for \" 
# - You need to find replace \n for \\n
# - You need to substitute all saut de ligne/returns/new lines par ''

# Then Copy paste the result into local-secrets.env as a variable (inside single quotes):
# SECRET_NAME='[PASTE_HERE]'


## — SCRIPT (LINUX) —
# Use bash to open a json file.
# And then find and replace '"'' for '\"'' and '\n' for '\\n' and new line for '', and print it.
cat FILE.json | sed 's/"/\\"/g' | sed 's/\\n/\\\\n/g' | tr -d '\n\r'
