# Dockerfile for the VRB lab "Wind nacelle line simulation" (Robotics for Offshore Wind VRB)
#
# Minimal flavor: no CRAM, no ROS workspace. The lab runs the discrete-event line model of the
# CuxhavenSiteTwin research twin (pure Python) in a notebook.
# Base image (ROS 2 + JupyterLab + VSCode + VNC desktop): https://github.com/IntEL4CoRo/jupyter-ros2
#
# Build-cache rule: slow, rarely changing steps at the TOP; steps using this repository's files after COPY.
FROM intel4coro/jupyter-ros2:jazzy-py3.12

USER root
ENV DEBIAN_FRONTEND=noninteractive

# JupyterLab's file browser is rooted at ${REPO_DIR}; everything the visitor should see goes below it.
ENV REPO_DIR=/home/repo
RUN mkdir -p ${REPO_DIR}

#================= EXTERNAL REPOSITORIES ======================================#
# The research twin, pinned to the commit the VRB reads its results from. Change TWIN_COMMIT together with
# data/twin/PINNED_COMMIT in the VRB (~/ResearchSpace/studios/WindVRB).
ARG TWIN_COMMIT=31685f52c7618ea1e00ec4f0492e39cd606141f3
ENV PROJECT_DIR=${REPO_DIR}/CuxhavenSiteTwin
RUN git clone https://github.com/beetz-m/CuxhavenSiteTwin.git ${PROJECT_DIR} && \
    git -C ${PROJECT_DIR} checkout ${TWIN_COMMIT} && \
    git config --global --add safe.directory ${PROJECT_DIR}

# cramera viewer with the twin's scenes, as a static site (release asset of the twin, checksum-verified).
# Served inside JupyterLab by jupyter-server-proxy at <lab>/cramera/ (package binder/cramera_proxy).
ARG SCENES_URL=https://github.com/beetz-m/CuxhavenSiteTwin/releases/download/cramera-scenes-31685f5/cramera-scenes-31685f5.tar.gz
ARG SCENES_SHA256=5373829da9fedbfa48d2b49dd6862481089448800a736b6a03d47a3dec52940e
RUN curl -fsSL -o /tmp/scenes.tar.gz "${SCENES_URL}" && \
    echo "${SCENES_SHA256}  /tmp/scenes.tar.gz" | sha256sum -c - && \
    tar -xzf /tmp/scenes.tar.gz -C ${REPO_DIR} && mv ${REPO_DIR}/csite ${REPO_DIR}/cramera_site && \
    rm /tmp/scenes.tar.gz

#================= PYTHON PACKAGES (pip) ======================================#
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt

#================= COPY THIS REPOSITORY INTO THE IMAGE ========================#
COPY . ${REPO_DIR}/
RUN git config --global --add safe.directory ${REPO_DIR}

WORKDIR ${REPO_DIR}
ENV CODE_WORKING_DIRECTORY=${REPO_DIR}

# Register the cramera viewer with jupyter-server-proxy (entry point jupyter_serverproxy_servers)
RUN python3 -m pip install --no-cache-dir ${REPO_DIR}/binder/cramera_proxy

#================= ENTRYPOINT =================================================#
COPY binder/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
