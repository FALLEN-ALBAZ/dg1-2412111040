#!/bin/bash

# 1. Kiem tra tham so truyen vao
if [ -z "$1" ] || [ ! -d "$1" ]; then
    echo "Loi: Thu muc khong hop le!"
    exit 1
fi

# 2. Tao thu muc luu tru backup neu chua co
mkdir -p ~/backup

# 3. Lay ten thu muc va moc thoi gian
TEN=$(basename "$1")
THOI_GIAN=$(date +"%Y%m%d_%H%M%S")
FILE_DICH="$HOME/backup/${TEN}_${THOI_GIAN}.tar.gz"

# 4. Nen thu muc
tar -czf "$FILE_DICH" "$1"

# 5. Ghi nhat ky
echo "$(date '+%Y-%m-%d %H:%M:%S') - $FILE_DICH" >> logs/backup.log
