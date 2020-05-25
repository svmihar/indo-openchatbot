~~1. acquire dataset~~
~~- bikin biar bisa download dan extract zip~~
~~- preproses semua link agar ke subtitle yify aja~~
~~2. preprocess dataset to an appropriate format for gpt2~~
~~sambungin ke tensorboard~~



# dataset
diambil dari [sini](http://opus.nlpl.eu/OpenSubtitles-v2018.php) dulu
- harus format opensubtitle
    - literally cuman tiap conversation dipisah per baris
- ubah ke dialogpt2 format dengan [ini](https://github.com/PolyAI-LDN/conversational-datasets.git)
    - WARNING! Only works with python 2.7, pastikan ada di env yang benar
    - tiap response harus ada context -> ini gimana cara misahin context nya pake ./conversational-datasets/open-subtitles
    - kenapa kenapa banyak af ini dependency nya hanya untuk extract response

# hasil 
pertama kali running dia jawabannya sama terus, mesti di ganti kayanya datasetnya rada bego soalnya
