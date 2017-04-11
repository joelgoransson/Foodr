Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "512"
  end

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y python3-pip postgresql-9.3 libpq-dev
    sudo apt-get install -y python3-pip
    sudo pip3 install honcho
    sudo pip3 install -r /vagrant/requirements.txt
    sudo su - postgres -c "createuser -s vagrant"
    sudo su - postgres -c "createdb webapp"
    sudo su - vagrant -c "python3 /vagrant/install.py"
  SHELL
end