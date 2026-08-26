for i in *.pdf
do 
    if [[ "${i: -8}" != "book.pdf" ]]
    then
        pdfcrop --margins "2 2 2 2" "$i" "$i"_output.pdf; 

        pdfbook2 "$i"_output.pdf -i 40 -o 15 -t 20 -b 15; 
        rm "$i"_output.pdf
    fi 
done
