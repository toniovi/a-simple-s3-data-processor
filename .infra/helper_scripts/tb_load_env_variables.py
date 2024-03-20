#TB! load env variables
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv('local-secrets.env'), override=True)
load_dotenv(find_dotenv('.env'), override=True)

### AND THE NEW VERSION: ###

#TB! load env ariables
import our_utilities; our_utilities.load_env_with_substitutions()