# .bashrc

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'

git_branch() {
  git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}
PS1='[\u@\h \W\[\e[32m\]$(git_branch)\[\e[0m\]]\$ '

export PATH="/home/admin/.jdks/temurin-21.0.8/bin/:$PATH"
export PATH="/home/admin/.local/bin:$PATH"
