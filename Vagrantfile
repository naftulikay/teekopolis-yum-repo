# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.define "fedora24" do |fedora24|
#   create a Fedora 23 box for building Fedora 23 packages
    fedora24.vm.box = "fedora/fedora-cloud-24"
    fedora24.vm.box_url = "https://download.fedoraproject.org/pub/fedora/linux/releases/24/CloudImages/x86_64/images/Fedora-Cloud-Base-Vagrant-24-1.2.x86_64.vagrant-virtualbox.box"
    fedora24.vm.hostname = "fedora24"

    fedora24.vm.provision "shell", inline: "dnf install -y bash-completion make gcc python-2.7.11 libselinux-python python2-dnf python-devel"

    fedora24.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/vagrant.yml"
      ansible.sudo = true
    end

    fedora24.vm.synced_folder ".", "/vagrant", type: "virtualbox"
  end

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", type: "dhcp"

  config.vm.provider "virtualbox" do |vb|
    # Use VBoxManage to customize the VM. For example to change memory:
    vb.customize ["modifyvm", :id, "--memory", "4096"]
    # 8 VCPUs
    vb.customize ["modifyvm", :id, "--cpus", "8"]
  end
end
