# MetaLex Tool
MetaLex is general tool for **lexicographics** and **metalexicographics** activities.
For current developpement version of this tool, see [MetaLex/v0.3](https://github.com/Levis0045/MetaLex/tree/v0.3)

[![Build Status](https://travis-ci.org/claroline/Distribution.svg?branch=master)](mteprojet.fr/MetaLex)

# Requirements

MetaLex is developped in **Python 2.7** environment, these packages are required :

```sh
    sudo apt-get install build-essential libssl-dev libffi-dev python-dev
    sudo pip install Cython
    sudo apt-get install libtesseract-dev libleptonica-dev libjpeg-dev zlib1g-dev libpng-dev
    sudo apt-get install tesseract-ocr-all
    sudo apt-get install python-html5lib
    sudo apt-get install python-lxml
    sudo apt-get install python-bs4
    sudo pip install pillow
    sudo pip install termcolor
    sudo CPPFLAGS=-I/usr/local/include pip install tesserocr
```

# Usage

- Move **fileTestMetaLex.py** in the current folder (MetaLex) and place it in the parent folder

- Global usage commands line


```sh
    python fileTestMetaLex.py -h
```

```md
   MetaLex arguments :
   
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -p PROJECTNAME, --project PROJECTNAME
                        Defined MetaLex project name
  -c author comment contributors, --confproject author comment contributors
                        Defined MetaLex configuration for the current project
  -i [IMAGEFILE], --dicimage [IMAGEFILE]
                        Input one or multiple dictionary image(s) file(s) for
                        current MetaLex project
  -d IMAGESDIR, --imagedir IMAGESDIR
                        Input folder name of dictionary image files for
                        current MetaLex project
  -r FILERULE, --filerule FILERULE
  -l LANG, --lang LANG  Set language for optical characters recognition and
                        others MetaLex treatment
  -s, --save            Save output result of the current project in files
  -t, --terminal        Show result of the current treatment in the terminal
  
```


- Build the file rule. 

MetaLex take file which using  specific structure to enhance output text of OCR data (from image's files dictionnaries). **\W** for word replacement, **\C** for caracter replacement and **\R**  for regular expression replacement. The space between headers served to describe remplacement.

```md
    \START
    \MetaLex\project_name\type_of_project\lang\author\date
    \W
    /t'/t
    /{/f.
    /E./f.
    \C
    /i'/i
    \R
    /a-z+/ij
    \END
```


- Run your project with the default parameters


```sh
    python fileTestMetaLex.py  -d 'imagesInputFiles' -s
```


- Run your project with your own set parameters 


```sh
    python fileTestMetaLex.py -p 'projectname' -c 'author' 'comment' 'contributors' -d 'imagesInputFiles' -r 'file_Rule.dic' -l fra
```


# Contributors

Special thank to [Bill](https://github.com/billmetangmo) for [MetaLex-vagrant](https://github.com/Levis0045/MetaLex-vagrant) version for windows, Mac OS 6, Linux


# Reference

Please don't forget to cite this work :

```latex
    @article{Mboning-Elvis,
        title  = {Quand le TAL s'empare de la métalexicographie : conception d'un outil pour le métalexicographe},
        author = {Mboning, Elvis},
        url    = {https://github.com/Levis0045/dic/},
        date   = {2017-06-20},
        shool  = {Université de Lille 3},
        year   = {2017},
        pages  = {12},
        keywords = {métalexicographie, TAL, fouille de données, extraction d'information, lecture optique, lexicographie, Xmlisation, DTD}
    }
```


