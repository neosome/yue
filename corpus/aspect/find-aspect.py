import tomllib, tomli_w
import pycantonese

# Load the TOML file
with open("particles.toml", "rb") as f:
    data = tomllib.load(f)

# Extract particle list
particles = {(p["particle"], p["pronunciation"]) for p in data["particles"]}

print(particles)

# Load HKCanCor corpus
corpus = pycantonese.hkcancor()  # Load the Hong Kong Cantonese Corpus

# Store results for each particle
plain_sentences = {}
fancy_sentences = {}
markdown_output = []

def format_sent(sentence, fancy=False):
    formatted_sentence = []
    for token in sentence:
        word=token.word
        if (word == particle) and fancy:
            # Exact match -> Bold
            formatted_sentence.append(f"**{word}**")
        elif (particle in word)and fancy:
            # Substring match -> Strikethrough if not at the right end
            if (not word.endswith(particle))and fancy:
                formatted_sentence.append(f"~~{word}~~")
            else:
                formatted_sentence.append(f"***{word}***")  # Bold italic if at the right end
        else:
            formatted_sentence.append(word)
    print(formatted_sentence)
    return " ".join(formatted_sentence)


for particle, pronunciation in particles:
    example_sentences = corpus.search(
        character=particle,
        jyutping=pronunciation,
        by_tokens=True,
        by_utterances=True
    )
    # Store results in TOML
    plain_sentences[particle] = {"examples": [format_sent(sentence) for sentence in example_sentences]}
    fancy_sentences[particle] = {"examples": [format_sent(sentence, fancy=True) for sentence in example_sentences]}


    # Store results in Markdown
    markdown_output.append(f"## Particle: `{particle}`\n")
    markdown_output.append("**Example Sentences:**\n")
    for sent in fancy_sentences[particle]['examples']:
        print('SENT', sent)
        markdown_output.append(f"- {sent}\n")
    markdown_output.append("\n---\n")

# Save results to TOML
output_file_toml = "cantonese_particle_sentences.toml"
with open(output_file_toml, "w", encoding="utf-8") as f:
    toml_str = tomli_w.dumps(plain_sentences)
    f.write(toml_str)

# Save results to Markdown
output_file_md = "cantonese_particle_sentences.md"
with open(output_file_md, "w", encoding="utf-8") as f:
    f.writelines(markdown_output)

print(f"Results saved to {output_file_toml} and {output_file_md}")
