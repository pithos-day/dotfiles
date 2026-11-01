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

link_file "bash/.bashrc" "$HOME"
link_file "bash/.bash_profile" "$HOME"

link_file "foot" "$HOME/.config"
link_file "nvim" "$HOME/.config"

# link agent skills
# ~/.agents/skills: opencode, codex など / ~/.claude/skills: claude code

for skills_dir in "$HOME/.agents/skills" "$HOME/.claude/skills"; do
    mkdir -p "$skills_dir"
    for skill in agents/skills/*/; do
        link_file "agents/skills/$(basename "$skill")" "$skills_dir"
    done
done
