# -*- mode: ruby -*-
# vi: set ft=ruby :


# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|

  config.vm.synced_folder '.', '/vagrant', disabled: true

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "centos/7"

  # Forward your local keys to the vagrant host. If more than the creator of this
  # vagrant host can access the host, comment this out.
  config.ssh.forward_agent = true

  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.
  config.vm.provider "virtualbox" do |v|
    v.memory = 125000
    v.cpus = 32
    # I moved this out of the default values so I could configure libvirt to also use the disk
    # parameter. If you get an error, please double check this. -JRS
    v.disksize.size = '80GB'
  end

  #config.disksize.size = '80GB'
  #config.vm.disk :disk, size: "100GB", primary: true

  if Vagrant.has_plugin?("vagrant-libvirt") && Vagrant.has_plugin?("vagrant-mutate")
    config.vm.provider "libvirt" do |libvirt, override|
        libvirt.cpus=32
        libvirt.memory=125000
        libvirt.machine_virtual_size = 80
    end

    if config.vm.provider == "libvirt"
        server.vm.provision "shell", inline: <<-SHELL
        sudo yum install -y cloud-utils-growpart
        sudo growpart /dev/vda 1
        sudo xfs_growfs /dev/vda1
        SHELL
    end
  end

end
