# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  #config.ssh.insert_key = false

  config.vm.box = "debian/contrib-jessie64"
  config.vm.boot_timeout = 600

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = ".vagrant_provisioning/playbook.yml"
    # ansible.tags = ""
    # ansible.verbose = "vvv"
  end

  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 3306, host: 51524

  config.vm.network "private_network", ip: "192.168.33.99"

  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--cableconnected1", "on"]
  end

  config.vm.provider "virtualbox" do |provider|
    provider.customize ["modifyvm", :id, "--memory", "1024"]
  end

  config.vm.provider "vmware" do |provider|
    provider.customize ["modifyvm", :id, "--memory", "1024"]
  end

  # vagrant-hostupdater configuration
  config.vm.define "pbw-django" do |machine|
    machine.vm.box = "debian/contrib-jessie64"
    machine.vm.hostname = "pbw-django.vagrant"
    machine.vm.network "private_network", ip: "192.168.33.99"
  end
end
