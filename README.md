# Sononymefel
Sononymefel is a small Python script that automatically creates and assigns tags to your sample library in the FL Studio browser using Sononym's local database file.

## Requirements
- [Python](https://www.python.org/downloads/)
- An existing [Sononym](https://www.sononym.net/) library
- [FL Studio](https://www.image-line.com/)

## Usage

The syntax goes as follows:

`Sononymefel.py dbfile_path [--fl_user_data_folder] [--sample_library_folder]`
<br/><br/><br/>
## How does this work?

### Sononym's database file
Upon scanning a sample library and automatically tagging the audio files using machine learning, Sononym creates a database file called **sononym.db**, normally located at the root of the imported sample library folder.

Fortunately this database is not encrypted, so we can easily read and extract its contents. For the purposes of this script, we simply need the **filename** and **categories_VS** columns.

### FL Studio's "Tags" File
To store the list of tags and to remember which tag(s) are associated with each sample, once at least one tag is assigned to a sample, FL Studio creates a file called **Tags** in the following location:

`USER_DATA_FOLDER/FL Studio/Settings/Browser/`.

Although I found that FL Studio can be very picky about the syntax when parsing this file, we can see that it is relatively straight forward to understand how the information is structured.
