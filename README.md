# share_etymonline

[![Create Releases](https://github.com/scillidan/share_etymonline/actions/workflows/releases.yml/badge.svg)](https://github.com/scillidan/share_etymonline/actions/workflows/releases.yml)

Data from `etymonline.zip` (StarDict) on [Free StarDict dictionaries](https://tuxor1337.frama.io/firedict/dictionaries.html). I can't get newer data from [Online Etymology Dictionary](http://etymonline.com) using [dictmaster](https://framagit.org/tuxor1337/dictmaster).

## Usage

1. Download files from [Releases](https://github.com/scillidan/share_etymonline/releases).
2. Use them in GoldenDict (StarDict format), sdcv, dictd, Yomichan/Yomitan.
3. See preview screenshot [here](asset/).

### sdcv

```sh
export STARDICT_DATA_DIR="<path_to_dictionaries>"
chmod +x ./sdcv-awk.sh
# Install
ln -sfn $(pwd)/sdcv-awk.sh ~/.local/bin/sdcv-awk
# Usage
sdcv --color --use-dict etymonline -n <word> | sdcv-awk
# Uninstall
rm ~/.local/bin/sdcv-awk
```

### dictd

```sh
# Arch
unzip etymonline-dictd.zip
sudo cp etymonline-dictd.{index,dict.dz} /usr/share/dictd/
sudo vim /etc/dict/dictd.conf
```

```
# Add database
database etymonline {
	data /usr/share/dictd/etymonline-dictd.dict.dz
	index /usr/share/dictd/etymonline-dictd.index
}
```

```sh
sudo systemctl restart dictd.service
```

```sh
chmod +x ./dictd-awk.sh
# Install
ln -sfn $(pwd)/dictd-awk.sh ~/.local/bin/dictd-awk
# Usage
dict --host localhost --port 2528 --database etymonline -n <word> | dictd-awk
```
