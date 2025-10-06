
FROM continuumio/miniconda3 AS base

RUN conda install -y -c conda-forge mamba

WORKDIR /app

# copiar solo el environment y crear env
COPY environment.yml .
RUN mamba env create -f environment.yml -n koi-env

# setear entorno para RUN posteriores
SHELL ["conda", "run", "-n", "koi-env", "/bin/bash", "-lc"]

# copiar código (esto es rápido y se puede cambiar sin rebuild del entorno)
COPY . .
COPY Front/test_input_real.csv /app/Front/test_input_real.csv

ENV PATH /opt/conda/envs/koi-env/bin:$PATH
ENV PREDICTOR_PATH=Front/models/ag_predictor
ENV PORT=8080
EXPOSE 8080

CMD ["conda", "run", "-n", "koi-env", "streamlit", "run", "Front/app_streamlit_min.py", "--server.port", "8080", "--server.address", "0.0.0.0", "--server.headless", "true"]

