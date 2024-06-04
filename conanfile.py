from conans import ConanFile, CMake, tools
import os, subprocess
from pathlib import Path
import shutil

#conan export .\conanfile.py DebPkg/0.0.1@project1/dev
#conan upload  DebPkg/0.0.1@project1/dev

class DebBase(object):
    name = "deb-package"
    settings = "os", "compiler", "build_type", "arch"
    version = "0.0.1"
    url = "https://git.com/project1/bld-debpackage"
    license = "LICENSE"
    description = "Linux build deb packages"
    
    #removing build artifacts, exclude deb file
    def clear_catalog(self, path, chk_func):
        #chk_func True - removing, False - not removing
        path = Path(path)
        print('------start_on_clear_catalog-------')
        #self.output.info("%s" % path)
        if chk_func:
            for f in path.glob("**/*"):
                if os.path.isdir(f):
                    print('Deleted directory %s' % f)
                    shutil.rmtree(f)
                elif not str(f).endswith(".deb"):
                    f.unlink()
        print('-------end_of_clear_catalog--------')
        #try:
        #f.unlink()
        #except OSError as e:
        #print("Error: %s : %s" % (f, e.strerror))
            #if chk_func(f):
            #    f.unlink()

    def package_install_linux(self, dst_folder):
        if self.settings.os == 'Linux':
            iconsPath="/usr/share/icons/hicolor"
            desktopPath="/usr/share/applications" 
            linkPath="/usr/bin/myapp"
            appName = self.name
            home_dir = self.home_dir
            installAppFolder = self.conan_data["pkgs"]["app"] + self.name + "/"
            prefix_deb ='/DEBIAN'
            prefix_pkgs ='/pkgs'
            image_path = self.image_path
            print("--------------------------1------------------------------")
            self.output.info("%s" % self.image_path)
            #dirPackageInstaller = image_path+prefix_pkgs+prefix_deb
            dirPackageInstaller = self.home_dir+prefix_pkgs+prefix_deb
            self.run("mkdir -p %s" % dirPackageInstaller)
            self.output.info("%s" % os.path.dirname(os.path.realpath(__file__)))
            self.output.info("%s" % dirPackageInstaller)
            self.output.info("%s" % dst_folder)
            self.output.info("selfhome %s" % self.home_dir)
            self.output.info("home %s" % home_dir)
            self.output.info("selfname %s" % self.name)
            self.output.info("appName %s" % appName )
            
            #self.run("ls -la %s" % self.dst_folder)
            pkgs = self.conan_data["pkgs"];
            self.output.info("%s" % pkgs)
            package_type = 'DEB'
            print("---------------------------2-----------------------------")  
            for k,v in pkgs.items():
                #self.output.info("%s " % k)
                if k == "conffiles" and v is not None:
                    print("-----------------------conffiles---------------------------------")
                    self.output.info("%s " % k)
                    for conffiles in pkgs[k]:
                        self.output.info("%s " % conffiles)
                        self.copy(conffiles, src=self.home_dir+"/"+self.name+"/"+'/Package/data/',dst=self.home_dir+prefix_pkgs+pkgs["app"]+self.name)
                        with open(dirPackageInstaller+'/'+k, 'a+') as f:
                            f.write(installAppFolder+conffiles+"\n")
                elif k == "control" and v is not None:
                    print("-----------------------control---------------------------------")
                    for kk,vv in pkgs[k].items():
                        with open(dirPackageInstaller+'/control', 'a+') as ff:
                            print(f"{kk}: {vv}")
                            if kk == "Version" and self.version!="":
                                ff.write(f"{kk}: {self.version}\n")
                            else:
                                ff.write(f"{kk}: {vv}\n")
                elif k == "dirs" and v is not None:
                    print("-----------------------dirs---------------------------------")                    
                    self.output.info("%s" % pkgs[k])
                    for vv in pkgs[k]:
                        with open(dirPackageInstaller+'/'+k, 'a+') as f:
                            f.write(vv+"\n")
                elif k == "systemd" and v is not None:
                    print("------------------------systemd--------------------------------")
                    #print_res = self.run("mkdir -p %s" % self.image_path+prefix_pkgs+"/etc/systemd/system/" )
                    self.run("mkdir -p %s" % self.home_dir+prefix_pkgs+"/etc/systemd/system/" )
                    #self.copy("*.service",src=self.image_path,dst=self.image_path+prefix_pkgs+"/etc/systemd/system/", keep_path=True)
                    #self.copy("*.service",src=self.home_dir+"/"+self.name+'/Package/data/',dst=self.home_dir+prefix_pkgs+"/etc/systemd/system/", keep_path=True)
                    #with open(self.home_dir+"/"+self.name+"/"+pkgs[k], 'r') as f1, open( self.home_dir+prefix_pkgs+'/etc/systemd/system/'+pkgs[k], 'w+') as f2:
                    self.output.info("%s" % self.home_dir+"/"+self.name+'/Package/data/'+pkgs[k] )
                    self.output.info("%s" % self.home_dir+prefix_pkgs+'/etc/systemd/system/'+pkgs[k] )
                    with open(self.home_dir+"/"+self.name+'/Package/data/'+pkgs[k], 'r') as f1, open( self.home_dir+prefix_pkgs+'/etc/systemd/system/'+pkgs[k], 'w+') as f2:
                        f2.write(f1.read().format(USERNAME=pkgs["user"], \
                                                  APPFOLDER=pkgs["app"]+self.name , \
                                                  APPNAME=self.name))
                        self.run("cat %s" % self.home_dir+prefix_pkgs+'/etc/systemd/system/'+pkgs[k] )
                elif k == "desktop" and v is not None:
                    print("--------------------------desktop------------------------------")                    
                    self.output.info("%s" % self.conan_data["pkgs"][k]+self.name)
                elif k == "app" and v is not None:
                    print("--------------------------app------------------------------")
                    #self.output.info("%s" % k )
                    self.run("mkdir -p %s" % self.home_dir+"/"+prefix_pkgs+pkgs["app"]+self.name )
                    self.copy("*", src=dst_folder, dst=self.home_dir+prefix_pkgs+pkgs["app"]+self.name, keep_path=False, symlinks=True)
                    #self.output.info("%s" % print_res )
            print(pkgs["user"], "---" ,pkgs["app"]+self.name , "---" , self.name)
            if os.path.exists(self.home_dir+"/"+self.name+"/"+'/Package/data/'+'postinst'):
                print('---------------- postinst script -------------------------')
                with open(self.home_dir+"/"+self.name+"/"+'/Package/data/'+'postinst', 'r') as f1, open( dirPackageInstaller+"/"+'postinst', 'w+') as f2:
                    f2.write(f1.read().format(USERNAME=pkgs["user"], \
                                            APPFOLDER=pkgs["app"]+self.name , \
                                            APPNAME=self.name))
                self.run("chmod -R 0755 %s" % dirPackageInstaller+"/"+'postinst')
            
            name_deb_package = self.home_dir+"/"+prefix_pkgs+" "+self.package_dir+"/" \
                + self.name + "-" + str(self.settings.build_type) + "-" + str(self.settings.compiler) + str(self.settings.compiler.version) \
                + "-" + self.version + ".deb"
            list_files = self.run("fakeroot dpkg-deb -b %s" % name_deb_package )
            self.output.info("%s" % list_files)
            #self.clear_catalog(image_path, False)

class DebPkg(ConanFile):
    name = "DebPkg"
    url = "https://git.com/project1/bld-debpackage"
    license = "LICENSE"
    description = "Linux build deb packages"
    version = "0.0.1"
