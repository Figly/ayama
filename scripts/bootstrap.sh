#!/usr/bin/env bash
set -fu
set -o pipefail

ssh -q git@github.com
if [[ "$?" == "127" ]]; then
  echo "Please make sure you have SSH installed"
  exit 1
elif [[ "$?" == "255" ]]; then
  echo "Please make sure you have an SSH key for Github"
  exit 1
fi

which sudo
if [[ "$?" == "1" ]]; then
  function sudo() {
    $*
  }
fi

set -e

MINIKUBE_VERSION="1.11.0"
STERN_VERSION="1.10.0"
KUBECTL_VERSION="1.18.3"

if [[ "$(uname -s)" == 'Linux' ]]; then
  CLIENT_OS='linux'
  echo "Updating aptitude, so we don't need to do this later..."
  sudo apt-get update
else
  CLIENT_OS='darwin'
  if ! which brew &>/dev/null; then
    echo 'Brew not found.'
    echo 'Installing it...'
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  else
    echo 'Brew installed.'
  fi
  echo "Updating brew, so we don't need to do this later..."
  sudo chown -R $(whoami) /usr/local/var/homebrew
  brew update
fi

if ! which wget &>/dev/null; then
  echo 'wget not found.'
  echo 'Installing it...'
  if [[ "${CLIENT_OS}" == 'darwin' ]]; then
    brew install wget
  else
    sudo apt-get install -y wget
  fi
else
  echo 'wget installed.'
fi

if ! which tmate &>/dev/null; then
  echo 'tmate not found.'
  echo 'Installing it...'
  if [[ "${CLIENT_OS}" == 'darwin' ]]; then
    brew install tmate
  else
    sudo apt-get install -y tmate
  fi
else
  echo 'tmate installed.'
fi

if ! which pip3 &>/dev/null; then
  echo 'Python3 and pip3 not found.'
  echo 'Installing It...'
  if [[ "${CLIENT_OS}" == 'darwin' ]]; then
    brew install python3
  else
    sudo apt-get install -y python3 python3-pip
  fi
else
  echo 'Python3 and pip installed.'
fi

SCRIPTS_DIR=$(dirname "$(python -c "import os; print(os.path.realpath('$0'))")")

. "${SCRIPTS_DIR}/_colours.sh"

echo 'Checking requirements...'

if ! which git &>/dev/null; then
  echo 'Git not found.'
  echo 'Installing It...'
  if [[ "${CLIENT_OS}" == 'darwin' ]]; then
    brew install git
  else
    sudo apt-get install -y git
  fi
else
  echo_green 'Git installed.'
fi

if ! which docker &>/dev/null; then
  echo_red 'Docker not installed.'
  if [[ "${CLIENT_OS}" == 'darwin' ]]; then
    brew install docker
    brew link --overwrite docker
  else
    wget -O - https://get.docker.com/ | bash -
  fi
else
  echo_green 'Docker installed.'
fi

function install_kubectl() {
  wget -O kubectl "https://storage.googleapis.com/kubernetes-release/release/v${KUBECTL_VERSION}/bin/${CLIENT_OS}/amd64/kubectl"
  chmod +x kubectl
  sudo mv kubectl /usr/local/bin/
  echo_green 'Kubectl installed.'
}

function install_minikube() {
  wget -O minikube "https://storage.googleapis.com/minikube/releases/v${MINIKUBE_VERSION}/minikube-${CLIENT_OS}-amd64"
  chmod +x minikube
  sudo mv minikube /usr/local/bin/
  echo_green 'Minikube installed.'
}

function install_hyperkit_driver() {
  brew install docker-machine-driver-hyperkit
  if [[ -f $(brew --prefix)/opt/docker-machine-driver-hyperkit/bin/docker-machine-driver-hyperkit ]]; then
    sudo chown root:wheel $(brew --prefix)/opt/docker-machine-driver-hyperkit/bin/docker-machine-driver-hyperkit
    sudo chmod u+s $(brew --prefix)/opt/docker-machine-driver-hyperkit/bin/docker-machine-driver-hyperkit
  fi
  echo_green 'Hyperkit driver installed.'
}

function install_hyperkit_executable() {
  brew install hyperkit
  echo_green 'Hyperkit executable installed.'
}

function install_kvm_driver() {

  sudo apt-get install libvirt-bin qemu-kvm nfs-kernel-server
  sudo usermod -a -G libvirtd $(whoami)
  newgrp libvirtd
  sudo curl -L https://storage.googleapis.com/minikube/releases/latest/docker-machine-driver-kvm2 -o /usr/bin/docker-machine-driver-kvm2
  sudo chmod +x /usr/bin/docker-machine-driver-kvm2
}

if ! which gcloud &>/dev/null; then
  echo 'Google-cloud-SDK not found.'
  echo 'Installing it...'
  wget -O install.sh https://sdk.cloud.google.com
  chmod +x install.sh
  export CLOUDSDK_CORE_DISABLE_PROMPTS=1
  ./install.sh
  # This script is running as bash and this will add gcloud to our path
  . ~/google-cloud-sdk/path.bash.inc
  if [[ -t 1 ]]; then
    read -p "Woud you like us to add gcloud to your shell profile? (y/n) " -n 1 -r
    echo "This will allow auto-completion and using gcloud tools"
    echo
  else
    REPLY="n"
  fi
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [[ "${SHELL}" == "/bin/zsh" ]]; then
      echo 'source ~/google-cloud-sdk/completion.zsh.inc' >>~/.zshrc
      echo 'source ~/google-cloud-sdk/path.zsh.inc' >>~/.zshrc
    else
      if [[ "${CLIENT_OS}" == 'darwin' ]]; then
        echo 'source ~/google-cloud-sdk/completion.bash.inc' >>~/.bash_profile
        echo 'source ~/google-cloud-sdk/path.bash.inc' >>~/.bash_profile
      else
        echo 'source ~/google-cloud-sdk/completion.bash.inc' >>~/.bashrc
        echo 'source ~/google-cloud-sdk/path.bash.inc' >>~/.bashrc
      fi
    fi
  fi
  echo 'Loaded gcloud path'
