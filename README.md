# Wind nacelle line simulation: a VRB lab

[![Binder](https://binder.intel4coro.de/badge_logo.svg)](https://binder.intel4coro.de/v2/gh/beetz-m/binder-template/wind_line_sim_vrb_lab?urlpath=lab/tree/notebooks/line_simulation.ipynb)

A virtual lab of the **Robotics for Offshore Wind** Virtual Research Building (AICOR, University of Bremen), prepared for
the Siemens Energy Innovation Lab in Cuxhaven. It runs the discrete-event model of a nacelle assembly line from the
research twin [CuxhavenSiteTwin](https://github.com/beetz-m/CuxhavenSiteTwin), pinned to commit `31685f5`. It shows
which levers raise output (robot bolting, a robot cell at the cabling station, plug-in skids, shifts, AGVs), how
sure the model is (8 seeds, spread, bottleneck counts), and where a robot's case rests on safety and quality rather
than throughput.

The twin is reconstructed from public and second-hand sources. It is not the real plant and uses no Siemens Energy
data; station times are our own estimates. Siemens Energy does not run or endorse this lab.

## Launch

| Link | Opens |
|---|---|
| [**Notebook**](https://binder.intel4coro.de/v2/gh/beetz-m/binder-template/wind_line_sim_vrb_lab?urlpath=lab/tree/notebooks/line_simulation.ipynb) | `notebooks/line_simulation.ipynb` in JupyterLab |
| [**VSCode**](https://binder.intel4coro.de/v2/gh/beetz-m/binder-template/wind_line_sim_vrb_lab?urlpath=vscode) | the repository in VSCode |

The first launch builds the image and can take a while; later launches are quick until the next push.

## Layout

- `binder/Dockerfile`: the minimal flavor of the template, without CRAM or a ROS workspace. It clones the twin into
  `/home/repo/CuxhavenSiteTwin`, pinned by `TWIN_COMMIT`.
- `notebooks/line_simulation.ipynb`: the lab. Runs in about 15 s.
- `requirements.txt`: numpy, matplotlib, ipywidgets.

Run it locally without Docker: clone the twin next to this repository as `CuxhavenSiteTwin/` (it is git-ignored),
install the requirements and open the notebook.

The template's demo files (`notebooks/demo.ipynb`, `demo_ui.py`, `utils.py`, `rviz/`, `*.rviz`, `webapps.json`,
`binder/desktop-widget/`) are left over from the template and are not used by this lab.
