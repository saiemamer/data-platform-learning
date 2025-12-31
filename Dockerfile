# We use Python 3.11 Slim (matching your company's production image)
FROM python:3.11-slim-bookworm

# 1. Install OS Dependencies
# These are the tools your company installs in their base image
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    wget \
    zsh \
    vim \
    nano \
    openssh-client \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Google Cloud SDK (CLI)
# This allows us to run 'gcloud auth login'
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin
RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-464.0.0-linux-x86_64.tar.gz && \
    mkdir -p /usr/local/gcloud && \
    tar -C /usr/local/gcloud -xvf google-cloud-cli-464.0.0-linux-x86_64.tar.gz && \
    /usr/local/gcloud/google-cloud-sdk/install.sh && \
    rm google-cloud-cli-464.0.0-linux-x86_64.tar.gz

# 3. Python Setup (Poetry + DBT)
WORKDIR /dbt
# We are upgrading these to match your company's exact versions
RUN pip install --no-cache-dir \
    dbt-core==1.9.2 \
    dbt-bigquery==1.9.1 \
    sqlfluff==3.2.5 \
    pre-commit \
    pyyaml \
    google-cloud-bigquery==3.25.0 \
    python-gitlab

# 4. Developer Experience (ZSH & Aliases)
# Install Oh My Zsh for a nice terminal experience
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# 5. Create the Aliases (Replicating your 'scripts/utility/aliases.sh')
# This creates the 'glogin' command you are used to.
RUN echo 'alias glogin="gcloud auth login --update-adc && echo \"Auth Complete\""' >> /root/.zshrc
RUN echo 'alias dbt="dbt"' >> /root/.zshrc
# Set ZSH as default
ENV SHELL /bin/zsh

CMD ["tail", "-f", "/dev/null"]