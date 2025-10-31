if [ -d "./venv" ]
then
    source ./venv/bin/activate
    uv pip install -r requirements.txt
else
    uv venv "./venv"
    source ./venv/bin/activate
    uv pip install -r requirements.txt
fi
python find-aspect.py
pandoc -r gfm cantonese_particle_sentences.md -o cantonese_particles.html
