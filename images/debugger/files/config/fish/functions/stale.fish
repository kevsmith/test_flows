function stale -d "Checks for stale ASDF packages"
  set current (asdf current $argv[1])
  set latest (asdf latest $argv[1])
end
