#!/bin/bash
# Install dlfetch from skill directory
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SKILL_DIR/venv"

echo "Setting up dlfetch in $SKILL_DIR..."
echo "Creating virtual environment..."
python3 -m venv "$VENV_DIR"
echo "Installing dependencies..."
"$VENV_DIR/bin/pip" install -r "$SKILL_DIR/requirements.txt" -q

if [ -z "$THISDL_USERNAME" ] || [ -z "$THISDL_PASSWORD" ]; then
    echo ""
    echo "Credentials not set. Configure them now:"
    echo -n "Username: "
    read -r username
    echo -n "Password (hidden): "
    read -r -s password
    echo ""
    cat << 'EOF' >> "$HOME/.zshrc"
# DLFetch
export THISDL_USERNAME="REPLACE_USERNAME"
export THISDL_PASSWORD="REPLACE_PASSWORD"
alias dlfetch="source '$SKILL_DIR/venv/bin/activate' && python '$SKILL_DIR/main.py' && deactivate"
EOF
    # Replace placeholders with actual values (using sed for macOS compatibility)
    sed -i '' "s/REPLACE_USERNAME/$username/" "$HOME/.zshrc"
    sed -i '' "s/REPLACE_PASSWORD/$password/" "$HOME/.zshrc"
else
    cat << EOF >> "$HOME/.zshrc"
# DLFetch
alias dlfetch="source '$SKILL_DIR/venv/bin/activate' && python '$SKILL_DIR/main.py' && deactivate"
EOF
fi

echo ""
echo "Done! Run 'source ~/.zshrc' or open a new terminal, then use: dlfetch"
