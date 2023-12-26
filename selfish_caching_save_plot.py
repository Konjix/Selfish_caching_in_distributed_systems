import matplotlib.pyplot as plt
import pandas as pd
import os

output_folder = "Experiment_results"
if not os.path.exists(f"{output_folder}\\Plots"):
    os.makedirs(f"{output_folder}\\Plots")


exp_network_sizes = [10, 15, 25, 50]
exp_network_probabilities = [2, 3, 4]

for network_size in exp_network_sizes:
    for network_probability in exp_network_probabilities:

        path = f"experiment_results_{network_size}_{network_probability}"

        if os.path.exists(f"{output_folder}\\Results"):
            file_path = f"{output_folder}\\Results\\{path}.txt"
            
        try:
            df = pd.read_csv(file_path)
            df["Order"] = range(1, len(df) + 1)
            grouped_data = df.groupby("Objects")
        except Exception as e:
            print(f'Wystąpił błąd podczas wczytywania danych z pliku: {e}')
            continue

        plt.clf()
        # plt.axhline(y=40, color='r', linestyle='--', label='Optimum: 40') # linia optimum
        for name, group in grouped_data:
            plt.scatter(group["Order"], group["Cost"], label=f"Obiekty w sieci: {name}", s=100)
        plt.xlabel("Liczba porządkowa")
        plt.ylabel("Koszt ponoszony przez sieć")
        if network_probability == 2:
            plt.title(f"Koszt zoptymalizowanej sieci - {network_size} węzłów, prawdopodobieństwo 50%")
        elif network_probability == 3:
            plt.title(f"Koszt zoptymalizowanej sieci - {network_size} węzłów, prawdopodobieństwo 33%")
        else:
            plt.title(f"Koszt zoptymalizowanej sieci - {network_size} węzłów, prawdopodobieństwo 25%")
        plt.legend()
        plt.savefig(f"{output_folder}\\Plots\\{path}_plot.png")
