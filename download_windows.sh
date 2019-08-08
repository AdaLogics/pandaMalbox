# Create a working directory
mkdir sandbox_base
cd sandbox_base

# Download the disk image from Microsofts' website
# (URL from https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/)
wget https://az792536.vo.msecnd.net/vms/VMBuild_20150916/VirtualBox/IE8/IE8.Win7.VirtualBox.zip

# Unzip the virtualbox zip
unzip IE8.Win7.VirtualBox.zip

# Untar the .ova
tar -xvf IE8\ -\ Win7.ova

# Create a qcow image from the .vmdk file.
## First install qemu utils
sudo apt-get install qemu-utils

## Then create our image
qemu-img convert -O qcow2 IE8\ -\ Win7-disk1.vmdk IE8_win7_disk1.qcow2
chmod +x ./IE8_win7_disk1.qcow2

## Clean up some of the unnecessary files
rm IE8\ -\ Win7-disk1.vmdk
rm IE8\ -\ Win7.ova
