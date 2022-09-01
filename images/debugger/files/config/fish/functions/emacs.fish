function emacs -d "Open file in Emacs"
    /usr/local/emacs/bin/emacsclient -n $argv[1]
end

