from .read_lammps_out import read_species_out
import matplotlib.pyplot as plt
import pandas as pd

def read_in_data(file_name="species.out") -> pd.DataFrame:
    if file_name[-4:] == ".csv":
        species_df = pd.read_csv(file_name)
        for column in species_df.columns:
            species_df[column] = pd.to_numeric(species_df[column])
    else: 
        species_df = read_species_out(file_name)
    return species_df

def get_n_max(dataframe:pd.DataFrame,num_vals:int,ignore:list=[]) -> list[str]:
    vals = []
    for column in dataframe.columns:
        if column != "Timestep" and not column in ignore:
            vals.append((column,dataframe[column].max()))
    vals = sorted(vals,key=lambda x:x[1],reverse=True)
    return vals[:num_vals]

def get_n_max_cycle(dataframe:pd.DataFrame,num_vals:int,ignore:list=[]) -> list[str]:

    # Get the first set
    species_of_interest = get_n_max(dataframe,num_vals,ignore)
    print(f"Top {num_vals} species.")
    for species in species_of_interest:
        print(species)

    # Iteratevly remove species as needed
    print("If there are any you don't want included please type them below. You may specify multiple and seperate them by spaces. If you would not like to add species, leave it blank.")
    species_to_ignore = input("Species to ignore: ").strip().split()

    while species_to_ignore != []:
        for i in species_to_ignore:
            ignore.append(i)
        species_of_interest = get_n_max(dataframe,num_vals,ignore)

        for species in species_of_interest:
            print(species)

        print("If there are any you don't want included please type them below. You may specify multiple and seperate them by spaces. If you would not like to add species, leave it blank.")
        species_to_ignore = input("Species to ignore: ").strip().split()
    
    return species_of_interest


def species_vs_time_quickplot(dataframe:pd.DataFrame,keys_to_plot,time_step_lower=None,time_step_upper=None,is_transparent=False,outfile_name="species_vs_time.png",figure_title="Species over time"):
    temp_dataframe = dataframe.copy()
    if time_step_lower != None:
        temp_dataframe = temp_dataframe[temp_dataframe["Timestep"]>= time_step_lower]
    if time_step_upper != None:
        temp_dataframe = temp_dataframe[temp_dataframe["Timestep"]<= time_step_upper]
    
    for key in keys_to_plot:
        if key in temp_dataframe.columns:
            plt.plot(temp_dataframe["Timestep"],temp_dataframe[key],label=key)
    plt.title(figure_title)
    plt.xlabel("Time Step")
    plt.ylabel("Species Count")
    plt.legend()
    plt.savefig(outfile_name,bbox_inches="tight",transparent=is_transparent)
    print(f"{outfile_name} created")

if __name__ == "__main__":
    print("Hello  World")
