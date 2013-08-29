echo "(loading .profile)"
export PS1="\[\033[1;34m\]\!\[\033[0m\] \[\033[1;35m\]\u\[\033[0m\]:\[\033[1;35m\]\W\[\033[0m\]$ "
# update the history straight-away and include the time
export PROMPT_COMMAND='history -a'
export HISTTIMEFORMAT='%F %T '

# Here be env vars
export M2_HOME=/usr/local/apache-maven-3.0.5
# The use of launchctl is brough to you by
# http://stackoverflow.com/questions/135688/setting-environment-variables-in-os-x
# via http://stackoverflow.com/questions/7053666/maven-home-m2-home-not-being-picked-up-by-intellij-idea
launchctl setenv M2_HOME $M2_HOME
export MAVEN_OPTS="-Xmx1024M"
launchctl setenv MAVEN_OPTS "$MAVEN_OPTS"

export JAVA_OPTS="$JAVA_OPTS -Dfile.encoding=UTF-8"
launchctl setenv JAVA_OPTS "$JAVA_OPTS"

export JAVA_TOOL_OPTIONS="-Dfile.encoding=UTF8"
launchctl setenv JAVA_TOOL_OPTIONS "$JAVA_TOOL_OPTIONS"

export FIGNORE=.svn

if [[ $PATH != */Users/$USER/bin* ]]; then
  export PATH=~/bin:$PATH
fi
if [[ $PATH != */usr/local/git/bin* ]]; then
  export PATH=/usr/local/git/bin:$PATH
else
  echo "/usr/local/git/bin already in \$PATH from /etc/paths.d/git"
fi
export PATH="/Library/Frameworks/Python.framework/Versions/3.2/bin:${PATH}"
export PATH="$PATH:/usr/local/scala-2.10.1/bin"
:
# This is deesigned to be the last setting of PATH!
if [[ $PATH != */github/endafarrell/dot-scripts* ]]; then
  export PATH=/github/endafarrell/dot-scripts:$PATH
else
  echo "Warning: /github/endafarrell/dot-scripts was already in the \$PATH"
fi

export EDITOR='mvim -f -c "au VimLeave * !open -a Terminal"'m
#export http_proxy="nokes.nokia.com:8080"
#export https_proxy="nokes.nokia.com:8080"
#echo "http_proxy set to $http_proxy and https_proxy set to $https_proxy"

# Knowing what tab-completion is to ignore can be nice ;-)
export FIGNORE=.svn

# Here be aliases
alias gitmstatus='git status -s | grep "^\ M" | cut -c4- | xargs git diff'
alias kc='open -n -a "Google Chrome.app" --args --auth-server-whitelist="*.cutlass.nokia.com,*.europe.nokia.com,*.nokia.com" --auth-negotiate-delegate-whitelist'
alias kinit='echo "kinit efarrell@NOE.NOKIA.COM"; kinit efarrell@NOE.NOKIA.COM'
alias emacs='/Applications/Emacs.app/Contents/MacOS/Emacs -nw'
alias ec='/Applications/Emacs.app/Contents/MacOS/bin/emacsclient -c -n'

# There be functions - this doesn't get loaded (at least in a terminal) without
# sourcing it here)
source ~/.bashrc

# Here be messages
echo "git fetch origin; git rebase origin/master; git push origin"
