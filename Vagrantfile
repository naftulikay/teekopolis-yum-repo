# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.define "fedora23" do |fedora23|
#   create a Fedora 23 box for building Fedora 23 packages
    fedora23.vm.box = "fedora/fedora-cloud-23"
    fedora23.vm.box_url = "https://download.fedoraproject.org/pub/fedora/linux/releases/23/Cloud/x86_64/Images/Fedora-Cloud-Base-Vagrant-23-20151030.x86_64.vagrant-virtualbox.box"
    fedora23.vm.hostname = "fedora23"

    fedora23.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "ansible/fedora23.yml"
      ansible.sudo = true
    end

    fedora23.vm.synced_folder ".", "/vagrant", type: "virtualbox"
  end

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", type: "dhcp"

  config.vm.provider "virtualbox" do |vb|
    # Use VBoxManage to customize the VM. For example to change memory:
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end
end
