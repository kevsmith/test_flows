function mk_sparse --description 'Create sparse disk image' --argument-names image_name image_size
    if test -z $image_name
        printf "Missing image name\n" 1>&2
        return 1
    end
    if test -z $image_size
        printf "Invalid image size\n" 1>&2
        return 1
    end
    if test $image_size -lt 16
        printf "Image size too small. Minimum size is 16 MB\n" 1>&2
        return 1
    end
    command dd if=/dev/zero of={$image_name} bs=1 count=0 seek={$image_size}M
    command mkfs -t ext4 -q {$image_name}
end
