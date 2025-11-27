# share_etymonline

[![Create Releases](https://github.com/scillidan/share_etymonline/actions/workflows/releases.yml/badge.svg)](https://github.com/scillidan/share_etymonline/actions/workflows/releases.yml)

Data from `etymonline.zip` (StarDict) on [Free StarDict dictionaries](https://tuxor1337.frama.io/firedict/dictionaries.html). I can't use [dictmaster](https://framagit.org/tuxor1337/dictmaster) to download data from [etymonline.com](http://etymonline.com), so I used this archive.

## Usage

1. Download files from [Releases](https://github.com/scillidan/share_etymonline/releases).
2. Use them in GoldenDict (StarDict), sdcv, Yomichan/Yomitan.
3. See preview screenshot [here](asset/).

### sdcv

```sh
export STARDICT_DATA_DIR="<path_to_dictionaries>"
chmod +x ./sdcv-awk.sh
# Install
ln -sfn $(pwd)/sdcv-awk.sh ~/.local/bin/sdcv-awk
# Usage
sdcv --use-dict etymonline -n <word> | sdcv-awk
# Uninstall
rm ~/.local/bin/sdcv-awk
```
