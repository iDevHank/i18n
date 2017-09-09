i18n is a python tool set for internationalization in iOS projects.

## Usage

### Generate unlocalized strings
`i18n.py -p PROJECT_PATH -o TARGET_PATH`

`PROJECT_PATH` is your iOS project directory.
Your don't have to specify the `-p PROJECT_PATH` if you run script in your project directory.

`-o TARGET_PATH` is an optional, default path is `./generated.strings`.

### Check localizable file format
Automatically check `.strings` file's format.
And indicate lines and files if there's any broken format.

### Remove duplicate localizable strings
`i18n.py -r`

Remove duplicate localizable strings using the latest one(sorted by line).

### Integrate new localizable strings
`i18n.py -i NEW_STRING_PATH`

This option requires a strict format of directory.
i.e.
```
|NEW_STRING_PATH:
    |Base.lproj:
        |Localizable.strings
    |en.lproj:
        |Localizable.strings
    |zh-Hans.lproj:
        |Localizable.strings
```

## Getting started

1. This project is based on python3 and supports macOS only. You can install python3 through brew or conda.
2. Download source code and unzip it.
3. **Edit** `config.py` to customize your project settings, such as localizable string regular expression and file path.
4. Run `DOWNLOAD_PATH/i18n.py -h` for more information.

## Have a question?
If you need any help, please create an issue or contact [me](idevhank@gmail.com).
