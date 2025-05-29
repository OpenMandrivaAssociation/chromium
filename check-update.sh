#!/bin/sh
curl -s 'https://chromiumdash.appspot.com/fetch_releases?channel=Stable&platform=Linux&num=1' |jq .[].version |sed -e 's,",,g'
