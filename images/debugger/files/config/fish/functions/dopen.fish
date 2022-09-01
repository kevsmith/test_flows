function dopen -d "Open file using application associated with file type"
    xdg-open $argv[1] &> /dev/null
end