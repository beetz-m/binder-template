# Wind turbine robotics labs: line simulation, replacement matrix, service mission, cramera scenes

[![Binder](https://binder.intel4coro.de/badge_logo.svg)](https://binder.intel4coro.de/v2/gh/beetz-m/binder-template/wind_line_sim_vrb_lab?urlpath=lab/tree/notebooks/line_simulation.ipynb)

A virtual lab of the **Robotics for Offshore Wind** Virtual Research Building (AICOR, University of Bremen), prepared for
the Siemens Energy Innovation Lab in Cuxhaven. It runs the discrete-event model of a nacelle assembly line from the
research twin [CuxhavenSiteTwin](https://github.com/beetz-m/CuxhavenSiteTwin), pinned to commit `31685f5`. It shows
which levers raise output (robot bolting, a robot cell at the cabling station, plug-in skids, shifts, AGVs), how
sure the model is (8 seeds, spread, bottleneck counts), and where a robot's case rests on safety and quality rather
than throughput.

A second notebook runs the twin's **replacement matrix**. It asks which of 20 selected nacelle components a robot team
(legged robot, cargo drone, nacelle hoist with a robotic crane) can exchange offshore without an external heavy lift.
Visitors can change the hatch, the kit shaft, the payloads and the hoist capacity, and see how the nacelle's design
decides whether robots can service it.

A third notebook schedules the twin's **service mission M1**, a robot-only visit at a wind turbine. It shows which
steps set the length of the visit, checks the plan against the twin's weather limits, and lets visitors drop the
pump-motor exchange, keep a resident robot in the nacelle or slow the robots down.

The **cramera viewer** shows the twin's scenes in 3D in the browser: the Cuxhaven port and yard, the factory hall,
the Windanker wind farm (turbine positions illustrative), hub station H1, and a recorded run of a PR2 robot supplying
kits at H1 (simulated, planned with CRAM). Visitors can orbit, select parts, browse the scene graph and replay the
recording. The scenes are a release asset of the twin, `cramera-scenes-31685f5`, about 390 MB. The image downloads
the asset and checks its SHA-256. Questions in the entity query language need the live CRAM stack and do not work in
this static viewer.

The twin is reconstructed from public and second-hand sources. It is not the real plant and uses no Siemens Energy
data; station times are our own estimates. Siemens Energy does not run or endorse this lab.

## Launch

| Link | Opens |
|---|---|
| [**Line simulation**](https://binder.intel4coro.de/v2/gh/beetz-m/binder-template/wind_line_sim_vrb_lab?urlpath=lab/tree/notebooks/line_simulation.ipynb) | `notebooks/line_simulation.ipynb` in JupyterLab |
| [**Replacement matrix**](https://binder.intel4coro.de/v2/gh/beetz-m/binder-template/wind_line_sim_vrb_lab?urlpath=lab/tree/notebooks/replacement_matrix.ipynb) | `notebooks/replacement_matrix.ipynb` in JupyterLab |
| [**Service mission**](https://binder.intel4coro.de/v2/gh/beetz-m/binder-template/wind_line_sim_vrb_lab?urlpath=lab/tree/notebooks/service_mission.ipynb) | `notebooks/service_mission.ipynb` in JupyterLab |
| [**cramera viewer**](https://binder.intel4coro.de/v2/gh/beetz-m/binder-template/wind_line_sim_vrb_lab?urlpath=cramera/) | the 3D scenes (port, hall, Windanker, H1, recorded PR2 run) |
| [**VSCode**](https://binder.intel4coro.de/v2/gh/beetz-m/binder-template/wind_line_sim_vrb_lab?urlpath=vscode) | the repository in VSCode |

The first launch builds the image and can take a while; later launches are quick until the next push.

## Layout

- `binder/Dockerfile`: the minimal flavor of the template, without CRAM or a ROS workspace. It clones the twin into
  `/home/repo/CuxhavenSiteTwin`, pinned by `TWIN_COMMIT`.
- `notebooks/line_simulation.ipynb`: the line model. Runs in about 15 s.
- `notebooks/replacement_matrix.ipynb`: the replacement matrix. Runs in about 1 s.
- `notebooks/service_mission.ipynb`: the service-mission planner. Runs in a few seconds.
- `requirements.txt`: numpy, matplotlib, ipywidgets, jupyter-server-proxy.
- `binder/cramera_proxy/`: a small package that registers the static cramera site with jupyter-server-proxy at
  `<lab>/cramera/`. The site lands in `/home/repo/cramera_site` (git-ignored).

Scene credits: orthophotos and building models © LGLN 2026, dl-de/by-2-0; map data © OpenStreetMap contributors, ODbL;
PR2 description (Willow Garage), BSD licence. See `cramera_site/ATTRIBUTION.md` in the running lab.

Run it locally without Docker: clone the twin next to this repository as `CuxhavenSiteTwin/` (it is git-ignored),
install the requirements and open the notebook.

The template's demo files (`notebooks/demo.ipynb`, `demo_ui.py`, `utils.py`, `rviz/`, `*.rviz`, `webapps.json`,
`binder/desktop-widget/`) are left over from the template and are not used by this lab.
