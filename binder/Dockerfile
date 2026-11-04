# Dockerfile for the VRB lab "IIS Lecture 3: the robot–world manipulation system in description logic"
#
# Minimal flavor: no CRAM, no ROS workspace. The lab runs the course's teaching ontology (owlready2) with the
# reasoner HermiT, which needs a Java runtime.
# Base image (ROS 2 + JupyterLab + VSCode + VNC desktop): https://github.com/IntEL4CoRo/jupyter-ros2
#
# Build-cache rule: slow, rarely changing steps at the TOP; steps using this repository's files after COPY.
FROM intel4coro/jupyter-ros2:jazzy-py3.12

USER root
ENV DEBIAN_FRONTEND=noninteractive

# JupyterLab's file browser is rooted at ${REPO_DIR}; everything the visitor should see goes below it.
ENV REPO_DIR=/home/repo
RUN mkdir -p ${REPO_DIR}

#================= SYSTEM PACKAGES (apt) =====================================#
# HermiT (bundled with owlready2) is a Java program.
RUN apt update && apt install -y --no-install-recommends default-jre-headless && rm -rf /var/lib/apt/lists/*

#================= PYTHON PACKAGES (pip) ======================================#
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt

#================= COPY THIS REPOSITORY INTO THE IMAGE ========================#
# Everything below this line re-runs on every push.
COPY . ${REPO_DIR}/
RUN git config --global --add safe.directory ${REPO_DIR}

# JupyterLab and VSCode start in the repository
WORKDIR ${REPO_DIR}
ENV CODE_WORKING_DIRECTORY=${REPO_DIR}

#================= ENTRYPOINT =================================================#
COPY binder/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
