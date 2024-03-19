# Script of initialization of local machines when Cloning a repo via "Dev Containers: Clone Repository in Container Voilume..."
# to allow for keeping a local folder synced with the Container (for ex. to store the necessary secrets of the repo locally when in dev stage)
# Version: 2

# Define an associative array with key-value pairs of the local config files in local-config-yamls folder
declare -A users
users["/Users/tov"]="local-yaml-config-my-mac.yaml"

# If environnement variable CODESPACES is true then we are in a codespace, if CODESPACES variable is not set then we are not in a codespace

# When we are in a codespace, we need to copy the empty.compose.extend.yaml file to compose.extend.yml, and force overwrite if the file already exists
if [ "$CODESPACES" = "true" ]; then
    cp -f .devcontainer/empty.compose.extend.yaml ./compose.extend.yaml

else
    # Iterate over the array
    for user in "${!users[@]}"; do
        # Check if the user string is in the HOME or USERPROFILE environment variable
        if [[ "$HOME" == *"$user"* ]] || [[ "$USERPROFILE" == *"$user"* ]]; then
            cp -f .devcontainer/empty.compose.extend.yaml .devcontainer/temp_local.yaml

            # Concatenate the corresponding config file to temp_local.yaml
            cat .devcontainer/local-config-yamls/${users[$user]} >> .devcontainer/temp_local.yaml

            # Now move temp_local.yaml into ./compose.extend.yaml
            mv -f .devcontainer/temp_local.yaml ./compose.extend.yaml

            # Break the loop as we've found the user
            break
        fi
    done

    # Fallback to an empty.compose.extend.yaml if no user match was found (ie. no compose.extend.yaml present at root level of the project)
    if [ ! -f ./compose.extend.yaml ]; then
        cp -f .devcontainer/empty.compose.extend.yaml ./compose.extend.yaml
    fi

fi

# Finally, If you're in a Local Machine, and you have correctly configure your local secrets, make your file available as env variables for he whole system
# If ./local-secrets.env exists, then export the local-secrets.env variables into root's bashrc file
if [ -f ./local-secrets.env ]; then cat ./local-secrets.env >> /etc/environment; fi
