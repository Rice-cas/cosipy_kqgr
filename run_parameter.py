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

# Define new values for parameters in both files
# Loop to modify parameters in both TOML files and run COSIPY.py
for albedo_fresh_snow in np.arange(0.8, 0.82, 0.01):
    for albedo_firn in np.arange(0.5, 0.52, 0.01):
        for albedo_ice in np.arange(0.25, 0.27, 0.01):
            for albedo_mod_snow_aging in np.arange(15, 17, 2):
                for albedo_mod_snow_depth in np.arange(5, 7, 2):
                    # Use np.arange for floating-point values
                    # Update parameters in constants.toml

                    update_config_file(constant_file, 'CONSTANTS', 'albedo_fresh_snow', albedo_fresh_snow)
                    update_config_file(constant_file, 'CONSTANTS', 'albedo_firn', albedo_firn)
                    update_config_file(constant_file, 'CONSTANTS', 'albedo_ice', albedo_ice)
                    update_config_file(constant_file, 'CONSTANTS', 'albedo_mod_snow_aging', albedo_mod_snow_aging)
                    update_config_file(constant_file, 'CONSTANTS', 'albedo_mod_snow_depth', albedo_mod_snow_depth)
                    
                    # Update parameters in config.toml
                    update_config_file(config_file, 'FILENAMES', 'output_prefix', 
                        f'kqgr_as{albedo_fresh_snow}_af{albedo_firn}_ai{albedo_ice}_sa{albedo_mod_snow_aging}_sd{albedo_mod_snow_depth}')

                    
                    # Run COSIPY.py script
                    run_cosipy_script()

                    # Optional: sleep for a short period before the next run
                    time.sleep(10)  # Adjust as needed