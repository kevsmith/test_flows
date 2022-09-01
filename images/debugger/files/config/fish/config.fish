set -Ux GOPATH $HOME/repos/go

fish_add_path -aU $GOPATH/bin
fish_add_path -aU $HOME/.asdf/shims
fish_add_path -aU $HOME/bin
fish_add_path -aU $HOME/.local/bin

abbr --add rl reload

set -Ux EDITOR "vim"
set -Ux VISUAL "vim"
set -Ux TERM "xterm-256color"

if type -q percol
   function percol_select_history
      history|percol --result-bottom-up --prompt-bottom|read foo
      if [ $foo ]
        commandline $foo
      else
        commandline ''
      end
    end

    # this is suboptimal because I am am defining this function here
    # In fish versions prior to 3.0, this function doesn't need to be defined,
    # just put the bind command anywhere. For now, On my linux mint machine, fish 2.7.1 is still the suported version
    function fish_user_key_bindings
        bind \cr percol_select_history
    end
end
