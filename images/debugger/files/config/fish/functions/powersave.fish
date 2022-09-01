function set_governor
  sudo cpufreq-set -c $argv[1] -g $argv[2]
end

function set_all_governors
  set cpus (cat /proc/cpuinfo | grep processor | cut -d: -f2 | tr -d ' ')
  for cpu in $cpus
    set_governor $cpu $argv[1]
  end
end

function powersave -d "Sets powersave governor on all CPUs"
  set_all_governors "powersave"
end

function ondemand -d "Sets ondemand governor on all CPUS"
  set_all_governors "ondemand"
end

function performance -d "Sets performance governor on all CPUs"
  set_all_governors "performance"
end
