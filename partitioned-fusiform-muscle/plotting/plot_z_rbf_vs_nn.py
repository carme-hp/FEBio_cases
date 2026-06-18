import subprocess
import matplotlib.pyplot as plt

# -------------------------------------------------
# CASES
# -------------------------------------------------

cases2 = [

    {
        "vtu": "results_rbf2x2x8/results-opendihu-muscle/muscle_0000299.vtu",
        "el": [2, 2, 8]
    },

    {
        "vtu": "results_rbf4x4x16/results-opendihu-muscle/muscle_0000299.vtu",
        "el": [4, 4, 16]
    },

    {
        "vtu": "results_rbf8x8x32/results-opendihu-muscle/muscle_0000299.vtu",
        "el": [8, 8, 32]
    },

    {
        "vtu": "results_rbf12x12x24/results-opendihu-muscle/muscle_0000299.vtu",
        "el": [12, 12, 24]
    },


    {
        "vtu": "results_rbf16x16x64/results-opendihu-muscle/muscle_0000299.vtu",
        "el": [16, 16, 64]
    }

]

cases1 = [

    {
        "vtu": "results_2x2x8/results-opendihu-muscle/muscle_0000299.vtu",
        "el": [2, 2, 8]
    },

    {
        "vtu": "results_4x4x16/results-opendihu-muscle/muscle_0000299.vtu",
        "el": [4, 4, 16]
    },

    {
        "vtu": "results_8x8x32/results-opendihu-muscle/muscle_0000299.vtu",
        "el": [8, 8, 32]
    },

    {
        "vtu": "results_16x16x64/results-opendihu-muscle/muscle_0000299.vtu",
        "el": [16, 16, 64]
    }

]

cases3 = [

    {
        "vtu": "results_8x8x32/results-opendihu-muscle/muscle_0000299.vtu",
        "el": [8, 8, 32]
    }

]

# -------------------------------------------------
# FUNCTION TO PROCESS CASES
# -------------------------------------------------

def process_cases(cases):

    num_elements = []
    average_z_values = []

    for case in cases:

        el_x, el_y, el_z = case["el"]

        cmd = [
            "python",
            "compute_average_z.py",
            case["vtu"],
            str(el_x),
            str(el_y),
            str(el_z)
        ]

        result = subprocess.check_output(cmd)

        average_z = float(result.decode().strip())

        total_elements = el_x * el_y * el_z

        num_elements.append(total_elements)
        average_z_values.append(average_z)

        print(f"Elements: {total_elements}")
        print(f"Average z: {average_z}")

    return num_elements, average_z_values

# -------------------------------------------------
# RUN BOTH CASE SETS
# -------------------------------------------------

num_elements1, average_z_values1 = process_cases(cases1)
num_elements2, average_z_values2 = process_cases(cases2)
num_elements3, average_z_values3 = process_cases(cases3)

# -------------------------------------------------
# PLOT
# -------------------------------------------------

plt.figure(figsize=(8, 6))

plt.plot(
    num_elements1,
    average_z_values1,
    marker='o',
    label='RBF mapping'
)

plt.plot(
    num_elements2,
    average_z_values2,
    marker='s',
    label='NN mapping'
)

plt.plot(
    num_elements3,
    average_z_values3,
    marker='s',
    label='rbf + mat'
)


plt.xscale('log')

plt.xlabel("Total number of elements")
plt.ylabel("Average z-coordinate")
plt.title("Convergence of average z")

plt.grid(True)
plt.legend()

plt.show()