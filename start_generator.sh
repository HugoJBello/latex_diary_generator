# remember 
# chmod +x generate_diary.py
# chmod +x booklets.py
# chmod +x start_generator.sh
# source venv/bin/activate

python3 generate_diary.py

pdflatex result.tex

python3 booklets.py result.pdf -o result_booklet.pdf -m 0.5
