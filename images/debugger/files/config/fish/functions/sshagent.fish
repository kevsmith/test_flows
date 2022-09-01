function sshagent -d "Start ssh-agent"
    if not set -q SSH_AGENT_PID
        eval (ssh-agent -c)
       
        for k in $SSH_KEYS
            set key (string join "/" "$HOME/.ssh" $k)
            ssh-add -q $key
        end        
    end
end
