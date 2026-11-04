# Sheet 3 lab: the errand in description logic (Task 8)

`sheet3_dl_lab.ipynb` runs the course's teaching ontology of the robot–world manipulation system with the reasoner
HermiT. Open it in Jupyter from this folder and run the cells from top to bottom.

- **Needs:** Python 3.10 or newer, Java (HermiT is a Java program; e.g. `sudo apt install default-jre`), and
  `owlready2` (the first cell installs it with pip if it is missing; it bundles HermiT).
- **Uses:** `../dl/rwms_ontology.py` (the ontology), `../dl/DUL.owl` (DOLCE+DnS Ultralite, the EASE copy, v3.34;
  source: ontologydesignpatterns.org, Gangemi et al.), `../dl/lab_helpers.py` (fresh copies, consistency checks,
  part-of queries), and `../carton_model.py` for the one numeric question.
- **In this Binder lab** Java and owlready2 are preinstalled; just run the cells.
