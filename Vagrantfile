targets = {
  "ubuntu-14.04" => "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box",
}

Vagrant.configure("2") do |config|
  targets.each do |name, url|
    config.vm.define name do |this|
      this.vm.box = name
      this.vm.hostname = name
      this.vm.box_url = url 
    end
  end

  config.vm.provider "virtualbox" do |vb|
    vb.memory = 2048 
    vb.cpus = 2 
    vb.gui = false 
  end
end
