#!/usr/bin/ruby
#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# 
#
require 'net/http'
require 'net/https'
require 'openssl'

require 'rubygems'
require 'json'
require 'cgi'
require 'yaml'

$this_version = '2011.02.01.001'
$resource_url = 'http://169.254.169.254/latest/meta-data/'
$instance_info_hash = Hash.new

def vmInfo()
 def a(address)
         url = URI.parse(address)
         req = Net::HTTP::Get.new(url.path)
         res = Net::HTTP.start(url.host, url.port) { |http| http.request(req) }
         res.body.split().map { |i| lambda{ if i[-1,1] != "/" then $instance_info_hash[(address+i)[40..-1]] = "" else lambda{a(address+i)}.call end}.call}
 end
 def set()
         a($resource_url)
   $instance_info_hash.each_pair{ |key,value|
     url = URI.parse($resource_url+key)
     req = Net::HTTP::Get.new(url.path)
     res = Net::HTTP.start(url.host, url.port) {|http| http.request(req) }
     if res.class == Net::HTTPInternalServerError then $instance_info_hash[key] = nil
                 else $instance_info_hash[key] = res.body end
   }
   $instance_info_hash["event_type"] = "instasnce_lunched"
   $instance_info_hash["linuxusername"] = $linuxusername
   $instance_info_hash["linuxuserpassword"] = $linuxuserpassword
   $instance_info_hash["linuxuservncpassword"] = $vncpassword
   $instance_info_json = $instance_info_hash.to_json
 end
end

# makePasswd function can be simply done by "openssl rand -base64 8"
def makePasswd(n)
 passwd = ""
 lower_chars = ("a".."z").to_a
 upper_chars = ("A".."Z").to_a
 numbers = ("0".."9").to_a
 special_chars = ["~","@","#","$","%","^","*","-"]
 passwd_chars = (lower_chars + upper_chars + numbers + special_chars).uniq
 passwd_chars_size = passwd_chars.size
 passwd = Array.new(n){ passwd_chars[rand(passwd_chars_size)] }.join
 return passwd
=begin
 passwd = ""
 IO.popen("openssl rand -base64 #{n}") { |f| passwd = f.read() }
 return passwd[0..7]
=end
end

def reportToInstanceService(arg)
 instance_service_url = JSON.parse(arg)['atmosphere']['instance_service_url']
 token = JSON.parse(arg)['atmosphere']['token']
 userid = JSON.parse(arg)['atmosphere']['userid']
 uri = URI.parse(instance_service_url)
 data = {'token'=> token, 'userid'=>userid,'vminfo'=>$instance_info_json}
 if uri.scheme == "https"
   http = Net::HTTP.new(uri.host,uri.port)
   http.use_ssl = true
   http.verify_mode = OpenSSL::SSL::VERIFY_NONE
   path = uri.path
   res = http.post(uri.path,data.collect do |key,val| "#{CGI.escape(key.to_s)}=#{CGI.escape(val)}" end.join('&'))
 else
   res = Net::HTTP.post_form(URI.parse(instance_service_url), data)
 end
end


def main(arg)
  $linuxusername = JSON.parse(arg)['atmosphere']['userid']
  $linuxuserpassword = makePasswd(8)
  IO.popen("/usr/sbin/useradd -m -p \`openssl passwd #{$linuxuserpassword}\` #{$linuxusername}") { |f| }
  open('/etc/sudoers','a') { |f| f.puts "## Atmosphere system \n#{$linuxusername}\tALL=(ALL)\tALL" }

  if File.exists?("/etc/atmoconfig")
    begin
      uservnc = false
      config = YAML.load_file '/etc/atmoconfig'
      uservnc = config['uservnc']
    rescue Exception=>e
      #
    end
    if uservnc == true
      $vncpassword = makePasswd(8)
      File.open("/etc/sysconfig/vncservers","a") { |f| f.write("\n###############################\nVNCSERVERS=\"1:#{$linuxusername}\"") }
      IO.popen("sudo -u #{$linuxusername} mkdir /home/#{$linuxusername}/.vnc") { |f| }
      IO.popen("sudo -u #{$linuxusername} touch /home/#{$linuxusername}/.vnc/passwd") { |f| }
      IO.popen("sudo -u #{$linuxusername} /usr/bin/x11vnc -storepasswd #{$vncpassword} /home/#{$linuxusername}/.vnc/passwd") { |f| }
      IO.popen("/sbin/service vncserver start") { |f| }
      IO.popen("cp -r /root/Desktop/ /home/#{$linuxusername}/Desktop/") { |f| }
      IO.popen("chown -R #{$linuxusername}:#{$linuxusername} /home/#{$linuxusername}/Desktop") { |f| }
    end
  end

  vmInfo.set()
  
  #IO.popen("hostname #{$instance_info_hash['hostname']}") { |f| }
  reportToInstanceService(arg)

  # FOR PRODUCTION STAGE
  #IO.popen("rm -fr /tmp/*") { |f| }
end

