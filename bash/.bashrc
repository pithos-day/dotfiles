# .bashrc

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'

git_branch() {
  git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}
PS1='[\u@\h \W\[\e[32m\]$(git_branch)\[\e[0m\]]\$ '

export PNPM_HOME="$HOME/.local/share/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac

export PATH="/home/admin/.local/share/pnpm/bin:$PATH"
export PATH="/home/admin/.jdks/temurin-21.0.8/bin/:$PATH"
export PATH="/home/admin/.local/bin:$PATH"
export PATH="/home/admin/.cargo/bin:$PATH"

# opencode
export PATH=/home/admin/.opencode/bin:$PATH
