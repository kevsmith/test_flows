function sysupdate -d "Update system"
    sudo apt-fast update && sudo apt-fast -y full-upgrade
end

function sysup -d "Update system"
    sysupdate
end
