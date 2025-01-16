import os

def generate_starfield_script(start_longitude, start_latitude, step, grid_size, output_directory, script_filename):
    with open(script_filename, 'w') as script_file:
        for i in range(-grid_size, grid_size + 1):
            for j in range(-grid_size, grid_size + 1):
                longitude = start_longitude + i * step
                latitude = start_latitude + j * step
                output_path = os.path.join(output_directory, f'starfield_{longitude}_{latitude}.png')
                script_file.write(f'// Point and capture commands for Celestia\n')
                script_file.write(f'celestia point-to {longitude} {latitude} 10000\n')
                script_file.write(f'celestia capture-starfield {output_path}\n')
                script_file.write(f'wait 0.5\n')

def capture_starfields(start_longitude=0, start_latitude=0, step=10, grid_size=18, output_directory='celestia_starfields', refine=False):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    script_filename = 'celestia_script.txt'
    generate_starfield_script(start_longitude, start_latitude, step, grid_size, output_directory, script_filename)
    run_celestia_script(script_filename)

def run_celestia_script(script_filename):
    os.system(f'celestia --script {script_filename}')
