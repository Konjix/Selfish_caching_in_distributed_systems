import os

stats_folder = "Experiment_results\\Statistics"
stats = {}

# Iteracja przez pliki w folderze
for filename in os.listdir(stats_folder):
    if filename.endswith(".txt"):
        filepath = os.path.join(stats_folder, filename)

        with open(filepath, 'r') as file:
            lines = file.readlines()

            # Iteracja przez linie w pliku tekstowym
            for line in lines:
                if ":" in line:
                    key, value = map(str.strip, line.split(":", 1))
                    key_lower = key.lower()
                    if "object" in key_lower or "network" in key_lower:
                        stats.setdefault(key, []).append(value)
                    else:
                        stats.setdefault(key, []).append(value)

output_file = os.path.join(stats_folder, "combined_stats.txt")

with open(output_file, 'w') as output:
    for key, values in stats.items():
        output.write(f"{key}: {', '.join(map(str, values))}\n")
