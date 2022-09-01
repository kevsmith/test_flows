function iadd -d "Interactive version of \"git add\""
    git ls-files -m | percol | xargs git add
end
