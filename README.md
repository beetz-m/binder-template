# IIS Lecture 3 lab: the robot–world manipulation system in description logic

[![Binder](https://binder.intel4coro.de/badge_logo.svg)](https://binder.intel4coro.de/v2/gh/beetz-m/binder-template/iis_l3_dl_vrb_lab?urlpath=lab/tree/iis_l3_dl/sheet3/sheet3_dl_lab.ipynb)

Lab for Exercise Sheet 3, Task 8, of the course *Integrated Intelligent Systems* (AICOR, University of Bremen). The
notebook runs the course's teaching ontology of the robot–world manipulation system, every concept specialized from
the upper ontology DUL, with the reasoner HermiT: it reproduces the lecture's nine competency questions and lets
students extend the ontology for the cereal-box errand and query it. Java and owlready2 are preinstalled.

**Launch:** [open the notebook in JupyterLab](https://binder.intel4coro.de/v2/gh/beetz-m/binder-template/iis_l3_dl_vrb_lab?urlpath=lab/tree/iis_l3_dl/sheet3/sheet3_dl_lab.ipynb) (the first launch builds the image and can take a while).

| folder | content |
|---|---|
| `iis_l3_dl/sheet3/` | `sheet3_dl_lab.ipynb`, the lab notebook (Task 8), and its README |
| `iis_l3_dl/dl/` | the teaching ontology (`rwms_ontology.py`), DUL (`DUL.owl`, DOLCE+DnS Ultralite, EASE copy v3.34), helpers |
| `iis_l3_dl/carton_model.py` | the causal model used for the one numeric competency question |

The lab files are copies from the course repository (`writing/lecture-course/lectures/03-scientific-object/` in
ResearchSpace); update them there and copy them over.

---

Built from the [EASE VRB binder template](https://github.com/aicor-vrb/binder-template) (minimal flavor: no CRAM, no
ROS workspace; base image `intel4coro/jupyter-ros2:jazzy-py3.12` with a Java runtime added for HermiT).
