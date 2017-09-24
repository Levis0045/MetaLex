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


- Usage situation

```
    I am a metalexicographer or linguist and I have printed dictionaries. I wish to make a diachronic metalexicographics studies to
    the evolution of the formulations of the definitions of a collection of dictionaries available from period A to period B.
    
    Traditionally or at best, the contemporary metalexicographer(according to our point of view) would apply successively the following methodology:
    
    - Scanning of printed materials (Scan)
    - Optical reading of the supports (Ocrisation)
    - Manual Error Corrections
    - Marking of the articles obtained
    - Metalexographical analysis / decryption of articles
    
    
    This is an example of process used with MetaLex ! Some other more complex process can be done !

```


- Move **MetaLex.py** in the current folder (MetaLex) and place it in the parent folder


```sh
    python MetaLex.py -h
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
  --imgalg actiontype value
                        Set algorithm for enhancing dictionary image files for
                        current MetaLex project (actiontype must be : constrat
                        or bright or filter)
  -r FILERULE, --filerule FILERULE
                        Defined file rules that we use to enhance quality of
                        OCR result
  -l LANG, --lang LANG  Set language for optical characters recognition and
                        others MetaLex treatment
  -s, --save            Save output result of the current project in files
  -t, --terminal        Show result of the current treatment in the terminal

  
```


- Build the file rules of the project. 

MetaLex takes file which using  specific structure to enhance output text of OCR data (from dictionnary images files). **\W** for words replacement, **\C** for caracters replacement and **\R**  for regular expressions replacement. The spaces between headers served to describe remplacement.

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


- Run your project with the default parameters except dictionary images data and save results. You must create a folder containing dictionnary images like **imagesInput/**.


```sh

    python MetaLex.py  -d 'imagesInput' -s  # We defined a folder containing dictionnary images for current treatment 
    python MetaLex.py  -i 'imagedic.png' -s  # Or you can defined a single dictionnary image
    
```


- Run your project with your own set of parameters and save results


```sh

    python MetaLex.py -p 'projectname' -c 'author' 'comment' 'contributors' -d 'imagesInput' -r 'file_Rule.dic' -l fra -s
    
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


