function ikill -d "Interactively kill processes"
    ps aux | percol | awk '{ print $2 }' | xargs kill
end
