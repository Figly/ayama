#!/usr/bin/env bash
set -efu

LOCAL_USERS_DIR='/Users'
SCRIPTS_DIR=$(dirname "$(python -c "import os; print(os.path.realpath('$0'))")")
KUBERNETES_VERSION="v1.13.11"
INSTALLED_MINIKUBE=$(minikube version | cut -d 'v' -f 3 | cut -d . -f 1)

handle_dodgy_virtio () {
  echo "Disabling Virtio9p mounting of /Users dir and starting minikube again"
  sed -i"" -e '/"Virtio9p"/ s/true/false/'  ~/.minikube/machines/minikube/config.json
  minikube stop
  minikube start
}

handle_ip_address_failure () {
  echo "Deleting .PID file and restarting minikube"
  minikube stop
  rm -f ~/.minikube/machines/minikube/hyperkit.pid
  minikube start
}

. "${SCRIPTS_DIR}/_colours.sh"

if [[ "$(uname -s)" = 'Linux' ]]; then
  CLIENT_OS='linux'
else
  CLIENT_OS='darwin'
  if [[ $(uname -r | cut -d . -f 1) > 18 ]]; then
    LOCAL_USERS_DIR='/System/Volumes/Data/Users'
  fi
fi

FIRST_RUN=""
if echo "$(minikube status)" | head -1 | grep -q -v "Stopped\|Running"; then
  FIRST_RUN=1
  # Default resource options for minikube host
  MINIKUBE_MEMORY='--memory=4096'
  MINIKUBE_CPUS='--cpus=2'
  MINIKUBE_DISKSIZE='--disk-size=40g'
  KUBERNETES_COMPAT_VERSION="--kubernetes-version ${KUBERNETES_VERSION}" # To maintain compatibility with kubectl and by extension production.
  while [ ! $# -eq 0 ]; do
    case "$1" in
      --memory=*)
        MINIKUBE_MEMORY=$1 ;;
      --cpus=*)
        MINIKUBE_CPUS=$1 ;;
      --disk-size=*)
        MINIKUBE_DISKSIZE=$1 ;;
    esac
    shift
  done
  MINIKUBE_ARGS="${MINIKUBE_MEMORY} ${MINIKUBE_CPUS} ${MINIKUBE_DISKSIZE} ${KUBERNETES_COMPAT_VERSION} --insecure-registry '10.0.0.0/24'"
  echo_red 'No Minikube VM found.'
  echo "Creating minikube VM..."
  if [[ "${CLIENT_OS}" == 'darwin' ]]; then
    echo "(Using the hyperkit driver already installed in 'make bootstrap')"
    echo "/Users -network 192.168.64.0 -mask 255.255.255.0 -alldirs -maproot=root:wheel" | sudo tee -a /etc/exports
    sudo nfsd restart
    eval "minikube start ${MINIKUBE_ARGS} --vm-driver=hyperkit" || handle_dodgy_virtio || handle_ip_address_failure
  else
    sudo apt-get update
    sudo apt-get install libvirt-bin qemu-kvm nfs-kernel-server
    sudo usermod -a -G libvirtd "$(whoami)"
    newgrp libvirtd
    sudo curl -L https://storage.googleapis.com/minikube/releases/latest/docker-machine-driver-kvm2 -o /usr/bin/docker-machine-driver-kvm2
    sudo chmod +x /usr/bin/docker-machine-driver-kvm2
    echo "/home       192.168.0.0/255.255.0.0(rw,sync,no_root_squash,no_subtree_check)" | sudo tee -a /etc/exports
    sudo systemctl restart nfs-kernel-server && sleep 5
    eval "minikube start ${MINIKUBE_ARGS} --vm-driver=kvm2"
  fi
elif echo "$(minikube status)" | grep -q 'Stopped'; then
  echo_yellow 'Starting minikube.'
  if [[ -f /usr/local/bin/docker-machine-driver-hyperkit ]]; then
    if [ "${INSTALLED_MINIKUBE}" == "0" ]; then
      minikube start || handle_dodgy_virtio || handle_ip_address_failure
    else
      minikube start --kubernetes-version ${KUBERNETES_VERSION} || handle_dodgy_virtio || handle_ip_address_failure
    fi
  else
    if [ "${INSTALLED_MINIKUBE}" == "0" ]; then
      minikube start || handle_dodgy_virtio
    else
      minikube start --kubernetes-version ${KUBERNETES_VERSION} || handle_dodgy_virtio
    fi
  fi

else
  echo_green 'Minikube is running.'
fi

eval "$(minikube docker-env)"
if [[ "${CLIENT_OS}" = 'darwin' ]]; then
  if ! docker info | grep -E "provider=(hyperkit|xhyve)"; then
    echo_red "hyperkit and xhyve are the only supported VM drivers for OSX"
    echo_red "It looks like you're using:"
    echo_red "    $(docker info | grep provider=)"
    exit 1
  fi

  echo "Starting and mounting NFS on Minikube"
  set +e
  minikube ssh -- sudo mkdir -p /Users
  if [[ "$(minikube ssh -- "grep '^NAME=' /etc/os-release | sed -e 's/NAME=//g'")" == "Boot2Docker" ]]; then
    minikube ssh -- sudo /usr/local/etc/init.d/nfs-client start
    minikube ssh -- "if [ -z \"\$(mount | grep User | grep 192.168.64.1)\" ]; then sudo mount 192.168.64.1:${LOCAL_USERS_DIR} /Users -o rw,async,noatime,rsize=32768,wsize=32768,proto=tcp; fi"
  else
    minikube ssh -- "if [[ ! \$(grep \"192.168.64.1:${LOCAL_USERS_DIR}\" /etc/fstab) ]]; then echo -e \"192.168.64.1:${LOCAL_USERS_DIR}\t/Users\tnfs\trw,async,noatime,rsize=32768,wsize=32768,proto=tcp\t0\t0\" | sudo tee -a /etc/fstab; fi"
    minikube ssh -- "sudo mount -a"
  fi
  set -e
else
  if ! docker info | grep "provider=kvm"; then
    echo_red "KVM is the only supported VM driver for Linux"
    echo_red "It looks like you're using:"
    echo_red "    $(docker info | grep provider=)"
    exit 1
  fi

  HOST_IP=$(ifconfig virbr1 | awk '/inet addr/{split($2,a,":"); print a[2]}')

  echo "Starting and mounting NFS on Minikube"
  set +e
  minikube ssh -- sudo mkdir -p /Users
  if [[ "$(minikube ssh -- "grep '^NAME=' /etc/os-release | sed -e 's/NAME=//g'")" == "Boot2Docker" ]]; then
    minikube ssh -- sudo /usr/local/etc/init.d/nfs-client start
    minikube ssh -- "if [ -z \"\$(mount | grep home | grep ${HOST_IP})\" ]; then sudo mount ${HOST_IP}:/home /Users -o rw,async,noatime,rsize=32768,wsize=32768,proto=tcp,nolock; fi"
  else
    minikube ssh -- "if [ -z \"\$(mount | grep home | grep ${HOST_IP})\" ]; then sudo busybox mount -t nfs -oasync,noatime,nolock ${HOST_IP}:/home /Users; fi"
  fi
  minikube ssh -- sudo ln -s "/Users/${USER}/" /home/
  set -e
fi
eval "$(minikube docker-env)"


set +x

echo ""
echo ""
echo "If you get errors relating to not talking to the docker daemon, you'll need to run:"
echo "    eval \$(minikube docker-env)"
echo ""
echo ""