else
  echo_green 'Google-cloud-SDK installed.'
fi

if ! which jq &>/dev/null; then
  echo 'jq not installed.'
  if [[ "${CLIENT_OS}" == 'darwin' ]]; then
    brew install jq
  else
    sudo apt-get install -y jq
  fi
else
  echo_green 'jq installed.'
fi

echo_yellow 'Updating gcloud SDK'
sudo gcloud components update

# remove gcloud kubectl if installed
if [[ $(which kubectl) == *google-cloud-sdk* ]]; then
  gcloud components remove kubectl --quiet
fi

echo_blue "Configuring GCR Auth"
gcloud auth configure-docker --quiet --verbosity=error

if ! which kubectl &>/dev/null; then
  echo 'Kubectl not installed or not in your path. Trying to install.'
  install_kubectl
else
  INSTALLED_KUBECTL=$(kubectl version --client --output=json | jq -r '.clientVersion.gitVersion')
  if [ "${INSTALLED_KUBECTL}" != "v${KUBECTL_VERSION}" ]; then
    install_kubectl
  fi
fi

if ! which minikube &>/dev/null; then
  echo 'Minikube not installed.'
  install_minikube
else
  INSTALLED_MINIKUBE=$(minikube version | cut -d 'v' -f 3)
  if [ "${INSTALLED_MINIKUBE}" != "${MINIKUBE_VERSION}" ]; then
    install_minikube
  fi
fi

if [[ "${CLIENT_OS}" == 'darwin' ]]; then
  if ! which docker-machine-driver-hyperkit &>/dev/null; then
    echo 'Hyperkit docker machine driver not installed or not in your path. Trying to install.'
    install_hyperkit_driver
  fi
  if ! which hyperkit &>/dev/null; then
    echo 'Hyperkit executable not installed or not in your path. Trying to install.'
    install_hyperkit_executable
  fi
else
  if ! which docker-machine-driver-kvm2 &>/dev/null; then
    echo 'KVM docker machine driver not installed or not in your path. Trying to install.'
    install_kvm_driver
  fi
fi

if ! which stern &>/dev/null; then
  echo 'Stern not installed.'
  wget -O stern "https://github.com/wercker/stern/releases/download/${STERN_VERSION}/stern_${CLIENT_OS}_amd64"
  chmod +x stern
  sudo mv stern /usr/local/bin/
else
  echo_green 'Stern installed.'
fi

# Install NVM
if [ ! -d ~/.nvm ]; then
  echo 'NVM not installed'
  if [[ "${CLIENT_OS}" == 'darwin' ]]; then
    # Because https://github.com/nodejs/node/issues/9377
    sudo rm -rf /usr/local/lib/node_modules
  fi
  wget -O - https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
fi

# Ignore MANPATH (not set) & 'files folder missing' bug in nvm installation
set +efu
set +o pipefail

# Select/Install compatible version of node
. ~/.nvm/nvm.sh
nvm install 6
echo_green 'NVM installed and Node 6 (LTS) selected'

set -efu
set -o pipefail

if ! which bower &>/dev/null; then
  echo 'Bower not installed.'
  sudo npm install -g bower
else
  echo_green 'Bower installed.'
fi

if ! which gulp &>/dev/null; then
  echo 'Gulp not installed.'
  sudo npm install -g gulp
else
  echo_green 'Gulp installed.'
fi

if ! which jinja2 &>/dev/null; then
  echo 'jinja2-cli not installed.'
  sudo python3 -m pip install jinja2-cli pyyaml
else
  echo_green 'jinja2-cli installed.'
fi

if ! which realpath &>/dev/null; then
  echo 'realpath / coreutils not installed.'
  brew install coreutils
else
  echo_green 'realpath / coreutils installed.'
fi

if ! which hostess &>/dev/null; then
  echo 'Hostess not installed.'
  if [[ "${CLIENT_OS}" == 'darwin' ]]; then
    brew install hostess
  else
    wget -O hostess "https://github.com/cbednarski/hostess/releases/download/v0.2.0/hostess_linux_amd64"
    chmod +x hostess
    sudo mv hostess /usr/local/bin/
  fi
else
  echo_green 'Hostess installed.'
fi

if [[ ! "$(minikube status)" == 'Running' ]]; then
  echo "Make sure you 'make up' to setup your local Kubernetes cluster before getting started."
else
  echo 'Minikube is running.'
  echo
  echo "You'll need to run the following before interacting with Docker:"
  echo "    eval \$(minikube docker-env)"
  echo
fi

echo "You must use KVM (Linux) or Xhyve(OSX), please follow:"
echo "    https://github.com/kubernetes/minikube/blob/master/docs/drivers.md"

echo "Checking GCP authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep "\@"; then
  if [[ -t 1 ]]; then
    echo "You will be taken to GCP to authenticate"
    sleep 5
    gcloud auth login
    echo "Just one more time. You will be taken to GCP to authenticate (so that stern/kb aliases just work)"
    sleep 5
    gcloud auth application-default login
  else
    echo "Running non-interactively"
  fi
else
  echo "GCP auth looks good 👌"
fi
