import re
from datetime import date

def main():
    with open("arrivingAnimals.txt", "r") as f:
        animal_data = f.readlines()

    with open("animalNames.txt", "r") as f:
        name_pool = [line.strip() for line in f.readlines()]

    id_counter = {}
    name_index = 0
    habitats = {}

    for line in animal_data:
        line = line.strip()

        # Allow splitting into exactly 5 parts (even with commas in the origin)
        parts = line.split(", ", maxsplit=4)
        if len(parts) < 5:
            print("Skipping line due to format issue:", line)
            continue

        age_gender_species, birth_season, color_desc, weight_str, origin = parts

        # Match age, sex, and species
        match = re.match(r"(\d+)\s+year old\s+(male|female)\s+([\w\s]+)", age_gender_species.strip(), re.IGNORECASE)
        if not match:
            print("Skipping due to age/gender/species format:", age_gender_species)
            continue

        age, sex, species = match.groups()
        age = int(age)
        species = species.strip().lower()

        # Clean remaining fields
        season = birth_season.replace("birth season", "").strip().lower()
        color = color_desc.replace("color", "").strip().lower()
        weight_match = re.search(r"(\d+)", weight_str)
        if not weight_match:
            print("Skipping due to weight format:", weight_str)
            continue
        weight = int(weight_match.group(1))
        origin = origin.strip()

        # Generate fields
        birth_date = gen_birth_date(season, age)
        unique_id = gen_unique_id(species, id_counter)

        if name_index >= len(name_pool):
            raise ValueError("Not enough names in animalNames.txt.")
        name = name_pool[name_index]
        name_index += 1

        animal_info = (
            f"{unique_id}; {name}; birth date: {birth_date}; {color} color; "
            f"{sex}; {weight} pounds; from {origin}; arrived {date.today().isoformat()}"
        )

        if species not in habitats:
            habitats[species] = []
        habitats[species].append(animal_info)

    with open("zooPopulation.txt", "w") as f:
        for species, animals in habitats.items():
            f.write(f"{species.capitalize()} Habitat:\n\n")
            for animal in animals:
                f.write(animal + "\n")
            f.write("\n")

    print("Done!")

def gen_birth_date(season: str, age: int) -> str:
    current_year = date.today().year
    birth_year = current_year - age
    season_starts = {
        "spring": "-03-21",
        "summer": "-06-21",
        "fall": "-09-21",
        "autumn": "-09-21",
        "winter": "-12-21",
        "unknown": "-06-15"
    }
    suffix = season_starts.get(season.lower(), "-06-15")
    return f"{birth_year}{suffix}"

def gen_unique_id(species: str, id_counter: dict) -> str:
    prefix = species[:2].capitalize()
    id_counter[species] = id_counter.get(species, 0) + 1
    return f"{prefix}{id_counter[species]:02d}"

if __name__ == "__main__":
    main()
