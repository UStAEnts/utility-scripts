# OBS Scene Collection (Un)packer

A utility script for transfering complete OBS scenes between devices. Allows you to convert a scene collection JSON file into a zip archive which contains all referenced assets and a partial scene JSON file which can be unpacked ready for importing. You can then take this zip file and unpack it which will extract all the files, place them in a folder and update the scene JSON file to contain all the correct absolute paths which is default for OBS.

## Packing

```bash
$ python3 obs-pack.py pack testing.json
Made relative: Ents Crew Gray on Transparent.png
Made relative: Ents Crew2.png
Made relative: thanksto.png
Made relative: Ents Crew White on Transparent.png
Made relative: header-test.png
Made relative: StAndrewsUnion logo_whiteout[1]-01 (1).png
Made relative: labour-scotland-white-eps1.png
Made relative: Monotone_White_logo.png
Made relative: scottish_conservatives-logo-new.png
Made relative: snp.png
Made relative: looping-box0001-0360.avi
Made relative: 150715414_2554139718220037_7040795521113974714_n.jpg
Made relative: VoterRegAd.png
Made relative: overlay-card.png
Made relative: output.webm
Zipped and exported as 'testing__packaged.zip'
```

## Unpacking

```bash
$ python3 obs-pack.py unpack testing__packaged.zip
Made absolute: StAndrewsUnion_20logo-01.png
Made absolute: Ents Crew Gray on Transparent.png
Made absolute: Ents Crew2.png
Made absolute: thanksto.png
Made absolute: Ents Crew White on Transparent.png
Made absolute: header-test.png
Made absolute: StAndrewsUnion logo_whiteout[1]-01 (1).png
Made absolute: labour-scotland-white-eps1.png
Made absolute: Monotone_White_logo.png
Made absolute: scottish_conservatives-logo-new.png
Made absolute: snp.png
Made absolute: looping-box0001-0360.avi
Made absolute: 150715414_2554139718220037_7040795521113974714_n.jpg
Made absolute: VoterRegAd.png
Made absolute: overlay-card.png
Made absolute: output.webm
Unzipped and exported to testing__packaged.zip__unpack/
```

## Notes

* Searching for files has been done solely based off experimentation of OBS scenes lying around. If you find that certain media types have not been transferred properly please open an issue and **include the scenes file which caused the issue** which will help us track down missing keys.