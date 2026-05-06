#!/bin/bash

link_file() {
    link_file="$(pwd)/${1}"
    file_name="$(basename ${1})"
    link_target="${2}/$file_name"
    if [[ -L "$link_target" ]]; then
        echo -e "$file_name \033[32malready linked\033[0m"
        return
    fi
    if [[ -f "$link_target" ]]; then
        echo -e "$file_name \033[31mexists\033[0m"
        return
    fi
    # create symbolic link
    ln -s "$link_file" "$link_target" && echo -e "$file_name \033[32mlinked\033[0m"
}

link_file "tmux/.tmux.conf" "$HOME"
link_file "bash/.bashrc" "$HOME"
link_file "bash/.bash_profile" "$HOME"

link_file "ghostty" "$HOME/.config"
link_file "aerospace" "$HOME/.config"

link_file "opencode/opencode.json" "$HOME/.config/opencode"
link_file "opencode/skills" "$HOME/.config/opencode"
link_file "opencode/agents" "$HOME/.config/opencode"
link_file "opencode/themes" "$HOME/.config/opencode"
