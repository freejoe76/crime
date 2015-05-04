#!/bin/bash
# We're just checking which times the DPD csv gets updated.
# Example:
# $ ./monitor.bash

# Environment variables are stored in project root.
# Currently two variables are set in it:
#   $RECIPIENTS, a space-separated list of email addresses to send to
#   $SENDER, the sending email address.
source ./source.bash

# Default arguments
URL=''
TEST=0
SLUG='crime_csv'
FILESIZE=0

# What arguments do we pass?
while [ "$1" != "" ]; do
    case $1 in
        -u | --url ) shift
            URL=$1
            ;;
        -t | --test ) shift
            TEST=1
            ;;
    esac
    shift
done

# DOWNLOAD!
# If we're not testing, we download the file
if [ "$TEST" -eq 0 ]; then wget -q -O "$SLUG.new" $URL; fi

wget -O "$SLUG.new" "$URL"

FILESIZE=$(du -b "$SLUG.new" | cut -f 1)
if [ $FILESIZE -lt 1000 ]; then
    echo "Filesize: $FILESIZE"
    # The $SENDER and $RECIPIENTS are set via environment variables.
    python mailer.py --state --sender $SENDER $RECIPIENTS
    #rm "$SLUG.new"
    exit 2
fi

echo "DONE"
exit 1
