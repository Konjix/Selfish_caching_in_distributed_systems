import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

if not os.path.exists(f"Experiment_results\\Plots"):
    os.makedirs(f"Experiment_results\\Plots")
if not os.path.exists(f"Experiment_results\\Statistics"):
    os.makedirs(f"Experiment_results\\Statistics")

exp_network_sizes = [10, 15, 25, 50]
exp_network_probabilities = [2, 3, 4]

for network_size in exp_network_sizes:
    for network_probability in exp_network_probabilities:

        path = f"experiment_results_{network_size}_{network_probability}"
        opt_path = f"network_{network_size}_{network_probability}_optimum_value"

        if network_probability == 2:
           network_probability_percent = "50%"
        elif network_probability == 3:
            network_probability_percent = "33%"
        else:
            network_probability_percent = "25%"

        if os.path.exists(f"Experiment_results\\Results"):
            file_path = f"Experiment_results\\Results\\{path}.txt"
        if os.path.exists(f"Experiment_results\\Optimum"):
            opt_file_path = f"Experiment_results\\Optimum\\{opt_path}.txt"
            
        try:
            df = pd.read_csv(file_path)
            df2 = np.loadtxt(opt_file_path,delimiter=":",dtype=str)
            df["Order"] = range(1, len(df) + 1)
            grouped_data = df.groupby("Objects")
            average_cost = df["Cost"].mean()  # Średnia kosztów
            cost_variance = df["Cost"].var()  # Wariancja kosztów
            min_cost = df["Cost"].min()  # Minimalny koszt
            #max_cost = df["Cost"].max()  # Maksymalny koszt
            #min_cost_objects = df.loc[df["Cost"].idxmin()]["Objects"]  # Ilość obiektów dla minimalnego kosztu
            #max_cost_objects = df.loc[df["Cost"].idxmax()]["Objects"]  # Ilość obiektów dla maksymalnego kosztu
            optimum = int(df2[1])
        except Exception as e:
            print(f'Wystąpił błąd podczas wczytywania danych z pliku: {e}')
            continue

        # Zapisywanie wariancji, średniej, minimalnego i maksymalnego kosztu do osobnego pliku tekstowego
        statistics_file_path = f"Experiment_results\\Statistics\\{path}_statistics.txt"
        with open(statistics_file_path, "w") as statistics_file:
            statistics_file.write(f"Network size: {network_size}\n")
            statistics_file.write(f"Network probability: {network_probability_percent}\n")
            statistics_file.write(f"Mean Cost: {average_cost:.2f}\n")
            statistics_file.write(f"Variance Cost: {cost_variance:.2f}\n")
            statistics_file.write(f"Found Cost: {min_cost:.2f}\n")
            #statistics_file.write(f"Min object: {min_cost_objects}\n")
            #statistics_file.write(f"Max Cost: {max_cost:.2f}\n")
            #statistics_file.write(f"Max object: {min_cost_objects}\n")
            statistics_file.write(f"Optimum: {optimum}")

        plt.clf()
        for name, group in grouped_data:
            plt.scatter(group["Order"], group["Cost"], label=f"Obiekty w sieci: {name}", s=100)
        plt.axhline(y=average_cost, color='r', linestyle='--', label=f'średni koszt: {average_cost:.2f}')
        plt.xlabel("Liczba porządkowa")
        plt.ylabel("Koszt ponoszony przez sieć")
        plt.title(f"Koszt zoptymalizowanej sieci - {network_size} węzłów, prawdopodobieństwo {network_probability_percent}")
        plt.legend()
        plt.savefig(f"Experiment_results\\Plots\\{path}_plot.png")
