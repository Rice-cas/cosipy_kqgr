import toml
import subprocess
import time
import numpy as np

def update_config_file(config_file, section, key, value):
    """
    Update a key in the specified section of the TOML configuration file, ensuring the value is a float.
    """
    if config_file == 'constants.toml':
        # 强制将 value 转换为 float
        value = float(value)
    
    # Load the current configuration
    config = toml.load(config_file)
    
    # Check if section exists
    if section in config:
        # Check if key exists in the section
        if key in config[section]:
            # Update the key in the section with the float value
            config[section][key] = value
        else:
            print(f"Key '{key}' not found in section '{section}' of {config_file}")
    else:
        print(f"Section '{section}' not found in {config_file}")
    
    # Save the updated configuration back to the file
    with open(config_file, 'w') as f:
        toml.dump(config, f)
    
    print(f"Updated {key} in {section} to {value} (as float) in {config_file}")


def run_cosipy_script():
    """
    Run the COSIPY.py script using subprocess.
    """
    result = subprocess.run(['python', 'COSIPY.py'], capture_output=True, text=True)

    if result.returncode == 0:
        print("COSIPY.py ran successfully!")
    else:
        print(f"Error running COSIPY.py: {result.stderr}")


# Define file paths
constant_file = 'constants.toml'
config_file = 'config.toml'
# Flag to track if this is the first run
first_run = True  # Initialize the flag to True for the first run

# Loop to modify parameters in both TOML files and run COSIPY.py
for year in range(2015, 2020):
    # Update 'restart' parameter based on whether it's the first run
    if first_run:
        update_config_file(config_file, 'RESTART', 'restart', False)  # Set to False on first run
        first_run = True  # Set the flag to False after the first run
            # Update parameters in config.toml
        update_config_file(config_file, 'FILENAMES', 'output_prefix', f'ERA5_{year}')
        update_config_file(config_file, 'FILENAMES', 'input_netcdf', f'ERA5/ERA5_{year}.nc')
        update_config_file(config_file, 'SIMULATION_PERIOD', 'time_start', f'{year}-01-01T00:00')
        update_config_file(config_file, 'SIMULATION_PERIOD', 'time_end', f'{year+1}-01-01T00:00')

    else:
        update_config_file(config_file, 'RESTART', 'restart', True)  # Set to True on subsequent runs
        update_config_file(config_file, 'FILENAMES', 'output_prefix', f'ERA5_{year}')
        update_config_file(config_file, 'FILENAMES', 'input_netcdf', f'ERA5/ERA5_{year}.nc')
        update_config_file(config_file, 'SIMULATION_PERIOD', 'time_start', f'{year-1}-12-31T23:00')
        update_config_file(config_file, 'SIMULATION_PERIOD', 'time_end', f'{year+1}-01-01T00:00')



    # Run COSIPY.py script
    run_cosipy_script()

    # Optional: sleep for a short period before the next run
    time.sleep(8)  # Adjust as needed
