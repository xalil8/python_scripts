 #! /bin/sh
 
 function wrap {
    for i in `seq 0 $1`; do
        echo "$2$i$3"
    done
}

N=51 # Change this accordingly to number of files, that you want to feed to tesseract or export it as a script parameter.



mftraining -F font_properties -U unicharset -O eng.unicharset `wrap $N "eng.gorton.exp" ".tr"`
cntraining `wrap $N "eng.gorton.exp" ".tr"`